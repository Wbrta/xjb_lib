import re
import xlwt
import time
import urllib.request as ur
from bs4 import BeautifulSoup

def getHtml(url):
  header = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36"
  req = ur.Request(url)
  req.add_header('User-Agent', header)
  req.add_header('GET', url)
  req.add_header('Host', 'ticket.lvmama.com')
  req.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8')
  req.add_header('Accept-Language', 'zh-CN,zh;q=0.9,en;q=0.8')
  html = ur.urlopen(req).read().decode('utf8')
  return html

if __name__ == "__main__":
  num = 0
  url = "http://ticket.lvmama.com/vst_front/comment/newPaginationOfComments?type=all&currentPage=%d&totalCount=59907&placeId=175649&productId=&placeIdType=PLACE&isPicture=&isBest=&isPOI=Y&isELong=N"
  
  wbk = xlwt.Workbook()
  sheet = wbk.add_sheet('sheet 1')
  sheet.write(0, 0, '评论')
  sheet.write(0, 1, '评分')
  wbk.save('/root/wm/data_set3.xls')
  
  for i in range(1, 5990):
    if i != 1:
      time.sleep(5)
    new_url = url % i
    html = getHtml(new_url)
    bs = BeautifulSoup(html, 'lxml')
    comments = bs.find_all('div', class_ = 'comment-li')
    for comment in comments:
      num += 1
      print ('Handle %d comment...' % num, end='...')
      score = int(comment.find_all('i', style = re.compile('width:*'))[0]['data-level']) * 20
      content = comment.find_all('div', class_ = 'ufeed-content')[0]
      a = content.span
      if a is not None:
        b = bs.new_tag('a')
        a.replace_with(b)
      s = content.text.strip()
      sheet.write(num, 0, s)
      sheet.write(num, 1, score)
      wbk.save('/root/wm/data_set3.xls')
      print ('OK')
