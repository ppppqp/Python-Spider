# coding=utf-8
import xlwt
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import time

workbook = xlwt.Workbook() #create excel worksheet
sheet =workbook.add_sheet("2019",cell_overwrite_ok=True)

wd = webdriver.Chrome()
wd.get("http://thesis.lib.sjtu.edu.cn/sub.asp")    # 打开百度浏览器
wd.find_element_by_name("content").send_keys("2019")
select = Select(wd.find_element_by_name('choose_key'))
select.select_by_value("year")
button = wd.find_element_by_css_selector("input[type = 'submit']")   
button.click()
pages = range(293)
row = 0
for page in pages:
  for x in range(20):
    table = wd.find_elements_by_css_selector("tr[height = '35px']")
    tr = table[x]
    tr.find_element_by_link_text("查看详情").click()
    texts = wd.find_elements_by_css_selector("td[colspan = '2']")
    col = 1
    sheet.write(row, 0, row)
    for text in texts:
      print(text.text)
      sheet.write(row,col,text.text)
      col += 1
    row += 1
    time.sleep(1)
    wd.find_element_by_link_text("返回上一页").click()
  time.sleep(1)
  pagination = wd.find_element_by_class_name("pagination")
  pagination.find_element_by_link_text('>').click()
time.sleep(1)   #等待3秒
workbook.save('data.xls')
wd.quit()   #关闭浏览器