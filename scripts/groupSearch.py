from concurrent.futures import ThreadPoolExecutor, as_completed
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from urllib.parse import quote, urljoin
from bs4 import BeautifulSoup
import requests

# Define the search term for all scripts
search_term = input("Enter the search term: ")
encoded_search_term = quote(search_term)

# Script 1
def script1():
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

    # Define an empty list to store the results
    results = []

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

        # Return the extracted information as a tuple
        return title, price, image_url_absolute, product_url

    # Create a ThreadPoolExecutor with a maximum of 5 worker threads
    executor = ThreadPoolExecutor(max_workers=5)

    # Submit the scraping tasks to the executor
    scraping_tasks = [executor.submit(scrape_product, item) for item in product_items]

    # Process the results as they become available
    for task in as_completed(scraping_tasks):
        try:
            title, price, image_url, product_url = task.result()
            results.append((title, price, image_url, product_url))
        except Exception as e:
            print("Error occurred:", str(e))

    # Close the WebDriver instance
    driver.quit()

    # Return the list of results
    return results

# Script 2
def script2():
    search_url = f"http://www.justfortherecord.co.nz/albums/?filter%5Bkeyword%5D={encoded_search_term}&filter%5Bcondition%5D=any&filter%5Borigin%5D=any&filter%5Bpage_length%5D=54&filter%5Bsort_order%5D=stocked_date"
    # Send a GET request to the search URL and obtain the HTML content
    response = requests.get(search_url)
    html_content = response.text

    # Create a Beautiful Soup object
    soup = BeautifulSoup(html_content, "html.parser")

    # Find all the product items
    product_items = soup.find_all("div", class_="product-item")

    # Define an empty list to store the results
    results = []

    # Iterate over the product items and extract the desired information
    for item in product_items:
        name_element = item.find("div", class_="name")
        name = name_element.a.get_text() if name_element else "N/A"

        image_element = item.find("div", class_="image")
        image_url = image_element.img["src"] if image_element else "N/A"
        image_url = urljoin(search_url, image_url)  # Convert to absolute URL

        price_element = item.find("div", class_="price")
        price = price_element.span.get_text() if price_element else "N/A"

        view_details_element = item.find("div", class_="cart")
        view_details_url = view_details_element.a["href"] if view_details_element else "N/A"
        view_details_url = urljoin(search_url, view_details_url)  # Convert to absolute URL

        # Append the extracted information as a tuple to the results list
        results.append((name, price, image_url, view_details_url))

    # Return the list of results
    return results


# Script 3
def script3():
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

    # Define an empty list to store the results
    results = []

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

        # Append the extracted information as a tuple to the results list
        results.append((title, price, image_url, url, format_info, artist))

    # Return the list of results
    return results


def script4():
    search_url = f"https://www.southbound.co.nz/?s={encoded_search_term}&post_type=product&type_aws=true&aws_id=1&aws_filter=1"
    # Send a GET request to the search URL and obtain the HTML content
    response = requests.get(search_url)
    html_content = response.text

    # Create a Beautiful Soup object
    soup = BeautifulSoup(html_content, "html.parser")

    # Check if the search result is a single product page
    is_single_product = soup.find("div",
                                  class_="et_pb_module et_pb_wc_title et_pb_wc_title_0_tb_body et_pb_bg_layout_light")

    if is_single_product:
        # Extract information from the single product page
        name_element = soup.find("div", class_="et_pb_module_inner").find("h1")
        name = name_element.get_text() if name_element else "N/A"

        image_element = soup.find("figure", class_="woocommerce-product-gallery__wrapper")
        image_url = image_element.find("img")["data-large_image"] if image_element else "N/A"

        price_element = soup.find("span", class_="woocommerce-Price-amount")
        price = price_element.get_text() if price_element else "N/A"

        view_details_url = search_url

        # Return the extracted information as a list containing a single tuple
        return [(name, price, image_url, view_details_url)]
    else:
        # Find all the product items
        product_items = soup.find_all("li", class_="product")

        # Define an empty list to store the results
        results = []

        # Iterate over the product items and extract the desired information
        for item in product_items:
            name_element = item.find("h2", class_="woocommerce-loop-product__title")
            name = name_element.get_text() if name_element else "N/A"

            image_element = item.find("img", class_="attachment-woocommerce_thumbnail")
            image_url = image_element["data-src"] if image_element else "N/A"

            price_element = item.find("span", class_="woocommerce-Price-amount")
            price = price_element.get_text() if price_element else "N/A"

            view_details_element = item.find("a", class_="woocommerce-LoopProduct-link")
            view_details_url = view_details_element["href"] if view_details_element else "N/A"

            # Append the extracted information as a tuple to the results list
            results.append((name, price, image_url, view_details_url))

        # Return the list of results
        return results


def script5():
    search_url = f"https://stolenrecordclub.com/search?q={encoded_search_term}&type=product"
    # Send a GET request to the search URL and obtain the HTML content
    response = requests.get(search_url)
    html_content = response.text

    # Create a Beautiful Soup object
    soup = BeautifulSoup(html_content, "html.parser")

    # Find all the product items
    product_items = soup.find_all("div", class_="product-grid-item")

    # Define an empty list to store the results
    results = []

    # Iterate over the product items and extract the desired information
    for item in product_items:
        name_element = item.find("h3", class_="product-title").find("a")
        name = name_element.get_text(strip=True) if name_element else "N/A"

        image_element = item.find("a", class_="jas-product-img-element")
        image_url = image_element["data-bgset"].split(" ")[0] if image_element else "N/A"
        image_url = urljoin(search_url, image_url)  # Convert to absolute URL

        price_element = item.find("span", class_="price")
        price = price_element.get_text(strip=True) if price_element else "N/A"

        view_details_element = item.find("h3", class_="product-title").find("a")
        view_details_url = view_details_element["href"] if view_details_element else "N/A"
        view_details_url = urljoin(search_url, view_details_url)  # Convert to absolute URL

        # Append the extracted information as a tuple to the results list
        results.append((name, price, image_url, view_details_url))

    # Return the list of results
    return results


def script6():
    # Construct the search URL for the new website
    search_url = f"https://vinylcountdown.co.nz/?s={encoded_search_term}&post_type=product"

    # Send a GET request to the search URL and obtain the HTML content
    response = requests.get(search_url)
    html_content = response.text

    # Create a Beautiful Soup object
    soup = BeautifulSoup(html_content, "html.parser")

    # Define an empty list to store the results
    results = []

    # Check if the search result is a product page
    product_page = soup.find("div", class_="summary entry-summary")
    if product_page:
        # Extract information from the product page
        name_element = product_page.find("h1", class_="product_title")
        name = name_element.get_text() if name_element else "N/A"

        price_element = product_page.find("p", class_="price")
        price = price_element.get_text() if price_element else "N/A"

        view_details_url = search_url  # The current URL is the product page URL

        image_element = soup.find("div", class_="woocommerce-product-gallery__image")
        image_url = image_element["data-thumb"] if image_element else "N/A"

        # Append the extracted information as a tuple to the results list
        results.append((name, price, image_url, view_details_url))
    else:
        # Find all the product items on the new website
        product_items = soup.find_all("li", class_="ast-col-sm-12")

        # Iterate over the product items and extract the desired information
        for item in product_items:
            name_element = item.find("a", class_="woocommerce-LoopProduct-link")
            name = name_element.get_text() if name_element else "N/A"

            image_element = item.find("img", class_="attachment-woocommerce_thumbnail")
            image_url = image_element["src"] if image_element else "N/A"
            image_url = urljoin(search_url, image_url)  # Convert to absolute URL

            price_element = item.find("span", class_="price")
            price = price_element.get_text() if price_element else "N/A"

            view_details_element = item.find("a", class_="button")
            view_details_url = view_details_element["href"] if view_details_element else "N/A"
            view_details_url = urljoin(search_url, view_details_url)  # Convert to absolute URL

            # Append the extracted information as a tuple to the results list
            results.append((name, price, image_url, view_details_url))

    # Return the list of results
    return results


# List to store the results from each script
results = []

# Run each script and collect the results
for script in [script1, script2, script3, script4, script5, script6]:
    try:
        print(f"Running {script.__name__}...")
        output = script()
        print(f"{script.__name__} output: {output}")
        if output is not None and output != "N/A":  # Check if the output is not None or "N/A"
            results.append((script.__name__, output))
        print(f"{script.__name__} completed.")
    except Exception as e:
        print(f"Error occurred in {script.__name__}: {str(e)}")
        continue

# Debug output - Print intermediate results
print("Intermediate Results:")
for result in results:
    script_name, script_result = result
    print(f"{script_name}: {script_result}")

# Find the stores and their prices in ascending order
sorted_results = []

for script, result in results:
    if isinstance(result, list):
        for item in result:
            if len(item) >= 4:
                price = item[1]
                if price != "N/A":
                    # Extract only the numeric part of the price
                    price_value = float(''.join(filter(str.isdigit, price.replace(",", ".")))) / 100
                    sorted_results.append((price_value, script, item[2], item[3]))
    elif len(result) >= 4:
        price = result[1]
        if price != "N/A":
            # Extract only the numeric part of the price
            price_value = float(''.join(filter(str.isdigit, price.replace(",", ".")))) / 100
            sorted_results.append((price_value, script, result[2], result[3]))

# Sort the results in ascending order based on price
sorted_results.sort()

# Print the sorted results
if sorted_results:
    print("Ranking of stores from lowest to highest price:")
    for i, (price, script, image_url, view_details_url) in enumerate(sorted_results, start=1):
        print(f"{i}. {script}: ${price:.2f}")
        print(f"   Image URL: {image_url}")
        print(f"   View Details URL: {view_details_url}")
else:
    print("No valid results found from the scripts.")
