#-*- coding=utf8 -*-
import os
import urllib
from bs4 import BeautifulSoup

while True:
  #word = "leave"
  word = input("Please input word: ")
  if word == 'Q':
      break

  url = "http://dict.youdao.com/w/" + word + "/"
  html = urllib.request.urlopen(url).read()

  soup = BeautifulSoup(html, "lxml")
  results = soup.find_all("div", class_="trans-container")[0].find_all("li")

  print ("======================================")

  for result in results:
    res = str(result)
    res = res.replace("<li>", "").replace("</li>", "")
    print (res)
  
  tmp = input("Press enter to continue...")
  os.system("cls")
