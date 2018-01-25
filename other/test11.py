from bs4 import BeautifulSoup
import requests
import time
import psycopg2
import re

#头部信息,传入headers防止服务器拒绝request
headers = {
    'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
    'Cookie' : 'tma=202198739.25123171.1509871124928.1509871124928.1509871124928.1; tmd=1.202198739.25123171.1509871124928.; fingerprint=8831389cdecd842dbd19af635b0dbee9; bfd_g=a7e5345bc8ec1f3e000021c4000015bf59f3458a; Hm_lvt_ab2e5965345c61109c5e97c34de8026a=1509934663; Hm_lpvt_ab2e5965345c61109c5e97c34de8026a=1509934663; _39wt_pk_cookie=910cf848042252c2c15438363ee49842-990358911; _39wt_session_cookie=e73623077e8742d0809704ed0ae5a1501630260551; _39wt_last_session_cookie=e73623077e8742d0809704ed0ae5a1501630260551; _39wt_session_refer_cookie=https%253A%252F%252Fwww.google.com.hk%252F; _39wt_last_visit_time_cookie=1509934666599; area_info=CN110000|%D6%D0%B9%FA|%B1%B1%BE%A9|-|%B5%E7%D0%C5; JSESSIONID=abceGfXojuT8haavPhp_v; userLikesIdTemp=1509934693756; Hm_lvt_dc888321efaa2c58ab4aceeed619e820=1509934669; Hm_lpvt_dc888321efaa2c58ab4aceeed619e820=1510208538; _ga=GA1.2.1477589345.1509871125; _gid=GA1.2.774492229.1510208539; Hm_lvt_2e44bf94e67d57ced8420d8af730dd64=1509934669; Hm_lpvt_2e44bf94e67d57ced8420d8af730dd64=1510212906'
}

# 配置pg连接
conn = psycopg2.connect(database="datacloud", user="postgre", password="106524", host="127.0.0.1", port="5432")
cur = conn.cursor()

url = 'http://yyk.39.net/'

cur.execute("SELECT DISTINCT(hospital_level) FROM doctors_info WHERE hospatil='%s'" % '锦州市中医医院')
rows = cur.fetchall()
print(rows[0][0])
