from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
from selenium import webdriver
import sys
from .models import AmazonDataScrapCollection, ScrapRequest
from bson import ObjectId


def findPrice(item):

    if item.find("span", {"class": "a-color-price"}):
        price = item.find("span", {"class": "a-color-price"}).text
        return price

    if item.find("span", {"class": "a-size-base"}):
        price = item.select('span[class*="sc-price"]')[0].text
        return price

    if item.find("span", {"class": "a-color-secondary"}):
        priceTextsRaw = item.find("span", {"class": "a-color-secondary"})
        price = priceTextsRaw.text

        return price

    return None


def getLinksFromList(data):
    links = []
    for el in data:
        link = el.find("a")
        if link:
            links.append(link["href"])
    return links or False


def getLinksFromPage(driver, regionData):
    xpath = regionData.navbar_xpath
    try:
        wait = WebDriverWait(driver, 15)
        findDivPartialClassName = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
    except Exception:
        print("No links found (timeout)")
        return False
    findAtags = findDivPartialClassName.find_elements(By.TAG_NAME, "a")
    links = [
        x.get_attribute("href") for x in findAtags if x.get_attribute("href") != None
    ]
    print("Links found: ", len(links), " links: ", links)
    if len(links) == 0:
        print("No links found")
        return False
    return links


def getScrapedDataFromLinks(driver, regionData, url_base, links, user, scrape_request_id):
    scrapedTopList = []
    for link in links:
        cleaned_items = []

        driver.get(link)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        xpath = regionData.link_xpath
        title = None
        try:
            wait = WebDriverWait(driver, 15)
            title_element = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
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
                price = findPrice(item)

                link = item.find("a", {"class": "a-link-normal"})
                link = url_base + link["href"]

                cleaned_data = {
                    "rank": rank,
                    "product": description,
                    "price": price,
                    "link": link,
                }
                cleaned_items.append(cleaned_data)
            scrapedTopList.append({"category": title, "list": cleaned_items})
            driver.implicitly_wait(2)
        else:
            print(title)
            print("title is not found for link: ", link)
        

    AmazonDataScrapCollection.objects.create(
        data=scrapedTopList,
        user=user,
        request=ScrapRequest.objects.get(_id=ObjectId(scrape_request_id)),
    )
    return True


def scrapeData(region_data, scrape_request_id, user):
    url_base = region_data.url
    if url_base == "https://www.amazon.co.uk":
        url = f"{url_base}/Best-Sellers/zgbs"
    else:
        url = f"{url_base}/gp/bestsellers"
    options = webdriver.ChromeOptions()
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--disable-web-security")
    options.add_argument("--allow-running-insecure-content")
    options.add_argument("--log-level=3")
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    driver.implicitly_wait(10)
    print("Getting the data")
    link_list = getLinksFromPage(driver, region_data)
    if not link_list:
        ScrapRequest.objects.filter(_id=ObjectId(scrape_request_id)).update(
            status="FAILED"
        )
        sys.exit()

    scraped_data = getScrapedDataFromLinks(
        driver, region_data, url_base, link_list, user, scrape_request_id
    )
    if scraped_data:
        ScrapRequest.objects.filter(_id=ObjectId(scrape_request_id)).update(
            status="COMPLETED"
        )
        print("Data scraped successfully.")
        driver.quit()
        return True
    else:
        print("While scraping data an error occured please check the logs.")
        ScrapRequest.objects.filter(_id=ObjectId(scrape_request_id)).update(
            status="FAILED"
        )
        driver.quit()
        return False
