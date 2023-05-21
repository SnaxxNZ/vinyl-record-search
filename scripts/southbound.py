import requests
from bs4 import BeautifulSoup
from urllib.parse import quote

# Get the search term from the user
search_term = input("Enter the search term: ")

# Encode the search term for the URL
encoded_search_term = quote(search_term)

# Construct the search URL
search_url = f"https://www.southbound.co.nz/?s={encoded_search_term}&post_type=product&type_aws=true&aws_id=1&aws_filter=1"

# Send a GET request to the search URL and obtain the HTML content
response = requests.get(search_url)
html_content = response.text

# Create a Beautiful Soup object
soup = BeautifulSoup(html_content, "html.parser")

# Check if the search result is a single product page
is_single_product = soup.find("div", class_="et_pb_module et_pb_wc_title et_pb_wc_title_0_tb_body et_pb_bg_layout_light")

if is_single_product:
    # Extract information from the single product page
    name_element = soup.find("div", class_="et_pb_module_inner").find("h1")
    name = name_element.get_text() if name_element else "N/A"

    image_element = soup.find("figure", class_="woocommerce-product-gallery__wrapper")
    image_url = image_element.find("img")["data-large_image"] if image_element else "N/A"

    price_element = soup.find("span", class_="woocommerce-Price-amount")
    price = price_element.get_text() if price_element else "N/A"

    view_details_url = search_url

    print("Name:", name)
    print("Image URL:", image_url)
    print("Price:", price)
    print("View Details URL:", view_details_url)
    print("---------------------")
else:
    # Find all the product items
    product_items = soup.find_all("li", class_="product")

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

        print("Name:", name)
        print("Image URL:", image_url)
        print("Price:", price)
        print("View Details URL:", view_details_url)
        print("---------------------")
