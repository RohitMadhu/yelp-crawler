from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq
from lxml.html import fromstring
import requests

import csv

import random
import re
import time
import sys
from itertools import cycle
import traceback

def printProgressBar (iteration, total, decimals = 1, length = 45, fill = '█'):
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % ("Progress:", bar, percent, "Complete"), end = '\r')
    if iteration == total: 
        print()

def restaurantInfoCrawler (searchRange: int):
    AttributeErrorNum = 0

    with open('yelp.csv', 'w', newline='') as of:
        f = csv.writer(of, delimiter=',')
        f.writerow(["restaurant_title, restaurant_phone, restaurant_addr, restaurant_price, restaurant_category"])
    user_agents = [
        'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
        'Opera/9.25 (Windows NT 5.1; U; en)',
        'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
        'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
        'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.142 Safari/535.19',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:11.0) Gecko/20100101 Firefox/11.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:8.0.1) Gecko/20100101 Firefox/8.0.1',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.151 Safari/535.19']
    for i in range(0, searchRange, 30):
        headers = {"User-Agent": random.choice(user_agents)}
        url = 'https://www.yelp.com/search?find_desc=Restaurants&find_loc=Washington+DC&start=' + str(i)
        response=requests.get(url,headers=headers)
        soup=bs(response.content,'lxml')
        for item in soup.select('[class*=container]'):
            try:
                if item.find('h4'):
                    restaurant_title = item.find('h4').get_text()
                    restaurant_title = re.sub(r'^[\d.\s]+', '', restaurant_title)
                    restaurant_phone = item.select_one('[class*=secondaryAttributes]').get_text()[:14]
                    restaurant_addr = item.select_one('[class*="secondaryAttributes"]').get_text()[14:]
                    #restaurant_price = item.select_one('[class*=priceRange]').get_text()
                    pr = item.select_one('[class*="priceRange"]')
                    restaurant_price = pr.get_text(strip=True) if pr else '-'
                    restaurant_category = item.select_one('[class*=priceCategory]').get_text()
                    restaurant_category = re.sub(r'[^\w]', ' ', restaurant_category)
                    print(restaurant_title)
                    print(restaurant_phone)
                    print(restaurant_addr)
                    print(restaurant_price)
                    print(restaurant_category)
                    print('------------------')
                    with open('yelp.csv', 'a+', newline='') as of:
                        f = csv.writer(of, delimiter=',')
                        f.writerow([restaurant_title, restaurant_phone, restaurant_addr, restaurant_price, restaurant_category])
                            
            except AttributeError:
                AttributeErrorNum += 1
                continue
        printProgressBar(i, searchRange)
        random_int = random.randint(2, 10)
        time.sleep(random_int)
    print('\nDone! Attribute Error Occurs ' + str(AttributeErrorNum) + ' Times')

if __name__ == '__main__':
    ### DC
    print('Yelp Crawler starts... (DC Version)')
    invalidInput = True
    while invalidInput:
        searchRange = input('Please input search range(A num indicates how many yelp entries you want to get): ')
        if searchRange.isdigit():
            invalidInput = False
        else:
            print('You input is not a Num...\nTry again')
    restaurantInfoCrawler(int(searchRange))
