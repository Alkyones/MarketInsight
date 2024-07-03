from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
from selenium import webdriver
import  sys
from .models import AmazonDataScrapCollection, ScrapRequest
from bson import ObjectId

url_bases = {
    "au": {"country": "Australia", "url": "https://www.amazon.com.au"},
    "ae": {"country": "United Arab Emirates", "url": "https://www.amazon.ae"},
    "br": {"country": "Brazil", "url": "https://www.amazon.com.br"},
    "ca": {"country": "Canada", "url": "https://www.amazon.ca"},
    "cn": {"country": "China", "url": "https://www.amazon.cn"},
    "de": {"country": "Germany", "url": "https://www.amazon.de"},
    "es": {"country": "Spain", "url": "https://www.amazon.es"},
    "fr": {"country": "France", "url": "https://www.amazon.fr"},
    "in": {"country": "India", "url": "https://www.amazon.in"},
    "it": {"country": "Italy", "url": "https://www.amazon.it"},
    "jp": {"country": "Japan", "url": "https://www.amazon.co.jp"},
    "mx": {"country": "Mexico", "url": "https://www.amazon.com.mx"},
    "sg": {"country": "Singapore", "url": "https://www.amazon.sg"},
    "tr": {"country": "Turkey", "url": "https://www.amazon.com.tr"},
    "uk": {"country": "United Kingdom", "url": "https://www.amazon.co.uk"},
    "us": {"country": "United States", "url": "https://www.amazon.com"},
}



def findPrice(item):

    if(item.find("span", {"class": "a-color-price"})):
        price = item.find("span", {"class": "a-color-price"}).text
        return price
    
    if(item.find("span", {"class": "a-size-base"})):
        price = item.select('span[class*="sc-price"]')[0].text
        return price
    
    if(item.find("span", {"class": "a-color-secondary"})):
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

def getLinksFromPage(driver): 
    findDivPartialClassName = driver.find_element("xpath" , " /html/body/div[1]/div[1]/div[2]/div/div/div/div[2]/div/div[2]/div/div/div[2]")
    findAtags = findDivPartialClassName.find_elements(By.TAG_NAME, "a")
    links = [x.get_attribute("href")  for x in findAtags if x.get_attribute("href") != None]
    if len(links) == 0:
        links = False
    return links

def getScrapedDataFromLinks(driver, url_base, links):
    scrapedTopList = []
    for link in links:
        cleanedItems = []

        driver.get(link)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

        page_source = driver.page_source
        soup = BeautifulSoup(page_source, "lxml")

        xpath_list = [
            "/html/body/div[1]/div[2]/div/div/div[2]/div/div/div[2]/div[1]/span",
            "/html/body/div[1]/div[1]/div[2]/div/div/div/div[2]/div/div[2]/div/div/div[2]/div[1]/span",
        ]

        title = None

        for xpath in xpath_list:
            try:
                title_element = driver.find_element("xpath", xpath)
                title = title_element.text
                break
            except:
                pass

        if title:
            print("title: " + title)
            items = soup.find_all("div", {"id": "gridItemRoot"})
            for item in items:
                spans = item.find_all("span")
                rank = spans[0].text
                description = spans[1].text
                price = findPrice(item)

                link = item.find("a", {"class": "a-link-normal"})
                link = url_base + link["href"]

                cleanedData = {
                    "rank": rank,
                    "product": description,
                    "price": price,
                    "link": link,
                }
                cleanedItems.append(cleanedData)
            scrapedTopList.append({
                "category": title,
                "list": cleanedItems
            })
            time.sleep(4)
        else:
            print(title)
            print("title is not found for link: ", link)

       
    AmazonDataScrapCollection.objects.create(data=scrapedTopList)
    return True


def scrapeData(url_base, scrape_request_id):
    if url_base == "https://www.amazon.co.uk":
        url = f"{url_base}/Best-Sellers/zgbs"
    else:
        url = f"{url_base}/gp/bestsellers"
    print(url)
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument('suppress_console_output')
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    driver.implicitly_wait(2)
    print("Getting the data")
    linksList = getLinksFromPage(driver)
    if not linksList:
        print("No links found")
        sys.exit()

    scrapedData = getScrapedDataFromLinks(driver, url_base, linksList)
    if scrapedData:
        ScrapRequest.objects.filter(_id=ObjectId(scrape_request_id)).update(status='COMPLETED')
        print("Data scraped successfully.")
    else:
        print("While scraping data an error occured please check the logs.")
    