import xlwt
import time
import json
import urllib.request as ur

def getHtml(url):
  header = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36"
  req = ur.Request(url)
  req.add_header('User-Agent', header)
  req.add_header('GET', url)
  req.add_header('Host', 'menpiao.tuniu.com')
  req.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8')
  req.add_header('Accept-Language', 'zh-CN,zh;q=0.9,en;q=0.8')
  html = ur.urlopen(req).read().decode('utf8')
  return html

if __name__ == "__main__":
  num = 0
  url = "http://menpiao.tuniu.com/tn?r=ticket/scenic/newRemarkList&currentPage=%d&scenicId%%5B%%5D=1994829&pageLimit=100"
  
  wbk = xlwt.Workbook()
  sheet = wbk.add_sheet('sheet 1')
  sheet.write(0, 0, '评论')
  sheet.write(0, 1, '评分')
  wbk.save('/root/wm/data_set2.xls')

  scores = {0: '不满意', 2: '一般', 3: '满意'}
  for i in range(1, 170):
    if i != 1:
      time.sleep(5)
    new_url = url % i
    html = getHtml(new_url)
    data = json.loads(html)
    contents = data['contents']
    for content in contents:
      num += 1
      print ('Handle %d comment...' % num, end='...')
      comment = content['compTextContent']['dataSvalue']
      value = content['compGradeContent']['dataIvalue']
      sheet.write(num, 0, comment)
      sheet.write(num, 1, scores[value])
      wbk.save('/root/wm/data_set2.xls')
      print ('OK')
