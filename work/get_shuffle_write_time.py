# encoding: utf-8
import re
import xlwt
import requests
from bs4 import BeautifulSoup

urls = [
    "http://10.198.255.203:18080/history/app-20181018143144-0000/stages/stage/?id=1&attempt=0&task.sort=Write+Time&task.desc=true&task.pageSize=800",  # 10台机子 remote
    "http://10.198.255.203:18080/history/app-20181018150409-0000/stages/stage/?id=1&attempt=0&task.sort=Write+Time&task.desc=true&task.pageSize=800",  # 10台机子 sort
    "http://10.198.255.203:18080/history/app-20181018170128-0000/stages/stage/?id=1&attempt=0&task.sort=Write+Time&task.desc=true&task.pageSize=800",  # 1台机子 remote
    "http://10.198.255.203:18080/history/app-20181018160224-0000/stages/stage/?id=1&attempt=0&task.sort=Write+Time&task.desc=true&task.pageSize=800"   # 1台机子 sort
]

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Host": "10.198.255.203:18080"
}
proxies = {'http': "172.28.170.142:80"}

wbk = xlwt.Workbook()
aligment = xlwt.Alignment()
aligment.horz = xlwt.Alignment.HORZ_CENTER
aligment.vert = xlwt.Alignment.VERT_CENTER
style = xlwt.XFStyle()
style.alignment = aligment

for url in urls:
    response = requests.get(url, headers=headers, proxies=proxies)
    bs = BeautifulSoup(response.text, 'lxml')

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
    sheet.write(0, 3, 'Shuffle Write Time', style)
    sheet.write(0, 4, 'Shuffle Write Size', style)

    row = 1
    table = bs.find_all('table', id="task-table")[0]
    tbody = table.find_all('tbody')[0]
    trs = tbody.find_all('tr')

    for tr in trs:
        host = tr.contents[13].find_all('div', style="float: left")[0].string
        executor_id = tr.contents[11].string
        task_id = tr.contents[1].string
        shuffle_write_time = tr.contents[33].string
        shuffle_write_size = tr.contents[34].string
        # print (hosts.string, "|", shuffle_write_time.string, "|", shuffle_write_size.string)

        if shuffle_write_time is None:
            shuffle_write_time = "0 ms"

        sheet.write(row, 0, host, style)
        sheet.write(row, 1, executor_id, style)
        sheet.write(row, 2, task_id, style)
        sheet.write(row, 3, shuffle_write_time, style)
        sheet.write(row, 4, shuffle_write_size, style)
        row += 1

wbk.save('C:\\Users\\wuxueyang1\\Desktop\\shuffle_write_time.xls')