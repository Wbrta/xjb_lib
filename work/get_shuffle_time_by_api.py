import json
import xlwt
import requests

from bs4 import BeautifulSoup

def getHtml(url):
  headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Host": "10.198.255.203:18080"
  }
  proxies = {'http': "172.28.170.142:80"}
  html = requests.get(url, headers=headers, proxies=proxies).text
  return html

if __name__ == "__main__":
  url_template = "http://10.198.255.203:18080/api/v1/applications/%s/stages/%d/%d/taskList?offset=0&length=%d"
  apps_read = [
    ("app-id", stage_id, attemp_id, length)
  ]
  apps_write = [
    ("app-id", stage_id, attemp_id, length)
  ]

  wbk = xlwt.Workbook()
  aligment = xlwt.Alignment()
  aligment.horz = xlwt.Alignment.HORZ_CENTER
  aligment.vert = xlwt.Alignment.VERT_CENTER
  style = xlwt.XFStyle()
  style.alignment = aligment

  for app_read in apps_read:
    sheet = wbk.add_sheet(app_read[0] + "_read")
    sheet.col(0).width = 18 * 300
    sheet.col(1).width = 18 * 300
    sheet.col(2).width = 18 * 300
    sheet.col(3).width = 18 * 300
    sheet.col(4).width = 18 * 300
    sheet.col(5).width = 18 * 300
    sheet.col(6).width = 18 * 300

    sheet.write(0, 0, 'Host', style)
    sheet.write(0, 1, 'Executor Id', style)
    sheet.write(0, 2, 'Task Id', style)
    sheet.write(0, 3, 'GC Time', style)
    sheet.write(0, 4, 'Shuffle Read Time', style)
    sheet.write(0, 5, 'Shuffle Read Local Bytes', style)
    sheet.write(0, 6, 'Shuffle Read Remote Bytes', style)

    tasks = dict()
    for attemp_id in range(app_read[2] + 1):
      url = url_template % (app_read[0], app_read[1], attemp_id, app_read[3])
      print ("Crawling %s ..." % url, end="... ")
      html = getHtml(url)
      metrics = json.loads(html)

      for metric in metrics:
        host = metric['host']
        task_id = metric['index']
        executor_id = metric['executorId']
        if "taskMetrics" not in metric:
          continue
        gc_time = metric['taskMetrics']['jvmGcTime']
        shuffle_read_time = metric['taskMetrics']['shuffleReadMetrics']['fetchWaitTime']
        shuffle_read_local_bytes = metric['taskMetrics']['shuffleReadMetrics']['localBytesRead']
        shuffle_read_remote_bytes = metric['taskMetrics']['shuffleReadMetrics']['remoteBytesRead']
        tasks[task_id] = (host, executor_id, gc_time, shuffle_read_time, shuffle_read_local_bytes, shuffle_read_remote_bytes)
      print ("done")

    row = 1
    for task_id in tasks:
      task = (tasks[task_id][0], tasks[task_id][1], task_id, tasks[task_id][2], tasks[task_id][3], tasks[task_id][4], tasks[task_id][5])
      for col in range(len(task)):
        sheet.write(row, col, task[col])
      row += 1
  
  for app_write in apps_write:
    sheet = wbk.add_sheet(app_write[0] + "_write")
    sheet.col(0).width = 18 * 300
    sheet.col(1).width = 18 * 300
    sheet.col(2).width = 18 * 300
    sheet.col(3).width = 18 * 300
    sheet.col(4).width = 18 * 300
    sheet.col(5).width = 18 * 300

    sheet.write(0, 0, 'Host', style)
    sheet.write(0, 1, 'Executor Id', style)
    sheet.write(0, 2, 'Task Id', style)
    sheet.write(0, 3, 'GC Time', style)
    sheet.write(0, 4, 'Shuffle Write Time', style)
    sheet.write(0, 5, 'Shuffle Write Size', style)

    url = url_template % app_write
    print ("Crawling %s ..." % url, end="... ")
    html = getHtml(url)
    metrics = json.loads(html)

    tasks = dict()
    for metric in metrics:
      host = metric['host']
      task_id = metric['index']
      executor_id = metric['executorId']
      if "taskMetrics" not in metric:
        continue
      gc_time = metric['taskMetrics']['jvmGcTime']
      shuffle_write_time = metric['taskMetrics']['shuffleWriteMetrics']['writeTime']
      shuffle_write_size = metric['taskMetrics']['shuffleWriteMetrics']['bytesWritten']
      tasks[task_id] = (host, executor_id, gc_time, shuffle_write_time, shuffle_write_size)
    
    row = 1
    for task_id in tasks:
      task = (tasks[task_id][0], tasks[task_id][1], task_id, tasks[task_id][2], tasks[task_id][3], tasks[task_id][4])
      for col in range(len(task)):
        sheet.write(row, col, task[col])
      row += 1
    print ("done")
  wbk.save(r"C:\Users\wuxueyang1\Desktop\shuffle_times.xls")
