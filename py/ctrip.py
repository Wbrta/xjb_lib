import os
import re
import time
import xlwt
import random
import urllib.request as ur
from bs4 import BeautifulSoup

def getHtml(url):
  header = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36"
  req = ur.Request(url)
  req.add_header('User-Agent', header)
  req.add_header('GET', url)
  req.add_header('Host', 'you.ctrip.com')
  req.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8')
  req.add_header('Accept-Language', 'zh-CN,zh;q=0.9,en;q=0.8')
  html = ur.urlopen(req).read().decode('utf8')
  return html

if __name__ == "__main__":
  url = "http://you.ctrip.com/destinationsite/TTDSecond/SharedView/AsynCommentView?poiID=13412802&districtId=2&districtEName=ShanghaiDisneyResort&pagenow=%d&order=3.0&star=0.0&tourist=0.0&resourceId=1412255&resourcetype=2"
  
  wbk = xlwt.Workbook()
  sheet = wbk.add_sheet('sheet 1')
  sheet.write(0, 0, '评论')
  sheet.write(0, 1, '景色')
  sheet.write(0, 2, '趣味')
  sheet.write(0, 3, '性价比')
  sheet.write(0, 4, '评分')
  wbk.save('/root/wm/data_set.xls')

  num = 0
  for i in range (1, 2001):
    new_url = url % i
    html = getHtml(new_url)
    bs = BeautifulSoup(html, 'lxml')
    
    comments = bs.find_all('div', class_='comment_single')
    for comment in comments:
      num += 1
      print ('Handle %d comment...' % num, end='...')
      content = comment.find_all('span', class_='heightbox')[0].string
      sheet.write(num, 0, content)
      grade = comment.find_all('span', style=re.compile('width:*'))[0]['style'].replace('%;', '').split(':')
      if grade[0] == 'width':
        sheet.write(num, 4, int(grade[1]))
      scores_ = comment.find_all('span', class_='sblockline')
      if scores_ == []:
        print ('OK')
        continue
      scores = [s.strip().split('：') for s in scores_[0].string.strip().split('\u2003')]
      for score in scores:
        if score[0] == '景色':
          sheet.write(num, 1, int(score[1]))
        elif score[0] == '趣味':
          sheet.write(num, 2, int(score[1]))
        elif score[0] == '性价比':
          sheet.write(num, 3, int(score[1]))
      wbk.save('/root/wm/data_set.xls')
      print ('OK')
    time.sleep(5) 
