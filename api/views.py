from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re
import ollama


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

        # Fallback in case no headings are found
        if not headings:
            headings = ["No headings found"]

        # Extract meta description
        meta = soup.find("meta", attrs={"name": "description"})
        description = (
            meta["content"].strip()
            if meta and "content" in meta.attrs
            else "No meta description"
        )

        print(
            "========================================================================"
        )
        print(
            "========================================================================"
        )
        print(soup)
        print(
            "========================================================================"
        )
        print(
            "========================================================================"
        )

        # Ensure we return some meaningful data
        return {
            "page_title": title,
            "description": description,
            "headings": headings,
            "text_snippet": text,  # Increase the snippet size if needed
            "links": links,
            "external_css": css_links,  # Return the CSS links as well
        }

    except requests.exceptions.RequestException as e:
        return {"error": f"Request failed: {e}"}
    except Exception as e:
        return {"error": f"An error occurred: {e}"}


def generate_summary(scraped_data):
    # Prepare the data for summarization
    input_data = f"""
    Website Title: {scraped_data['page_title']}
    Meta Description: {scraped_data['description']}
    Headings: {', '.join(scraped_data['headings'])}
    Text Snippet: {scraped_data['text_snippet']}
    Links: {scraped_data['links']}
    External Links: {scraped_data['external_css']}
    
    Please summarize the website and provide an overview of what the website is about. 
    Be sure to include the main topics, its purpose, and any other key insights you can infer from the content.
    """

    try:
        # Directly call ollama.chat() to get the response
        response = ollama.chat(
            model="llama3", messages=[{"role": "user", "content": input_data}]
        )

        # Access the content of the response
        summary = response["message"]["content"]
        return summary

    except Exception as e:
        return f"An error occurred while generating the summary: {e}"


def scrape(request):
    if request.method == "GET":
        url = request.GET.get("url")
        if url:
            # Scrape the website data
            results = scrape_website(url)

            # If there's no error, generate a summary using Llama 3
            if "error" not in results:
                summary = generate_summary(results)
                results["ai_summary"] = summary  # Add AI-generated summary to results

            return render(request, "details.html", {"results": results})

    # If no URL provided, redirect back to index
    return render(request, "index.html", {"error": "Please provide a URL."})


def index(request):
    return render(request, "index.html")
