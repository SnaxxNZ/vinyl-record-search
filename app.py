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
from flask import Flask, render_template, request, url_for

app = Flask(__name__)

# Define a route to serve the image
@app.route('/images/<filename>')
def serve_image(filename):
    return app.send_static_file(f'images/{filename}')

@app.route('/', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        search_term = request.form['search_term']
        encoded_search_term = quote(search_term)

        # Script 1: Flying Out website
        def script1():
            # Construct the search URL
            search_url = f"https://flyingout.co.nz/search?q={encoded_search_term}"

            options = Options()
            options.add_argument("--headless")  # Run in headless mode, without opening a browser window

            webdriver_path = ChromeDriverManager().install()

            service = Service(webdriver_path)

            driver = webdriver.Chrome(service=service, options=options)

            try:
                # Perform the search and get the page source
                driver.get(search_url)
                html_content = driver.page_source

                # Parse the HTML content using BeautifulSoup
                soup = BeautifulSoup(html_content, "html.parser")

                # Extract product items from the page
                product_items = soup.select("div.boost-pfs-filter-product-item-inner")
                results = []

                def scrape_product(item):
                    # Extract product information from each item
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
                    image_url_relative = image_element.find("a", class_="main-img-link")[
                        "href"] if image_element else ""
                    image_url_absolute = urljoin(product_url, image_url_relative)
                    return title, price, image_url_absolute, product_url

                # Use ThreadPoolExecutor to concurrently scrape product information
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

        # Script 2: Just for the Record website
        def script2():
            # Construct the search URL
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
                    urljoin(search_url, item.select_one("div.image img")["src"]) if item.select_one(
                        "div.image") else "N/A",
                    urljoin(search_url, item.select_one("div.cart a")["href"]) if item.select_one("div.cart") else "N/A"
                )
                for item in product_items
            ]
            return results

        # Script 3: Real Groovy website
        def script3():
            # Construct the search URL
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
                image_url = img_element["src"] if img_element else ""

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

        # Script 4: Southbound Records website
        def script4():
            # Construct the search URL
            search_url = f"https://www.southbound.co.nz/?s={encoded_search_term}&post_type=product&type_aws=true&aws_id=1&aws_filter=1"
            response = requests.get(search_url)
            html_content = response.text
            soup = BeautifulSoup(html_content, "html.parser")
            is_single_product = soup.find("div",
                                          class_="et_pb_module et_pb_wc_title et_pb_wc_title_0_tb_body et_pb_bg_layout_light")

            if is_single_product:
                # If a single product is found, extract its information
                title_element = soup.find("div", class_="et_pb_module_inner").find("h1")
                title = title_element.get_text() if title_element else "N/A"

                image_element = soup.find("figure", class_="woocommerce-product-gallery__wrapper")
                image_url = image_element.find("img")["data-large_image"] if image_element else ""

                price_element = soup.find("span", class_="woocommerce-Price-amount")
                price = price_element.get_text() if price_element else "N/A"

                view_details_url = search_url
                return [(title, price, image_url, view_details_url)]
            else:
                # If multiple products are found, extract their information
                product_items = soup.find_all("li", class_="product")
                results = []
                for item in product_items:
                    title_element = item.find("h2", class_="woocommerce-loop-product__title")
                    title = title_element.get_text() if title_element else "N/A"

                    image_element = item.find("img", class_="attachment-woocommerce_thumbnail")
                    image_url = image_element["data-src"] if image_element else ""

                    price_element = item.find("span", class_="woocommerce-Price-amount")
                    price = price_element.get_text() if price_element else "N/A"

                    view_details_element = item.find("a", class_="woocommerce-LoopProduct-link")
                    view_details_url = view_details_element["href"] if view_details_element else "N/A"
                    results.append((title, price, image_url, view_details_url))
                return results

        # Script 5: Stolen Record Club website
        def script5():
            # Construct the search URL
            search_url = f"https://stolenrecordclub.com/search?q={encoded_search_term}&type=product"
            response = requests.get(search_url)
            html_content = response.text
            soup = BeautifulSoup(html_content, "html.parser")
            product_items = soup.find_all("div", class_="product-grid-item")
            results = []
            for item in product_items:
                title_element = item.find("h3", class_="product-title").find("a")
                title = title_element.get_text(strip=True) if title_element else "N/A"

                image_element = item.find("a", class_="jas-product-img-element")
                image_url = image_element["data-bgset"].split(" ")[0] if image_element else ""
                image_url = urljoin(search_url, image_url)  # Convert to absolute URL

                price_element = item.find("span", class_="price")
                price = price_element.get_text(strip=True) if price_element else "N/A"

                view_details_element = item.find("h3", class_="product-title").find("a")
                view_details_url = view_details_element["href"] if view_details_element else "N/A"
                view_details_url = urljoin(search_url, view_details_url)  # Convert to absolute URL
                results.append((title, price, image_url, view_details_url))
            return results

        # Script 6: Vinyl Countdown website
        def script6():
            # Construct the search URL
            search_url = f"https://vinylcountdown.co.nz/?s={encoded_search_term}&post_type=product"
            response = requests.get(search_url)
            html_content = response.text
            soup = BeautifulSoup(html_content, "html.parser")
            results = []
            product_page = soup.find("div", class_="summary entry-summary")
            if product_page:
                # If a single product is found, extract its information
                title_element = product_page.find("h1", class_="product_title")
                title = title_element.get_text() if title_element else "N/A"

                price_element = product_page.find("p", class_="price")
                price = price_element.get_text() if price_element else "N/A"

                view_details_url = search_url  # The current URL is the product page URL

                image_element = soup.find("div", class_="woocommerce-product-gallery__image")
                image_url = image_element["data-thumb"] if image_element else ""
                results.append((title, price, image_url, view_details_url))
            else:
                # If multiple products are found, extract their information
                product_items = soup.find_all("li", class_="ast-col-sm-12")
                for item in product_items:
                    title_element = item.find("a", class_="woocommerce-LoopProduct-link")
                    title = title_element.get_text() if title_element else "N/A"

                    image_element = item.find("img", class_="attachment-woocommerce_thumbnail")
                    image_url = image_element["src"] if image_element else ""
                    image_url = urljoin(search_url, image_url)  # Convert to absolute URL

                    price_element = item.find("span", class_="price")
                    price = price_element.get_text() if price_element else "N/A"

                    view_details_element = item.find("a", class_="woocommerce-LoopProduct-link woocommerce-loop-product__link")
                    view_details_url = view_details_element["href"] if view_details_element else "N/A"
                    view_details_url = urljoin(search_url, view_details_url)  # Convert to absolute URL
                    results.append((title, price, image_url, view_details_url))
            return results

        results = []

        # Determine the maximum number of workers based on CPU count
        max_workers = multiprocessing.cpu_count() * 4

        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Create a dictionary mapping each script to its corresponding function
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

            # Execute the scripts concurrently and store the results
            for future in concurrent.futures.as_completed(future_to_script):
                script_name = future_to_script[future]
                try:
                    output = future.result()
                    if output is not None and output != "N/A":
                        results.append((script_name, output))
                except Exception as e:
                    print(f"Error occurred in {script_name}: {str(e)}")

        sorted_results = []

        # Sort the results based on the price value
        for script, result in results:
            if isinstance(result, list):
                for item in result:
                    if len(item) >= 4:
                        price = item[1]
                        if price != "N/A":
                            price_value = float(
                                ''.join(filter(str.isdigit, re.sub(r'[^\d.,]+', '', price.replace(",", "."))))) / 100
                            sorted_results.append((price_value, script, item[0], item[2], item[3]))
            elif len(result) >= 4:
                price = result[1]
                if price != "N/A":
                    price_value = float(
                        ''.join(filter(str.isdigit, re.sub(r'[^\d.,]+', '', price.replace(",", "."))))) / 100
                    sorted_results.append((price_value, script, result[2], result[3], result[4]))

        sorted_results.sort()

        return render_template('results.html', sorted_results=sorted_results)

    return render_template('index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0')
