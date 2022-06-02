from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import selenium.common.exceptions as exception
from urllib.parse import urlparse, parse_qs, urlencode
import pandas as pd

PRODUCT_LIST_URL = "https://shopee.co.th/%E0%B9%80%E0%B8%84%E0%B8%A3%E0%B8%B7%E0%B9%88%E0%B8%AD%E0%B8%87%E0%B9%80%E0%B8%82%E0%B8%B5%E0%B8%A2%E0%B8%99-col.1017369?facet=11045875&page=0" # ปากกา

driver = None
wait = None

def set_url_query_string(url, key, value):
    url_parsed = urlparse(url)
    query = parse_qs(url_parsed.query)
    query[key] = value
    query = urlencode(query, doseq=True)
    print("query:", query)
    url_parsed = url_parsed._replace(query=query)
    updated_url = url_parsed.geturl()
    print("updated_url:", updated_url)
    return updated_url


def wait_for_page_load():
    try:
        wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, "button.shopee-icon-button.shopee-icon-button--right")))
        return True
    except exception.TimeoutException as e:
        return False


# grab list of product links
if __name__ == "__main__":
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 10)
    product_list_index = 0
    list_of_products_url = set_url_query_string(url=PRODUCT_LIST_URL,key="page", value=product_list_index)

    driver.get(list_of_products_url)
    has_more_pages = wait_for_page_load()
    product_links = []
    while has_more_pages:
        driver.implicitly_wait(5)
        product_elements = driver.find_elements(
            by=By.CSS_SELECTOR,
            value='div[data-sqe=\"item\"]')

        # Grab product links
        for product_idx, product_element in enumerate(product_elements):
            current_element = driver.find_element(
                by=By.CSS_SELECTOR,
                value=f"div[data-sqe=\"item\"]:nth-child({product_idx + 1})")
            driver.execute_script(
                "arguments[0].scrollIntoView();", current_element)
            product_link = current_element.find_element(
                by=By.CSS_SELECTOR, value='a').get_attribute('href')

            product_description = current_element.find_element(
              by=By.CSS_SELECTOR,
              value='a>div>div>div:nth-child(n+2)>div:first-child>div:first-child'
            ).text

            product_price = current_element.find_element(
              by=By.CSS_SELECTOR,
              value='a>div>div>div:nth-child(n+2)>div:nth-child(n+2)'
            ).text

            prices = product_price.split('\n')
            price_before_discount = prices[0]
            if len(prices) > 0:
              product_price = prices[-1]

            sold = current_element.find_element(
              by=By.CSS_SELECTOR,
              value='a>div>div>div:nth-child(n+2)>div:nth-child(n+3)>div:nth-child(n+2)'
            ).text

            location = current_element.find_element(
              by=By.CSS_SELECTOR,
              value='a>div>div>div:nth-child(n+2)>div:nth-child(n+4)'
            ).text

            print("\n")
            print(product_description)
            print(f"---[{price_before_discount}]\t[{product_price}]")
            print(f"sold: {sold}")
            print(f"location: {location}")


            product_links.append({
              "ชื่อสินค้า": product_description,
              "ราคา": price_before_discount,
              "ราคาปัจจุบัน": product_price,
              "ยอดขาย": sold,
              "ลิงค์":product_link,
              "location": location,
              })

        # Go to next page
        product_list_index += 1
        list_of_products_url = set_url_query_string(url=PRODUCT_LIST_URL,key="page", value=product_list_index)
        driver.get(list_of_products_url)
        has_more_pages = wait_for_page_load()

    print(len(product_links))

    df = pd.DataFrame(product_links)
    print(df)
    df.to_excel("product_list.xlsx", index=False)
    driver.quit()
