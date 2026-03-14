# Balar AI Tools — Website Audit Tool

A lightweight Flask web app that performs an instant SEO audit on any URL.

## Features

- Checks for title tag, meta description, and H1 tag
- Counts images missing alt attributes
- Reports total word count
- Scores the site out of 100
- Lead capture form on results page

## Quick Start

```bash
pip install -r requirements.txt
python server.py
```

Then open [http://localhost:5000](http://localhost:5000) in your browser.

## Project Structure

```
audit-tool/
├── server.py          # Flask app & routing
├── analyzer.py        # Website scraping & SEO checks
├── requirements.txt
├── templates/
│   ├── index.html     # Audit input form
│   └── result.html    # Score & results page
└── static/
    └── style.css      # Balar Media branding styles
```

## Built by

[Balar Media Group](https://balarmediagroup.com.au)
