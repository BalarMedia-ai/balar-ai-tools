import requests
from bs4 import BeautifulSoup


def analyze_website(url):
    results = {
        "title": False,
        "meta_description": False,
        "h1": False,
        "images_missing_alt": 0,
        "word_count": 0
    }
    try:
        r = requests.get(url, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")

        # title
        if soup.title:
            results["title"] = True

        # meta description
        meta = soup.find("meta", attrs={"name": "description"})
        if meta:
            results["meta_description"] = True

        # h1
        if soup.find("h1"):
            results["h1"] = True

        # alt tags
        images = soup.find_all("img")
        for img in images:
            if not img.get("alt"):
                results["images_missing_alt"] += 1

        # word count
        text = soup.get_text()
        results["word_count"] = len(text.split())

    except Exception:
        pass

    return results
