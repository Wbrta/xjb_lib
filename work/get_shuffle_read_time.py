# encoding: utf-8
import re
import xlwt
import requests

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.proxy import ProxyType
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

urls = [
  "http://10.198.255.203:18080/history/app-20181018170128-0000/stages/stage/?id=2&attempt=0&task.page=%d&task.sort=Duration&task.desc=true&task.pageSize=100"
]

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Host": "10.198.255.203:18080"
}
proxies = {'http': "172.28.170.142:80"}

def get_driver():
  proxy = webdriver.Proxy()
  proxy.proxy_type = ProxyType.MANUAL
  proxy.http_proxy = "172.28.170.142:80"

  dcap = dict(DesiredCapabilities.PHANTOMJS)
  dcap["phantomjs.page.settings.userAgent"] = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"

  proxy.add_to_capabilities(dcap)
  driver = webdriver.PhantomJS(executable_path=r"D:\phantomjs-2.1.1-windows\bin\phantomjs.exe", desired_capabilities=dcap)
  return driver

if __name__ == "__main__":
  driver = get_driver()

  wbk = xlwt.Workbook()
  aligment = xlwt.Alignment()
  aligment.horz = xlwt.Alignment.HORZ_CENTER
  aligment.vert = xlwt.Alignment.VERT_CENTER
  style = xlwt.XFStyle()
  style.alignment = aligment

  for url in urls:
    pattern = re.compile('.*\/(.*?)\/stages.*')
    result = pattern.findall(url)

    sheet = wbk.add_sheet(result[0])
    sheet.col(0).width = 18 * 300
    sheet.col(1).width = 18 * 300
    sheet.col(2).width = 18 * 300
    sheet.col(3).width = 18 * 300
    sheet.col(4).width = 18 * 300

    sheet.write(0, 0, 'Host', style)
    sheet.write(0, 1, 'Executor Id', style)
    sheet.write(0, 2, 'Task Id', style)
    sheet.write(0, 3, 'Shuffle Read Time', style)
    sheet.write(0, 4, 'Shuffle Read Size', style)

    row = 1
    for i in range(1, 56):
      new_url = url % i
      driver.get(new_url)
      html = driver.page_source
      bs = BeautifulSoup(html, 'lxml')
      
      tmp = dict()
      divs = bs.find_all('div', class_='task-assignment-timeline-content')
      for div in divs:
        data = div.attrs["data-title"]
        contents = data.split("<br>")
        task_id = contents[0].split()[1]
        shuffle_read_time = contents[5].split(":")[1].strip()
        tmp[task_id] = shuffle_read_time
      
      table = bs.find_all('table', id="task-table")[0]
      tbody = table.find_all('tbody')[0]
      trs = tbody.find_all('tr')
      for tr in trs:
        host = tr.contents[13].find_all('div', style="float: left")[0].string
        executor_id = tr.contents[11].string
        task_id = tr.contents[1].string
        shuffle_read_size = tr.contents[34].string

        sheet.write(row, 0, host, style)
        sheet.write(row, 1, executor_id, style)
        sheet.write(row, 2, task_id, style)
        sheet.write(row, 3, tmp[task_id], style)
        sheet.write(row, 4, shuffle_read_size, style)
        row += 1
  
  wbk.save('C:\\Users\\wuxueyang1\\Desktop\\shuffle_read_time.xls')