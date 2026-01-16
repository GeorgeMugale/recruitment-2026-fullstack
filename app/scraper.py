from typing import Dict, List
import requests
from bs4 import BeautifulSoup

URL = "https://www.parliament.gov.zm/members/constituencies"


def scrape_zambia_constituencies() -> Dict[str, List[str]]:
    """
    Scrape provinces and constituencies from the National Assembly of Zambia website.

    Returns:
        dict[str, list[str]]: Province -> constituencies mapping
    
    Raises:
        ConnectionError: If unable to fetch data
        ValueError: If HTML structure is unexpected and cannot be parsed
    """
    # Basic error handling with try-except blocks
    try: 
        # Fetch the webpage with SSL verification
        response = requests.get(URL, timeout=30, verify=False,)
        
        
        # Raise exception for HTTP errors
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        data = {}
        
        # Find province headings
        province_headings = soup.select("div.view-content > h3")
        
        if not province_headings:
            raise ValueError("Could not find province headings in the page")

        found_data = False
        for province_heading in province_headings:
            province = province_heading.get_text(strip=True)
            table = province_heading.find_next_sibling("table")

            if not table:
                continue

            constituencies = [
                a.get_text(strip=True)
                for a in table.select("a")
                if a.get_text(strip=True)
            ]
            
            if constituencies:
                data[province] = constituencies
                found_data = True
        
        if not found_data:
            raise ValueError("No constituency data found")

        return data
    # Handle errors gracefully
    except requests.exceptions.RequestException as e:
        # Wrap requests exceptions in ConnectionError
        raise ConnectionError(f"Failed to fetch data: {e}")
    except Exception as e:
        # Catch any other unexpected errors
        raise ValueError(f"Failed to parse data: {e}")
        
    
    
