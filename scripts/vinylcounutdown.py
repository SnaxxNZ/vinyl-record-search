import requests
from bs4 import BeautifulSoup
from urllib.parse import quote, urljoin

# Get the search term from the user
search_term = input("Enter the search term: ")

# Encode the search term for the URL
encoded_search_term = quote(search_term)

# Construct the search URL for the new website
search_url = f"https://vinylcountdown.co.nz/?s={encoded_search_term}&post_type=product"

# Send a GET request to the search URL and obtain the HTML content
response = requests.get(search_url)
html_content = response.text

# Create a Beautiful Soup object
soup = BeautifulSoup(html_content, "html.parser")

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

    print("Name:", name)
    print("Price:", price)
    print("Image URL:", image_url)
    print("View Details URL:", view_details_url)
    print("---------------------")
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

        print("Name:", name)
        print("Image URL:", image_url)
        print("Price:", price)
        print("View Details URL:", view_details_url)
        print("---------------------")