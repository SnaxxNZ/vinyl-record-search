import re
import requests
import multiprocessing
import concurrent.futures
from urllib.parse import quote, urljoin
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

search_term = input("Enter the search term: ")
encoded_search_term = quote(search_term)


def script1():
    search_url = f"https://flyingout.co.nz/search?q={encoded_search_term}"

    options = Options()
    options.add_argument("--headless")  # Run in headless mode, without opening a browser window

    webdriver_path = ChromeDriverManager().install()

    service = Service(webdriver_path)

    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get(search_url)

        html_content = driver.page_source
        soup = BeautifulSoup(html_content, "html.parser")
        product_items = soup.select("div.boost-pfs-filter-product-item-inner")
        results = []

        def scrape_product(item):
            title_element = item.find("a", class_="boost-pfs-filter-product-item-title")
            title = title_element.get_text() if title_element else "N/A"

            url_element = item.find("a", class_="boost-pfs-filter-product-item-image-link")
            product_url = "https://flyingout.co.nz" + url_element["href"] if url_element else "N/A"
            driver.get(product_url)
            product_html_content = driver.page_source
            product_soup = BeautifulSoup(product_html_content, "html.parser")
            price_element = product_soup.find("div", id="price").find("span", class_="current-price")
            price = price_element.get_text() if price_element else "N/A"

            image_element = product_soup.find("div", class_="product-media product-media--image")
            image_url_relative = image_element.find("a", class_="main-img-link")["href"] if image_element else "N/A"
            image_url_absolute = urljoin(product_url, image_url_relative)
            return title, price, image_url_absolute, product_url
        executor = ThreadPoolExecutor(max_workers=5)
        scraping_tasks = [executor.submit(scrape_product, item) for item in product_items]
        for task in as_completed(scraping_tasks):
            try:
                title, price, image_url, product_url = task.result()
                results.append((title, price, image_url, product_url))
            except Exception as e:
                print("Error occurred:", str(e))
        return results

    finally:
        driver.quit()


def script2():
    search_url = f"http://www.justfortherecord.co.nz/albums/?filter%5Bkeyword%5D={encoded_search_term}&filter%5Bcondition%5D=any&filter%5Borigin%5D=any&filter%5Bpage_length%5D=54&filter%5Bsort_order%5D=stocked_date"
    session = requests.Session()
    response = session.get(search_url)
    html_content = response.text
    soup = BeautifulSoup(html_content, "html.parser")
    product_items = soup.find_all("div", class_="product-item")
    results = [
        (
            item.select_one("div.name a").get_text() if item.select_one("div.name") else "N/A",
            item.select_one("div.price span").get_text() if item.select_one("div.price") else "N/A",
            urljoin(search_url, item.select_one("div.image img")["src"]) if item.select_one("div.image") else "N/A",
            urljoin(search_url, item.select_one("div.cart a")["href"]) if item.select_one("div.cart") else "N/A"
        )
        for item in product_items
    ]
    return results


def script3():
    search_url = f"https://realgroovy.co.nz/search?q={encoded_search_term}"
    options = Options()
    options.add_argument("--headless")
    webdriver_path = ChromeDriverManager().install()
    service = Service(webdriver_path)
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(search_url)
    html_content = driver.page_source
    driver.quit()
    soup = BeautifulSoup(html_content, "html.parser")
    product_items = soup.find_all("div", class_="ais-hits--item")
    results = []
    for item in product_items:
        title = item.find("div", class_="text").get_text() if item.find("div", class_="text") else "N/A"
        img_element = item.find("img", class_="img")
        image_url = img_element["src"] if img_element else "N/A"

        price_element = item.find("div", class_="title").strong
        price = price_element.get_text() if price_element else "N/A"

        artist_element = item.find("div", class_="subtitle")
        artist = artist_element.get_text() if artist_element else "N/A"

        format_element = item.find("div", class_="caption")
        format_info = format_element.get_text() if format_element else "N/A"

        url_element = item.find("a", class_="display-card")
        url = "https://realgroovy.co.nz" + url_element["href"] if url_element else "N/A"

        results.append((title, price, image_url, url, format_info, artist))
    return results


def script4():
    search_url = f"https://www.southbound.co.nz/?s={encoded_search_term}&post_type=product&type_aws=true&aws_id=1&aws_filter=1"
    response = requests.get(search_url)
    html_content = response.text
    soup = BeautifulSoup(html_content, "html.parser")
    is_single_product = soup.find("div", class_="et_pb_module et_pb_wc_title et_pb_wc_title_0_tb_body et_pb_bg_layout_light")

    if is_single_product:
        name_element = soup.find("div", class_="et_pb_module_inner").find("h1")
        name = name_element.get_text() if name_element else "N/A"

        image_element = soup.find("figure", class_="woocommerce-product-gallery__wrapper")
        image_url = image_element.find("img")["data-large_image"] if image_element else "N/A"

        price_element = soup.find("span", class_="woocommerce-Price-amount")
        price = price_element.get_text() if price_element else "N/A"

        view_details_url = search_url
        return [(name, price, image_url, view_details_url)]
    else:
        product_items = soup.find_all("li", class_="product")
        results = []
        for item in product_items:
            name_element = item.find("h2", class_="woocommerce-loop-product__title")
            name = name_element.get_text() if name_element else "N/A"

            image_element = item.find("img", class_="attachment-woocommerce_thumbnail")
            image_url = image_element["data-src"] if image_element else "N/A"

            price_element = item.find("span", class_="woocommerce-Price-amount")
            price = price_element.get_text() if price_element else "N/A"

            view_details_element = item.find("a", class_="woocommerce-LoopProduct-link")
            view_details_url = view_details_element["href"] if view_details_element else "N/A"
            results.append((name, price, image_url, view_details_url))
        return results


def script5():
    search_url = f"https://stolenrecordclub.com/search?q={encoded_search_term}&type=product"
    response = requests.get(search_url)
    html_content = response.text
    soup = BeautifulSoup(html_content, "html.parser")
    product_items = soup.find_all("div", class_="product-grid-item")
    results = []
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
        results.append((name, price, image_url, view_details_url))
    return results


def script6():
    search_url = f"https://vinylcountdown.co.nz/?s={encoded_search_term}&post_type=product"
    response = requests.get(search_url)
    html_content = response.text
    soup = BeautifulSoup(html_content, "html.parser")
    results = []
    product_page = soup.find("div", class_="summary entry-summary")
    if product_page:
        name_element = product_page.find("h1", class_="product_title")
        name = name_element.get_text() if name_element else "N/A"

        price_element = product_page.find("p", class_="price")
        price = price_element.get_text() if price_element else "N/A"

        view_details_url = search_url  # The current URL is the product page URL

        image_element = soup.find("div", class_="woocommerce-product-gallery__image")
        image_url = image_element["data-thumb"] if image_element else "N/A"
        results.append((name, price, image_url, view_details_url))
    else:
        product_items = soup.find_all("li", class_="ast-col-sm-12")
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
            results.append((name, price, image_url, view_details_url))
    return results


results = []

max_workers = multiprocessing.cpu_count() * 4

with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
    future_to_script = {
        executor.submit(script): name
        for name, script in [
            ('Flying Out', script1),
            ('Just for the Record', script2),
            ('Real Groovy', script3),
            ('Southbound Records', script4),
            ('Stolen Record Club', script5),
            ('Vinyl Countdown', script6)
        ]
    }

    for future in concurrent.futures.as_completed(future_to_script):
        script_name = future_to_script[future]
        try:
            output = future.result()
            if output is not None and output != "N/A":
                results.append((script_name, output))
        except Exception as e:
            print(f"Error occurred in {script_name}: {str(e)}")

sorted_results = []

for script, result in results:
    if isinstance(result, list):
        for item in result:
            if len(item) >= 4:
                price = item[1]
                if price != "N/A":
                    price_value = float(''.join(filter(str.isdigit, re.sub(r'[^\d.,]+', '', price.replace(",", "."))))) / 100
                    sorted_results.append((price_value, script, item[2], item[3]))
    elif len(result) >= 4:
        price = result[1]
        if price != "N/A":
            price_value = float(''.join(filter(str.isdigit, re.sub(r'[^\d.,]+', '', price.replace(",", "."))))) / 100
            sorted_results.append((price_value, script, result[2], result[3]))

sorted_results.sort()

if sorted_results:
    print("Ranking of stores from lowest to highest price:")
    for i, (price, script_name, image_url, view_details_url) in enumerate(sorted_results, start=1):
        print(f"{i}. {script_name}: ${price:.2f}")
        print(f"   Image URL: {image_url}")
        print(f"   View Details URL: {view_details_url}")
else:
    print("No valid results found from the scripts.")
