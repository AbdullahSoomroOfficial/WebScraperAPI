# Web Scraper API

A Django-based web scraping application that extracts information from websites.

## Features

- Scrape website content
- Extract page title, meta description, and headings
- Collect all links from the page
- Find external CSS files
- Clean text content preview
- Modern, responsive UI

## Setup

1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/WebScraperAPI.git
cd WebScraperAPI
```

2. Create and activate virtual environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies

```bash
pip install -r requirements.txt
```

4. Run migrations

```bash
python manage.py migrate
```

5. Start development server

```bash
python manage.py runserver
```

## Usage

1. Open browser and go to `http://localhost:8000`
2. Enter a URL to scrape
3. View the extracted information in a clean, organized format

## Technologies

- Django
- BeautifulSoup4
- Requests
- HTML5/CSS3
