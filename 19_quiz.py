from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from bs4 import BeautifulSoup

options = webdriver.ChromeOptions()
options.headless = True
options.add_argument("window-size=1920x1080")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36")

browser = webdriver.Chrome(options=options)
browser.maximize_window()

url = "https://www.daum.net"
browser.get(url)

keyword = "송파 아이파크"
inputKeyword = browser.find_element(By.ID, "q")
inputKeyword.send_keys(keyword)
inputKeyword.send_keys(Keys.ENTER)

soup = BeautifulSoup(browser.page_source, "lxml")
tradeTable = soup.find("div", attrs={"class":["wrap_tbl", "tbl_trade"]})
titles = tradeTable.find("thead").find_all("th")
trades = tradeTable.find("tbody").find_all("tr")

for idx, trade in enumerate(trades):

    tradeType = trade.find("td", attrs={"class":"col1"}).find("div", attrs={"class":"txt_ac"}).get_text()
    area = trade.find("td", attrs={"class":"col2"}).find("div", attrs={"class":"txt_ac"}).get_text()
    price = trade.find("td", attrs={"class":"col3"}).find("div", attrs={"class":"txt_ac"}).get_text()
    aptComplex = trade.find("td", attrs={"class":"col4"}).find("div", attrs={"class":"txt_ac"}).get_text()
    floor = trade.find("td", attrs={"class":"col5"}).find("div", attrs={"class":"txt_ac"}).get_text()

    print(f"======== 매물 {idx} =========")
    print(f"{titles[0].get_text()} : {tradeType}")
    print(f"{titles[1].get_text()} : {area}")
    print(f"{titles[2].get_text()} : {price}")
    print(f"{titles[3].get_text()} : {aptComplex}")
    print(f"{titles[4].get_text()} : {floor}")



