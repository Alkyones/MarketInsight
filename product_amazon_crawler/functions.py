from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
from selenium import webdriver
import sys
from .models import AmazonDataScrapCollection, ScrapRequest



def find_price(item):

    if item.find("span", {"class": "a-color-price"}):
        price = item.find("span", {"class": "a-color-price"}).text
        return price

    if item.find("span", {"class": "a-size-base"}):
        price = item.select('span[class*="sc-price"]')[0].text
        return price

    if item.find("span", {"class": "a-color-secondary"}):
        price_text_raw = item.find("span", {"class": "a-color-secondary"})
        price = price_text_raw.text

        return price

    return None



def get_links_from_page(driver, region_data):
    xpath = region_data.navbar_xpath
    try:
        wait = WebDriverWait(driver, 15)
        find_div_partial_class_name = wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))
    except Exception as e:
        with open('/tmp/selenium_page_source.html', 'w', encoding='utf-8') as f:
            f.write(driver.page_source)
        print("[DEBUG] Full page source written to /tmp/selenium_page_source.html")
        return False
    find_a_tags = find_div_partial_class_name.find_elements(By.TAG_NAME, "a")
    links = [
        x.get_attribute("href") for x in find_a_tags if x.get_attribute("href") != None
    ]
    if len(links) == 0:
        print("No links found")
        return False
    return links


def get_scraped_data_from_links(driver, region_data, url_base, links, user, scrape_request_id):
    scraped_top_list = []
    for link in links:
        cleaned_items = []

        driver.get(link)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        xpath = region_data.link_xpath
        title = None
        try:
            wait = WebDriverWait(driver, 15)
            title_element = wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))
            title = title_element.text.strip()
        except Exception:
            title = None
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, "lxml")
        if title:
            items = soup.find_all("div", {"id": "gridItemRoot"})
            for item in items:
                spans = item.find_all("span")
                rank = spans[0].text
                description = spans[1].text
                price = find_price(item)

                link = item.find("a", {"class": "a-link-normal"})
                link = url_base + link["href"]

                cleaned_data = {
                    "rank": rank,
                    "product": description,
                    "price": price,
                    "link": link,
                }
                cleaned_items.append(cleaned_data)
            scraped_top_list.append({"category": title, "list": cleaned_items})
            driver.implicitly_wait(2)
        else:
            print("title is not found for link: ", link)

    if scraped_top_list:
        AmazonDataScrapCollection.objects.create(
            data=scraped_top_list,
            user=user,
            request=ScrapRequest.objects.get(id=scrape_request_id),
        )
        return True
    else:
        return False


def scrape_data(region_data, scrape_request_id, user):
    url_base = region_data.url
    if url_base == "https://www.amazon.co.uk":
        url = f"{url_base}/Best-Sellers/zgbs"
    else:
        url = f"{url_base}/gp/bestsellers"
    options = webdriver.ChromeOptions()
    options.binary_location = "/usr/bin/chromium-browser"
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--disable-web-security")
    options.add_argument("--allow-running-insecure-content")
    options.add_argument("--log-level=3")
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--remote-debugging-port=9222")
    options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    driver.implicitly_wait(10)
    print("Getting the data")
    link_list = get_links_from_page(driver, region_data)
    channel_layer = get_channel_layer()
    if not link_list:
        ScrapRequest.objects.filter(id=scrape_request_id).update(
            status="FAILED"
        )
        async_to_sync(channel_layer.group_send)(
            f'status_{scrape_request_id}',
            {'type': 'status_update', 'status': 'FAILED'}
        )
        return False

    scraped_data = get_scraped_data_from_links(
        driver, region_data, url_base, link_list, user, scrape_request_id
    )
    if scraped_data:
        ScrapRequest.objects.filter(id=scrape_request_id).update(
            status="COMPLETED"
        )
        async_to_sync(channel_layer.group_send)(
            f'status_{scrape_request_id}',
            {'type': 'status_update', 'status': 'COMPLETED'}
        )
        print("Data scraped successfully.")
        driver.quit()
        return True
    else:
        print("While scraping data an error occured please check the logs.")
        ScrapRequest.objects.filter(id=scrape_request_id).update(
            status="FAILED"
        )
        async_to_sync(channel_layer.group_send)(
            f'status_{scrape_request_id}',
            {'type': 'status_update', 'status': 'FAILED'}
        )
        driver.quit()
        return False
