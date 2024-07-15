import time
import requests
import pandas as pd
from bs4 import BeautifulSoup
import random
from selenium import webdriver
driver = webdriver.Edge()
base_url = "https://www.Anonymous.com"
origin_url = "https://www.Anonymous.cn/"
#循环爬取所有的url,首选需要页数
final_urls = ['']
total_page = 116
flag = 1
#因为首页为0，url需要特殊处理，其他的正常添加即可
for i in range(1, total_page+1):
    if i == 1:
        continue
    else :
        base_url = base_url + str(i) + ".html"
    driver.get(base_url)
    time.sleep(1)
    html = driver.page_source
    content = BeautifulSoup(html, "html.parser")
    ResultList = content.find('div', attrs={'class':'list'}).findAll("li")
    for j in range(len(ResultList)):
        special = ResultList[0].find('a').get('href')[9:]
        final_url = origin_url + special
        final_urls.append(final_url)
        if final_urls[flag] != final_url:
            final_urls[flag] = flag
            print("fail_",flag)
        else :
            print("success_",flag)
        flag += 1
    print('page_',i)

# 分一部分跑
total_page = 232
for i in range(117, total_page+1):
    if i == 1:
        continue
    else :
        base_url = base_url + str(i) + ".html"
    driver.get(base_url)
    time.sleep(1)
    html = driver.page_source
    content = BeautifulSoup(html, "html.parser")
    ResultList = content.find('div', attrs={'class':'list'}).findAll("li")
    for j in range(len(ResultList)):
        special = ResultList[0].find('a').get('href')[9:]
        final_url = origin_url + special
        final_urls.append(final_url)
        if final_urls[flag] != final_url:
            final_urls[flag] = flag
            print("fail_",flag)
        else :
            print("success_",flag)
        flag += 1
    print('page_',i)