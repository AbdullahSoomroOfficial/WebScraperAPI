from django.shortcuts import render, redirect
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import requests
import re


def index(request):
    return render(request, "index.html")


def clean_text(text):
    # Replace multiple spaces with a single space and strip leading/trailing whitespace
    text = re.sub(r"\s+", " ", text)
    text = text.strip()
    return text


def scrape_website(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        # Get text content and clean it up
        text = clean_text(soup.get_text())

        # Get all regular links (anchor tags)
        links = list(
            set([urljoin(url, a["href"]) for a in soup.find_all("a", href=True)])
        )

        # Get all external CSS links
        css_links = list(
            set(
                [
                    urljoin(url, link["href"])
                    for link in soup.find_all("link", rel="stylesheet", href=True)
                ]
            )
        )

        # Extract page title
        title = soup.title.string.strip() if soup.title else "No title"

        # Extract h1 headings
        headings = [h.get_text(strip=True) for h in soup.find_all("h1")]

        # Extract meta description
        meta = soup.find("meta", attrs={"name": "description"})
        description = (
            meta["content"].strip()
            if meta and "content" in meta.attrs
            else "No meta description"
        )

        return {
            "page_title": title,
            "description": description,
            "headings": headings,
            "text_snippet": text[:500],  # Take only first 500 characters for preview
            "links": links,
            "external_css": css_links,  # Return the CSS links as well
        }

    except requests.exceptions.RequestException as e:
        return {"error": f"Request failed: {e}"}
    except Exception as e:
        return {"error": f"An error occurred: {e}"}


def scrape(request):
    if request.method == "GET":
        url = request.GET.get("url")
        if url:
            results = scrape_website(url)
            return render(request, "details.html", {"results": results})
    # If no URL provided, redirect back to index
    return render(request, "index.html", {"error": "Please provide a URL."})
