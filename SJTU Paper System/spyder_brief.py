
# coding=utf-8
import xlwt
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import time

workbook = xlwt.Workbook() #create excel worksheet
sheet =workbook.add_sheet("2018",cell_overwrite_ok=True)

wd = webdriver.Chrome()
wd.get("http://thesis.lib.sjtu.edu.cn/sub.asp")    # 打开百度浏览器
wd.find_element_by_name("content").send_keys("2018")
select = Select(wd.find_element_by_name('choose_key'))
select.select_by_value("year")
button = wd.find_element_by_css_selector("input[type = 'submit']")   
button.click()
pages = range(293)
row = 0
for page in pages:
  table = wd.find_elements_by_css_selector("tr[height = '35px']")
  for tr in table:
    texts = tr.find_elements_by_tag_name('td')
    col = 0
    for text in texts:
      print(text.text)
      if(col == 0) :
        sheet.write(row, col, row)
      else :
        sheet.write(row,col,text.text)
      col += 1
    row += 1
  pagination = wd.find_element_by_class_name("pagination")
  pagination.find_element_by_link_text('>').click()
time.sleep(1)   #等待3秒
workbook.save('data_2018.xls')
wd.quit()   #关闭浏览器