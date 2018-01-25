# coding:utf-8

import psycopg2
import requests
import re
from bs4 import BeautifulSoup


#头部信息，传入headers防止服务器拒绝request
headers = {
    'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
    'Cookie' : 'JSESSIONID=abcJiJR0Vt0Xyf-VF95_v; userLikesIdTemp=1510659399198; Hm_lvt_dc888321efaa2c58ab4aceeed619e820=1510629996,1510653431; Hm_lpvt_dc888321efaa2c58ab4aceeed619e820=1510712671; _ga=GA1.2.2096116624.1510630000; _gid=GA1.2.1608336467.1510630000; Hm_lvt_2e44bf94e67d57ced8420d8af730dd64=1510630000,1510653432; Hm_lpvt_2e44bf94e67d57ced8420d8af730dd64=1510733476'
}

#创建对pg服务器的连接
conn = psycopg2.connect(database="datacloud", user="postgres", password="root", host="39.106.127.31", port="5432")
cur = conn.cursor()



#返回数据库中医生的id，根据此id获取医生详细页面的url
def get_doctors_id():
    cur.execute("SELECT doctors_id FROM doctors_info WHERE work_on = '错误信息' ORDER BY doctors_id ASC")
    rows = cur.fetchall()
    return rows

#获取医生的患者就诊经历（次数），擅长领域，职业经历
def get_doctors_detail(id):
    url = 'http://yyk.39.net/doctor/'
    url = url + id
    wb_data = requests.get(url,headers=headers)
    soup = BeautifulSoup(wb_data.text,'lxml')
    #experiences = soup.select('#practiceExperience > div > div:nth-of-type(2)')
    #works       = soup.select('body > div.doc-head > div.doc-detail.doc-wrap.clearfix > dl > dd > div')
    works        = soup.select('body > div.doc-head > div.doc-detail.doc-wrap.clearfix > dl:nth-of-type(2) > dd:nth-of-type(4)')
    print(works)
    #comments    = soup.select('body > div.doc-con > div > div.doc-left > div > div > div.doc-cm-filter.clearfix > div.tag.tag-hide > ul > li > a')
    if works == []:
        works = soup.select('body > div.doc-head > div.doc-detail.doc-wrap.clearfix > dl > dd')
    for work in works:
        searchObj_work = re.search(r'擅长领域(.*)',work.get_text())
        if searchObj_work:
            work_detail = searchObj_work.group()
    '''        
    try:
        work_detail
    except NameError:
        work_detail = '错误信息'
    '''

    cur.execute("UPDATE doctors_info SET work_on ='%s' WHERE doctors_id =%s" % (work_detail, id))
    conn.commit()
    print("编号为%s的医生信息已补全" % str(id))


rows = get_doctors_id()
for i in rows:
    get_doctors_detail(str(i[0]))
#get_doctors_detail(str(6191))
conn.close()

