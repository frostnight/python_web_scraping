import requests
import re
from bs4 import BeautifulSoup

headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36"}


for i in range(1, 6):
    print("페이지 : ", i)
    url = f"https://www.coupang.com/np/search?q=%EB%85%B8%ED%8A%B8%EB%B6%81&channel=user&component=&eventCategory=SRP&trcid=&traid=&sorter=scoreDesc&minPrice=&maxPrice=&priceRange=&filterType=&listSize=36&filter=&isPriceRange=false&brand=&offerCondition=&rating=0&page={i}&rocketAll=false&searchIndexingToken=1=6&backgroundColor="

    res = requests.get(url, headers=headers)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "lxml")

    items = soup.find_all("li", attrs={"class":re.compile("^search-product")})

    for item in items:

        # 광고 제품은 제외
        ad_badge = item.find("span", attrs={"class":"ad-badge-text"})
        if ad_badge:
            continue

        name = item.find("div", attrs={"class", "name"}).get_text() # 제품
        # 애플 제품 제외
        if "Apple" in name:
            continue

        price = item.find("strong", attrs={"class":"price-value"}).get_text() # 가격
        # 리뷰 100개 이상, 평점 4.5 이상 되는 것만 조회
        rate = item.find("em", attrs={"class":"rating"}) # 평점
        if rate:
            rate = rate.get_text()
        else:
            continue

        rate_count = item.find("span", attrs={"class":"rating-total-count"}) # 평점 수
        if rate_count:
            rate_count = rate_count.get_text()[1:-1]
        else:
            continue

        link = item.find("a", attrs={"class":"search-product-link"})["href"]


        if float(rate) >= 4.5 and int(rate_count) >= 100:
            #print(name, price, rate, rate_count)
            print(f"제품명 : {name}")
            print(f"가격 : {price}")
            print(f"평점 : {rate}점 ({rate_count}개)")
            print(f"바로가기 : https://www.coupang.com{link}")
            print("-"*100) # 줄긋기
