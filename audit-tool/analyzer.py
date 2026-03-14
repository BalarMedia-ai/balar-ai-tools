import requests
import urllib3
from bs4 import BeautifulSoup

# Suppress SSL warnings for sites with cert issues
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-AU,en;q=0.9",
    "Accept-Encoding": "gzip, deflate",
    "Connection": "keep-alive",
}


def _normalise_url(url):
    """Ensure URL has a scheme. Default to https://."""
    url = url.strip()
    if not url.startswith(("http://", "https://")):
        url = "https://" + url
    return url


def _fetch_html(url):
    """
    Fetch HTML with a multi-strategy approach:
    1. HTTPS with browser UA (verify=False to handle cert issues)
    2. HTTP fallback (handles sites that geo-block HTTPS from non-AU IPs)
    Returns (html_text, final_url, error_message)
    """
    # Strategy 1: HTTPS
    https_url = url if url.startswith("https://") else url.replace("http://", "https://", 1)
    try:
        r = requests.get(https_url, timeout=12, headers=HEADERS,
                         allow_redirects=True, verify=False)
        if r.status_code == 200 and len(r.text) > 500:
            return r.text, r.url, None
    except requests.exceptions.Timeout:
        pass  # Fall through to HTTP
    except Exception:
        pass

    # Strategy 2: HTTP fallback (handles geo-blocked HTTPS)
    http_url = https_url.replace("https://", "http://", 1)
    try:
        r = requests.get(http_url, timeout=12, headers=HEADERS,
                         allow_redirects=True, verify=False)
        if r.status_code == 200 and len(r.text) > 500:
            return r.text, r.url, None
    except Exception as e:
        return None, url, str(e)

    return None, url, "Could not retrieve page — site may be blocking automated requests."


def analyze_website(url):
    url = _normalise_url(url)

    results = {
        "url": url,
        "title": False,
        "title_text": "",
        "meta_description": False,
        "meta_description_text": "",
        "h1": False,
        "h1_text": "",
        "images_total": 0,
        "images_missing_alt": 0,
        "word_count": 0,
        "error": None,
        "fetch_url": url,
    }

    html, final_url, error = _fetch_html(url)
    results["fetch_url"] = final_url

    if html is None:
        results["error"] = error or "Failed to fetch page."
        return results

    soup = BeautifulSoup(html, "html.parser")

    # Title tag
    if soup.title and soup.title.string:
        results["title"] = True
        results["title_text"] = soup.title.string.strip()[:80]

    # Meta description
    meta = soup.find("meta", attrs={"name": "description"})
    if meta and meta.get("content", "").strip():
        results["meta_description"] = True
        results["meta_description_text"] = meta["content"].strip()[:120]

    # H1 tag
    h1 = soup.find("h1")
    if h1 and h1.get_text(strip=True):
        results["h1"] = True
        results["h1_text"] = h1.get_text(strip=True)[:80]

    # Images and alt tags
    images = soup.find_all("img")
    results["images_total"] = len(images)
    results["images_missing_alt"] = sum(
        1 for img in images if not img.get("alt", "").strip()
    )

    # Word count (body text only, strip scripts/styles)
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()
    text = soup.get_text(separator=" ")
    results["word_count"] = len(text.split())

    return results
