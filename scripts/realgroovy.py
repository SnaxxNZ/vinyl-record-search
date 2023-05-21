from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from urllib.parse import quote

# Get the search term from the user
search_term = input("Enter the search term: ")

# Encode the search term for the URL
encoded_search_term = quote(search_term)

# Construct the search URL with the encoded search term
search_url = f"https://realgroovy.co.nz/search?q={encoded_search_term}"

# Configure Selenium options
options = Options()
options.add_argument("--headless")  # Run in headless mode, without opening a browser window

# Set the path to your ChromeDriver executable
webdriver_path = "/usr/bin/chromedriver"

# Create a new ChromeDriver service
service = Service(webdriver_path)

# Create a new WebDriver instance with headless mode enabled
driver = webdriver.Chrome(service=service, options=options)

# Navigate to the search URL
driver.get(search_url)

# Get the page source after the dynamic content has loaded
html_content = driver.page_source

# Close the WebDriver instance
driver.quit()

# Create a Beautiful Soup object
soup = BeautifulSoup(html_content, "html.parser")

# Find all the product items
product_items = soup.find_all("div", class_="ais-hits--item")

# Iterate over the product items and extract the desired information
for item in product_items:
    title = item.find("div", class_="text").get_text()

    # Check if the img element exists before accessing its src attribute
    img_element = item.find("img", class_="img")
    image_url = img_element["src"] if img_element else "N/A"

    price = item.find("div", class_="title").strong.get_text()
    artist = item.find("div", class_="subtitle").get_text()
    format_info = item.find("div", class_="caption").get_text()
    url = "https://realgroovy.co.nz" + item.find("a", class_="display-card")["href"]

    print("Title:", title)
    print("Image URL:", image_url)
    print("Price:", price)
    print("Artist:", artist)
    print("Format:", format_info)
    print("URL:", url)
    print("---------------------")
