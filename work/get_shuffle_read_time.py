# encoding: utf-8
import re
import sys
import xlwt
import requests

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.proxy import ProxyType
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

urls = [
  "http://10.198.255.203:18080/history/app-20181022161402-0000/stages/stage/?id=2&attempt=0&task.page=%d&task.sort=Duration&task.desc=true&task.pageSize=100",
  "http://10.198.255.203:18080/history/app-20181022171458-0000/stages/stage/?id=2&attempt=0&task.page=%d&task.sort=Duration&task.desc=true&task.pageSize=100",
  "http://10.198.255.203:18080/history/app-20181022161402-0000/stages/stage/?id=2&attempt=0&task.page=%d&task.sort=Duration&task.desc=true&task.pageSize=100"
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
  # driver = webdriver.PhantomJS(executable_path=r"D:\phantomjs-2.1.1-windows\bin\phantomjs.exe", desired_capabilities=dcap)

  chrome_options = Options()
  chrome_options.add_argument("--headless")
  chrome_options.add_argument("--disable-gpu")
  driver = webdriver.Chrome(executable_path=r"D:\chromedriver_win32\chromedriver.exe", desired_capabilities=dcap, chrome_options=chrome_options)
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
    sheet.col(5).width = 18 * 300
    sheet.col(6).width = 18 * 300
    sheet.col(7).width = 18 * 300

    sheet.write(0, 0, 'Host', style)
    sheet.write(0, 1, 'Executor Id', style)
    sheet.write(0, 2, 'Task Id', style)
    sheet.write(0, 3, 'Shuffle Read Time', style)
    sheet.write(0, 4, 'Shuffle Read Time(ms)', style)
    sheet.write(0, 5, 'Shuffle Read Time(s)', style)
    sheet.write(0, 6, 'Shuffle Read Time(min)', style)
    sheet.write(0, 7, 'Shuffle Read Size', style)

    row = 1
    for i in range(1, 56):
      new_url = url % i
      print ("crawling %s..." % new_url)
      driver.get(new_url)
      import time
      time.sleep(3)
      driver.find_element_by_class_name("expand-task-assignment-timeline").click()
      time.sleep(3)
      html = driver.page_source
      bs = BeautifulSoup(html, 'lxml')
      tmp_ms, tmp_s, tmp_min = dict(), dict(), dict()
      divs = bs.find_all('div', attrs={"class": "task-assignment-timeline-content"})

      if len(divs) == 0:
        print ("Failed")
        sys.exit(1)

      for div in divs:
        data = div.attrs["data-title"]
        contents = data.split("<br>")
        task_id = contents[0].split()[1]
        shuffle_read_time = contents[5].split(":")[1].strip()

        if "ms" in shuffle_read_time:
            srt_ms = float(shuffle_read_time.replace("ms", "").strip())
            srt_s = srt_ms / 1000
            srt_min = srt_s / 60
        elif "s" in shuffle_read_time:
            srt_s = float(shuffle_read_time.replace("s", "").strip())
            srt_min = srt_s / 60
            srt_ms = srt_s * 1000
        elif "min" in shuffle_read_time:
            srt_min = float(shuffle_read_time.replace("min", "").strip())
            srt_s = srt_min * 60
            srt_ms = srt_s * 1000
        else:
            print ("Error in change format of shuffle write time.")
            sys.exit(2)

        tmp_ms[task_id] = srt_ms
        tmp_s[task_id] = srt_s
        tmp_min[task_id] = srt_min
      
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
        sheet.write(row, 3, shuffle_read_time, style)
        sheet.write(row, 4, srt_ms, style)
        sheet.write(row, 5, srt_s, style)
        sheet.write(row, 6, srt_min, style)
        sheet.write(row, 7, shuffle_read_size, style)
        row += 1
  
  wbk.save('C:\\Users\\wuxueyang1\\Desktop\\shuffle_read_time.xls')