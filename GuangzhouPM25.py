#!/usr/bin/env python
#-*-coding:utf-8 -*-

##################################################################################
# For fetching back the Air Quality Data and write it into Graphite on local server
# Graphite Data Definition, this is the general definition among every city
# air.city.citypoint.so2
# air.city.citypoint.no2
# air.city.citypoint.pm10
# air.city.citypoint.co
# air.city.citypoint.o38h
# air.city.citypoint.pm25
# air.city.citypoint.aqi
# air.city.citypoint.firstp
# air.city.citypoint.overp
##################################################################################

# BeautifulSoup
from bs4 import BeautifulSoup

# Selenium
from contextlib import closing
from selenium.webdriver import Firefox
from selenium.webdriver.support.ui import WebDriverWait

# For writing into Graphite
import platform
import socket
import time

# Regex
import re

# Parameters comes here 
CARBON_SERVER = '0.0.0.0'
CARBON_PORT = 2003
DELAY = 15  # secs
URL = 'http://210.72.1.216:8080/gzaqi_new/RealTimeDate.html'
CITY = 'guangzhou'

# All Points In Guangzhou City
#"天河龙洞"
#"白云山"
#"麓湖"
#"公园前"
#"荔湾西村"
#"黄沙路边站"
#"杨箕路边站"
#"荔湾芳村"
#"海珠宝岗"
#"海珠沙园"
#"海珠湖"
#"大夫山"
#"奥体中心"
#"萝岗西区"
#"黄埔文冲"
#"黄埔大沙地"
#"亚运城"
#"体育西"
#"海珠赤沙"

# regex for matching the digits.
pattern = re.compile(r'\d*')
floatpattern=re.compile(r'[\d|\.]*')

# Sending message to graphite server. 
def send_msg(message):
  print 'sending message:\n%s' % message
  sock = socket.socket()
  sock.connect((CARBON_SERVER, CARBON_PORT))
  sock.sendall(message)
  sock.close()

# Fetching data, runs each hour. 
def get_air_data():
  # Calling selenium, need linux X
  with closing(Firefox()) as browser:
    browser.get(URL)
    # Now you click corresponding button for get the page refreshed.
    browser.find_element_by_id("白云山").click()
    page_source = browser.page_source
  # Cooking soup. 
  soup = BeautifulSoup(page_source, 'html.parser')
  print soup.find('td', {'id': 'othreeA_iaqi'}).contents[0]
  # pm2.5 value would be something like xx 微克/立方米, so we need an regex for
  # matching, example: print int(pattern.match(input).group())
  PM25 = int(pattern.match(soup.find('td',{'id': 'pmtow'}).contents[0]).group())
  PM25_iaqi = int(pattern.match(soup.find('td',{'id': 'pmtow_iaqi'}).contents[0]).group())
  PM10 = int(pattern.match(soup.find('td',{'id': 'pmten'}).contents[0]).group())
  PM10_iaqi = int(pattern.match(soup.find('td',{'id': 'pmten_iaqi'}).contents[0]).group())
  SO2 = int(pattern.match(soup.find('td',{'id': 'sotwo'}).contents[0]).group())
  SO2_iaqi = int(pattern.match(soup.find('td',{'id': 'sotwo_iaqi'}).contents[0]).group())
  NO2 = int(pattern.match(soup.find('td',{'id': 'notwo'}).contents[0]).group())
  NO2_iaqi = int(pattern.match(soup.find('td',{'id': 'notwo_iaqi'}).contents[0]).group())
  # Special notice the CO would be float value
  CO = float(floatpattern.match(soup.find('td',{'id': 'co'}).contents[0]).group())
  CO_iaqi = int(pattern.match(soup.find('td',{'id': 'co_iaqi'}).contents[0]).group())
  O3 = int(pattern.match(soup.find('td',{'id': 'othree'}).contents[0]).group())
  O3_iaqi = int(pattern.match(soup.find('td',{'id': 'othree_iaqi'}).contents[0]).group())

  # Return array contains all of the data
  data = []
  data.append(PM25)
  data.append(PM25_iaqi)
  data.append(PM10)
  data.append(PM10_iaqi)
  data.append(SO2)
  data.append(SO2_iaqi)
  data.append(NO2)
  data.append(NO2_iaqi)
  data.append(CO)
  data.append(CO_iaqi)
  data.append(O3)
  data.append(O3_iaqi)
  return data
  
if __name__ == '__main__':
  airdata = get_air_data()
  for i in airdata:
    print i
