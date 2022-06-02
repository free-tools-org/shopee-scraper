# 🎉🎉🎉 Shopee Scraper 🎉🎉🎉

## What does this repo do
This repo is just a simple web scraper to scrape shopee product list written in [Python]([https://](https://www.python.org/)) with the help of [Selenium](https://www.selenium.dev/)

## Installation
1. Download selenium webdriver that match your [chrome browser version](chrome://version/) from [ChromeDriver Download](https://chromedriver.storage.googleapis.com/index.html)
2. Extract the the downloaded file to a folder/directory that is in the path environment (Debian/Ubuntu: /usr/local/bin)
3. Clone this repo
4. Install python dependencies using ```pipenv install``` or ```pip install -r requirements```
5. Edit file ```scrape_shopee_product_list.py``` and put shopee product list in any categories you need to variable ```PRODUCT_LIST_URL```.
6. Save ```scrape_shopee_product_list.py```


## Let the scraper run
Using command
```
python scrape_shopee_product_list.py
```
Wait for it to finish and create an excel file for you


