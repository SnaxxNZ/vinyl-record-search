# Vinyl Record Search and Scraping

This project is a Flask-based web application that allows users to search for vinyl records and scrapes data from multiple websites related to vinyl records. The application provides a user-friendly interface for searching and displaying the scraped data.

## Features

- Search for vinyl records across multiple websites
- Scrapes data from the following websites:
  - [Flying Out](https://flyingout.co.nz)
  - [Just for the Record](http://www.justfortherecord.co.nz)
  - [Real Groovy](https://realgroovy.co.nz)
  - [Southbound Records](https://www.southbound.co.nz)
  - [Stolen Record Club](https://stolenrecordclub.com)
  - [Vinyl Countdown](https://vinylcountdown.co.nz)
- Uses concurrent programming techniques for efficient scraping
- Renders search results in a user-friendly format

## Prerequisites

- Python 3.x
- Flask
- BeautifulSoup
- Selenium
- Chrome WebDriver
- Requests
- Concurrent Futures

## Installation

1. Clone the repository:

   ```shell
   git clone https://github.com/your-username/vinyl-record-search.git
   ```

2. Change into the project directory:

   ```shell
   cd vinyl-record-search
   ```

3. Install the required dependencies using pip:

   ```shell
   pip install -r requirements.txt
   ```

4. Download and install the Chrome WebDriver from the following link: [ChromeDriver](https://sites.google.com/a/chromium.org/chromedriver/downloads)

   Make sure to download the version compatible with your Chrome browser.
   Note: The application will automatically install the Chrome WebDriver to `%userprofile%/.wdm/`.

5. Run the application:

   ```shell
   python app.py
   ```

6. Open your web browser and access the application at [http://localhost:5000](http://localhost:5000)

### Precompiled

Alternatively, you can use the precompiled version of the application. The precompiled version is available as a stand-alone executable file. Follow these steps to use the precompiled version:

1. Download the precompiled executable for your operating system from the [Releases](/releases) page.
2. Run the executable file.
3. Open your web browser and access the application at [http://localhost:5000](http://localhost:5000)

## Usage

1. Enter a search term in the search field on the home page.
2. Click the "Search" button.
3. The application will scrape data from multiple websites and display the results on a separate page.
4. The search results will include the title, price, image, and product URL for each record found.
5. Click on the product URL to view more details about a specific record.

## Contributing

Contributions to this project are welcome. Feel free to open issues and submit pull requests to contribute new features, improvements, or bug fixes.

## License

This project is licensed under the [MIT License](LICENSE).

---
```
