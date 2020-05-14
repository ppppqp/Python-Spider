from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import urllib.request
import sqlite3
#import threading
import os
import datetime
from selenium.webdriver.common.keys import Keys
import time
import xlwt
class MySpider:
    headers={
                "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3088.3 Safari/537.36"
    }

    def startUp(self, url):
        chrome_options=Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        self.driver=webdriver.Chrome(chrome_options=chrome_options)
        self.driver.maximize_window()
        print("started")
        #self.threads=[]
        self.No=0

        try:
            self.workbook = xlwt.Workbook()
            sheet = self.workbook.add_sheet("Sheet Name1",cell_overwrite_ok=True)#cell_overwrite_ok=True
            sheet.write(0,0,"Title")
            sheet.write(0,1,"number")
            sheet.write(0,2,"Price")
        except Exception as err:
            print(err)

    def closeUp(self):
        try:
            self.workbook.save('Excel_test1.xls')
        except Exception as err:
            print(err)

            
    def find_url(self):
        try:
            items=self.driver.find_element_by_xpath("//div[@class='list-inner']")
            for item in items:
                try:
                    #href=items.find_element_by_xpath("a[@class='pro-info']/@href")
                    #url=start_url+href
                    title=item.driver.find_element_by_xpath(".//span[@class='pro-name']/text()")#.extract_first()
                    number=item.driver.find_element_by_xpath(".//span[@class='price1' and position()=2]/text()")#.extract_first()
                    price=item.driver.find_element_by_xpath(".//span[@class='price1' and position()=1]/text()")
                    print(title)
                    item.click()
                    self.spide()
                    nextpage=self.driver.find_element_by_xpath("//a[@class='oran_pg_np'")
                    nextpage.click()
                    self.find_url()
                except Exception as err:
                    print(err)
        except Exception as err:
            print(err)


    def spide(self):
        try:
            print(self.driver.current_url)
            box=self.driver.find_element_by_xpath("//div[@class='attr-box']/tabel/tbody")
            
            tr_1=box.driver.find_element_by_xpath("/tr[position()=1]")
            tr_2=box.driver.find_element_by_xpath("/tr[position()=2]")
            tr_3=box.driver.find_element_by_xpath("/tr[position()=3]")
            tds=tr_1.driver.find_element_by_xpath("/td")
            for td in tds:
                print(td.text)
                count+=1
            td=tr_2.driver.find_element_by_xpath("/td")
            for td in tds:
                print(td.text)
                count+=1
            tds=tr_3.driver.find_element_by_xpath("/td")
            for td in tds:
                print(td.text)
                count+=1
            
        except Exception as err:
            print(err)
    def execute(self,url):
        self.startUp(url)
        self.find_url()
        self.closeUp()
        
url="https://www.ctfmall.com/c/all/all/?top=20&page=1" 
spider=MySpider()       
spider.execute(url)