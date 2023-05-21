import requests
from bs4 import BeautifulSoup
from urllib.parse import quote, urljoin

# Get the search term from the user
search_term = input("Enter the search term: ")

# Encode the search term for the URL
encoded_search_term = quote(search_term)

# Construct the search URL
search_url = f"https://stolenrecordclub.com/search?q={encoded_search_term}&type=product"

# Send a GET request to the search URL and obtain the HTML content
response = requests.get(search_url)
html_content = response.text

# Create a Beautiful Soup object
soup = BeautifulSoup(html_content, "html.parser")

# Find all the product items
product_items = soup.find_all("div", class_="product-grid-item")

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

    print("Name:", name)
    print("Image URL:", image_url)
    print("Price:", price)
    print("View Details URL:", view_details_url)
    print("---------------------")



