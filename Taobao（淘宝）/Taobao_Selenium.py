#This source code can spider the goods on the webpage of Taobao
#In this example, we are searchin for goods with key words"shiseido(资生堂)"
#This framwork uses selenium, and can cope with Java Script
#The user need to login into Taobao for one time during the spydering process.
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from pyquery import PyQuery as pq
import pymongo
import re
import time
import xlwt
browser = webdriver.Chrome()
wait = WebDriverWait(browser,10)
client = pymongo.MongoClient('localhost',27017)
mongo = client['taobao']
def searcher():
  url = 'https://www.taobao.com/'
  browser.get(url=url)
  try:
    #Set wait time
    #Judge whether the search bar has been loaded
    input_kw = wait.until(
      EC.presence_of_element_located((By.CSS_SELECTOR, '#q'))
    )
    #Judge whether the search button has been loaded
    submit = wait.until(EC.element_to_be_clickable(
      (By.CSS_SELECTOR,'#J_TSearchForm > div.search-button > button'))
    )
    input_kw.send_keys('资生堂')#send the search key words
    submit.click()
    #Judge the page_count
    page_counts = wait.until(
      EC.presence_of_element_located(
        (By.CSS_SELECTOR,'#mainsrp-pager > div > div > div > div.total'))
    )
    parse_page()
    return page_counts.text
  except TimeoutException as e:
    print(e.args)
    return searcher()
#实现翻页
def next_page(page_number):
  try:
    
    input_page = wait.until(
      EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > div.form > input'))
    )
    # Judge whether the button has been loaded
    submit = wait.until(EC.element_to_be_clickable(
      (By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > div.form > span.btn.J_Submit'))
    )
    input_page.send_keys(page_number)
    submit.click()
    #Judeg whether the page flip is successful
    wait.until(EC.text_to_be_present_in_element(
      (By.CSS_SELECTOR,'#mainsrp-pager > div > div > div > ul > li.item.active'),str(page_number))
    )
    parse_page()
  except TimeoutException as e:
    print(e.args)
    next_page(page_number)

def parse_page():
  # get you imformation of the page in this function
  wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-itemlist .items .item')))
  html = browser.page_source
  doc = pq(html)
  items = doc('#mainsrp-itemlist .items .item').items()  #change this sentence to fit for your goal
  for item in items:
    goods = {
    #change the following to fit for your goal
      'image':item.find('.pic .img').attr('src'),
      'price':item.find('.price').text(),
      'deal':item.find('.deal-cnt').text()[:-3],
      'title':item.find('.title').text(),
      'shop':item.find('.shop').text(),
      'location':item.find('.location').text()
    }
    if goods["shop"]=="shiseido资生堂官方旗舰店":#Sift out the goods from specific shop
        print(goods)
        data_storage(goods)
#write the data into an excel worksheet

def data_storage(goods):
  global count
  global sheet
  sheet.write(count,1,goods["title"])
  sheet.write(count,2,goods["price"])
  sheet.write(count,3,goods["shop"])
  sheet.write(count,4,goods["location"])
  sheet.write(count,5,goods["deal"])
  count+=1

count=0;
workbook = xlwt.Workbook()
sheet =workbook.add_sheet("Sheet Name1",cell_overwrite_ok=True)
text = searcher()
print(text)
pages = int(re.compile('(\d+)').search(text).group(0))
print(pages)
for i in range(2,pages+1):
  next_page(i)
workbook.save('data.xls')
browser.close()
