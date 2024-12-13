import requests
from bs4 import BeautifulSoup
import re
BASE_URL = "https://cantusdatabase.org/sources/"
PAGE_COUNT = 6  
pattern = re.compile(r"^/source/\d+$")
with open("valid_sources.txt", "w") as file:
    for page in range(1, PAGE_COUNT + 1):
        url = f"{BASE_URL}?page={page}"
        print(f"Fetching page: {url}")
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            links = soup.find_all("a", href=pattern)
            for link in links:
                href = link.get("href")
                if href:
                    number = href.split("/")[-1]
                    name = link.get_text(strip=True)  
                    print(f"Found valid number: {number}, Name: {name}")
                    file.write(f"{number}: {name}\n")
        else:
            print(f"Failed to fetch page {page}. Status code: {response.status_code}")
print("Finished scraping pages. Saved to valid_sources.txt.")
