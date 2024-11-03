import requests
import time
import platform
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote_plus
import time
import logging


def get_current_time() -> str:
    """Get the current time"""
    current_time = time.strftime("%A, %m/%d/%Y, %H:%M:%S")
    return f"The current time is {current_time}"

def get_system_info() -> str:
    """Get System Information"""
    return f"The system is {platform.system()} running on {platform.processor()}"


def google_search(query, num_results=10, language="en"):
    """
    Scrapes Google search results.
    
    Parameters:
    - query: The search term
    - num_results: Number of results to return (default: 10)
    - language: Search language (default: "en" for English)
    
    Returns:
    A list of dictionaries containing titles, links, and snippets
    """
    
    # Format the query for URL
    encoded_query = quote_plus(query)
    
    # Create URL
    url = f"https://www.google.com/search?q={encoded_query}&hl={language}&num={num_results}"
    
    # Headers to mimic a browser request
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    try:
        # Make the request
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for bad status codes
        
        # Parse the HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find all search result divs
        search_results = []
        
        # Find all result divs
        results = soup.find_all('div', class_='g')
        
        for result in results:
            try:
                # Extract title
                title_element = result.find('h3')
                title = title_element.text if title_element else ""
                
                # Extract link
                link_element = result.find('a')
                link = link_element['href'] if link_element else ""
                
                # Extract snippet
                snippet_element = result.find('div', class_='VwiC3b')
                snippet = snippet_element.text if snippet_element else ""
                
                # Only add if we have at least a title and link
                if title and link:
                    search_results.append({
                        'title': title,
                        'link': link,
                        'snippet': snippet
                    })
                    
                if len(search_results) >= num_results:
                    break
                    
            except Exception as e:
                print(f"Error parsing result: {e}")
                continue
        
        return search_results
        
    except requests.RequestException as e:
        print(f"Error fetching search results: {e}")
        return []


def browse_url(url: str) -> str:
    """
    Scrapes text content from a given URL.
    """
    logging.info(f"Scraping URL: {url}")
    try:
        # Enhanced headers
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
        }
        
        # Add timeout and verify parameters
        response = requests.get(url, headers=headers, timeout=30, verify=True)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # More specific content extraction for LiveMint
        article_content = soup.find('div', {'class': 'mainArea'}) or soup.find('article')
        
        if article_content:
            # Remove unwanted elements
            for unwanted in article_content.find_all(['script', 'style', 'nav', 'header', 'footer']):
                unwanted.decompose()
                
            text = article_content.get_text(separator=' ', strip=True)
        else:
            text = soup.get_text(separator=' ', strip=True)
            
        return text.strip()
        
    except requests.RequestException as e:
        logging.error(f"Request error: {e}")
        return f"Error fetching content: {e}"
    except Exception as e:
        logging.error(f"Processing error: {e}")
        return f"Error processing content: {e}"
    

tools = [
    {
        'type': 'function',
        'function': {
            'name': 'get_current_time',
            'description': 'Get the current time',
            'parameters': {
                'type': 'object',
                'properties': {},
                'required': [],
            },
        },
    },
    {
        'type': 'function',
        'function': {
            'name': 'get_system_info',
            'description': 'Get System Information',
            'parameters': {
                'type': 'object',
                'properties': {},
                'required': [],
            },
        },
    },
    {
        'type': 'function',
        'function': {
            'name': 'google_search',
            'description': 'Search the web using Google Search API',
            'parameters': {
                'type': 'object',
                'properties': {
                    "query": {
                        "type": "string",
                        "description": "The search query",
                    },
                },
                'required': ['query'],
            },
        },
    },
    {
        'type': 'function',
        'function': {
            'name': 'browse_url',
            'description': 'Scrape text content from a given URL',
            'parameters': {
                'type': 'object',
                'properties': {
                    "url": {
                        "type": "string",
                        "description": "The URL to scrape",
                    },
                },
                'required': ['url'],
            },
        },
    },
]
