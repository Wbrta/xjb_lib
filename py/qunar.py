import re
import time
import json
import xlwt
import urllib.request as ur

def getHtml(url):
  header = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36"
  req = ur.Request(url)
  req.add_header('User-Agent', header)
  req.add_header('GET', url)
  req.add_header('Host', 'piao.qunar.com')
  req.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8')
  req.add_header('Accept-Language', 'zh-CN,zh;q=0.9,en;q=0.8')
  html = ur.urlopen(req).read().decode('utf8')
  return html

if __name__ == "__main__":
  num = 0
  url = "http://piao.qunar.com/ticket/detailLight/sightCommentList.json?sightId=457472&index=%d&page=%d&pageSize=100&tagType=0"
  
  wbk = xlwt.Workbook()
  sheet = wbk.add_sheet('sheet 1')
  sheet.write(0, 0, '评论')
  sheet.write(0, 4, '评分')
  wbk.save('/root/wm/data_set1.xls')
  
  for i in range(1, 201):
    new_url = url % (i, i)
    html = getHtml(new_url)
    data = json.loads(html)
    comments = data['data']['commentList']
    for comment in comments:
      num += 1
      print ('Handle %d comment...' % num, end = '...')
      content = comment['content']
      score = comment['score'] * 20 # 此处为了与携程的进行统一化乘 20，如果不需要可以不乘 20
      sheet.write(num, 0, content)
      sheet.write(num, 4, score)
      wbk.save('/root/wm/data_set1.xls')
      print ('OK')
    time.sleep(5)
