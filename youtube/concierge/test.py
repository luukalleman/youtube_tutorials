import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Base URL of the Virgin Atlantic annual reports page
base_url = "https://corporate.virginatlantic.com"

# Path to the specific annual reports page
url_path = "/gb/en/annual-reports.html"

# Send a GET request to fetch the page content
response = requests.get(base_url + url_path)

# Parse the page content using BeautifulSoup
soup = BeautifulSoup(response.content, "html.parser")

# Find the link to the 2023 annual report
report_link = None
for link in soup.find_all("a"):
    if "Annual Report 2022" in link.text:
        report_link = link.get("href")
        break

# Print the complete URL to the 2023 annual report
if report_link:
    full_link = urljoin(base_url, report_link)
    print("Link to the 2022 Annual Report:", full_link)
else:
    print("2023 Annual Report link not found.")
