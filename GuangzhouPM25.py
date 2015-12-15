#!/usr/bin/env python

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

# Parameters comes here 
CARBON_SERVER = '0.0.0.0'
CARBON_PORT = 2003
DELAY = 15  # secs
URL = 'http://210.72.1.216:8080/gzaqi_new/DataList2.html?EPNAME=%E6%B5%B7%E7%8F%A0%E6%B9%96'
CITY = 'guangzhou'

# For sending message to graphite server. 
def send_msg(message):
  print 'sending message:\n%s' % message
  sock = socket.socket()
  sock.connect((CARBON_SERVER, CARBON_PORT))
  sock.sendall(message)
  sock.close()

# For fetching data, runs each hour. 
def get_air_data():
  # Calling selenium, need linux X
  with closing(Firefox()) as browser:
    browser.get(URL)
    page_source = browser.page_source
  # Cooking soup. 
  soup = BeautifulSoup(page_source, 'html.parser')
  table = soup.find('table', {'class': 'headTable'})

   

# def get_loadavgs():
#     with open('/proc/loadavg') as f:
#         return f.read().strip().split()[:3]
#
# with closing(Firefox()) as browser:
#   browser.get(URL)
#   page_source = browser.page_source
# 
# soup = BeautifulSoup(page_source, 'html.parser')
# 
# table = soup.find('table', {'class': 'headTable'})
# for td in table.tbody.tr:
#   print td.contents[0]


