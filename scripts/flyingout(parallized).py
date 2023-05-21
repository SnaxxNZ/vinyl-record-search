from concurrent.futures import ThreadPoolExecutor, as_completed
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from urllib.parse import quote, urljoin
from bs4 import BeautifulSoup

# Get the search term from the user
search_term = input("Enter the search term: ")

# Encode the search term for the URL
encoded_search_term = quote(search_term)

# Construct the search URL with the encoded search term
search_url = f"https://flyingout.co.nz/search?q={encoded_search_term}"

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

# Create a Beautiful Soup object
soup = BeautifulSoup(html_content, "html.parser")

# Find all the product items
product_items = soup.find_all("div", class_="boost-pfs-filter-product-item-inner")

# Function to scrape information for a single product item
def scrape_product(item):
    title_element = item.find("a", class_="boost-pfs-filter-product-item-title")
    title = title_element.get_text() if title_element else "N/A"

    url_element = item.find("a", class_="boost-pfs-filter-product-item-image-link")
    product_url = "https://flyingout.co.nz" + url_element["href"] if url_element else "N/A"

    # Visit the product page
    driver.get(product_url)

    # Get the page source after the dynamic content has loaded
    product_html_content = driver.page_source

    # Create a Beautiful Soup object for the product page
    product_soup = BeautifulSoup(product_html_content, "html.parser")

    # Extract additional information from the product page
    price_element = product_soup.find("div", id="price").find("span", class_="current-price")
    price = price_element.get_text() if price_element else "N/A"

    image_element = product_soup.find("div", class_="product-media product-media--image")
    image_url_relative = image_element.find("a", class_="main-img-link")["href"] if image_element else "N/A"
    image_url_absolute = urljoin(product_url, image_url_relative)

    # Return the extracted information
    return title, price, image_url_absolute, product_url

# Create a ThreadPoolExecutor with a maximum of 5 worker threads
executor = ThreadPoolExecutor(max_workers=5)

# Submit the scraping tasks to the executor
scraping_tasks = [executor.submit(scrape_product, item) for item in product_items]

# Process the results as they become available
for task in as_completed(scraping_tasks):
    try:
        title, price, image_url, product_url = task.result()
        print("Title:", title)
        print("Price:", price)
        print("Image URL:", image_url)
        print("URL:", product_url)
        print("---------------------")
    except Exception as e:
        print("Error occurred:", str(e))

# Close the WebDriver instance
driver.quit()
