from datetime import date, datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random
import urllib, urllib.request, sys
import ssl
import json


host = 'https://apifreelat.market.alicloudapi.com'
path = '/whapi/json/aliweather/briefforecast3days'
method = 'POST'
appcode = '89b18879b9e2487f8f74f726abf5de70'
querys = ''
bodys = {}
url = host + path
today = datetime.now()
start_date = os.environ['START_DATE']
city = os.environ['CITY']
birthday = os.environ['BIRTHDAY']

app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]

user_id = os.environ["USER_ID"]
template_id = os.environ["TEMPLATE_ID"]


def get_weather():
  bodys['lat'] = '''31.82658'''
  bodys['lon'] = '''117.23344'''
  bodys['token'] = '''443847fa1ffd4e69d929807d42c2db1b'''
  post_data = urllib.parse.urlencode(bodys).encode('utf-8')
  request = urllib.request.Request(url, post_data)
  request.add_header('Authorization', 'APPCODE ' + appcode)
  request.add_header('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8')
  ctx = ssl.create_default_context()
  ctx.check_hostname = False
  ctx.verify_mode = ssl.CERT_NONE
  response = urllib.request.urlopen(request, context=ctx)
  content = json.loads(response.read().decode('utf-8'))
  weather = content['data']['forecast'][0]
  temp=weather['tempNight']+'-'+weather['tempDay']
  print(weather)
  return weather['conditionDay'], temp

def get_count():
  delta = today - datetime.strptime(start_date, "%Y-%m-%d")
  return delta.days

def get_birthday():
  next = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d")
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  return (next - today).days

def get_words():
  words = requests.get("https://api.shadiao.pro/chp")
  if words.status_code != 200:
    return get_words()
  return 1111

def get_random_color():
  return "#%06x" % random.randint(0, 0xFFFFFF)


client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)
wea, temperature = get_weather()
data = {"weather":{"value":wea},"temperature":{"value":temperature},"love_days":{"value":get_count()},"birthday_left":{"value":get_birthday()},"words":{"value":"111111", "color":get_random_color()}}
res = wm.send_template(user_id, template_id, data)
print(res)
