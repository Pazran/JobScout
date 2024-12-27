import requests
from bs4 import BeautifulSoup

# URL to scrape
url = "http://my.jobstreet.com/hse-jobs"

# Scrape the content
response = requests.get(url)
if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')

    # Save the HTML content to a file
    with open('mock_jobstreet.html', 'w', encoding='utf-8') as file:
        file.write(str(soup))
