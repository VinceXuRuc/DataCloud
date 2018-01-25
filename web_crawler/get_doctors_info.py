

from bs4 import BeautifulSoup
import requests
import time
import psycopg2
import re

#头部信息，传入headers防止服务器拒绝request
headers = {
    'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
    'Cookie' : 'tma=202198739.25123171.1509871124928.1509871124928.1509871124928.1; tmd=1.202198739.25123171.1509871124928.; fingerprint=8831389cdecd842dbd19af635b0dbee9; bfd_g=a7e5345bc8ec1f3e000021c4000015bf59f3458a; Hm_lvt_ab2e5965345c61109c5e97c34de8026a=1509934663; Hm_lpvt_ab2e5965345c61109c5e97c34de8026a=1509934663; _39wt_pk_cookie=910cf848042252c2c15438363ee49842-990358911; _39wt_session_cookie=e73623077e8742d0809704ed0ae5a1501630260551; _39wt_last_session_cookie=e73623077e8742d0809704ed0ae5a1501630260551; _39wt_session_refer_cookie=https%253A%252F%252Fwww.google.com.hk%252F; _39wt_last_visit_time_cookie=1509934666599; area_info=CN110000|%D6%D0%B9%FA|%B1%B1%BE%A9|-|%B5%E7%D0%C5; JSESSIONID=abceGfXojuT8haavPhp_v; userLikesIdTemp=1509934693756; Hm_lvt_dc888321efaa2c58ab4aceeed619e820=1509934669; Hm_lpvt_dc888321efaa2c58ab4aceeed619e820=1510208538; _ga=GA1.2.1477589345.1509871125; _gid=GA1.2.774492229.1510208539; Hm_lvt_2e44bf94e67d57ced8420d8af730dd64=1509934669; Hm_lpvt_2e44bf94e67d57ced8420d8af730dd64=1510212906'
}
#url = 'http://yyk.39.net/doctors/'
urls = ['http://yyk.39.net/doctors/c_p{}'.format(str(i)) for i in range(2900,4000)]
conn = psycopg2.connect(database="datacloud", user="postgres", password="106524", host="127.0.0.1", port="5432")
cur = conn.cursor()

def get_data(url,data=None):
    wb_data = requests.get(url,headers=headers)
    time.sleep(2)  #每请求一次加一次延时，防止访问频率太快被网站禁止访问
    soup_page = BeautifulSoup(wb_data.text,'lxml')
    images      = soup_page.select('body > div.serach-wrap > div > div.serach-left > div.serach-left-list > ul > li > a > img')
    names       = soup_page.select('body > div.serach-wrap > div > div.serach-left > div.serach-left-list > ul > li > div.ys-msg > div > a[title=""]')
    titles      = soup_page.select('body > div.serach-wrap > div > div.serach-left > div.serach-left-list > ul > li > div.ys-msg > p:nth-of-type(1)')
    hospatils   = soup_page.select('body > div.serach-wrap > div > div.serach-left > div.serach-left-list > ul > li > div.ys-msg > p:nth-of-type(2)')
    departments = soup_page.select('body > div.serach-wrap > div > div.serach-left > div.serach-left-list > ul > li > div.ys-msg > p:nth-of-type(3)')
    ids         = soup_page.select('body > div.serach-wrap > div > div.serach-left > div.serach-left-list > ul > li > div.ys-msg > div')
    hosp_sites  = soup_page.select('body > div.serach-wrap > div > div.serach-left > div.serach-left-list > ul > li > div.ys-msg > p > a')

    # 保留html代码
    page_file_path = '/Users/zijianxu/Desktop/DataCloud/page/'
    with open(page_file_path+str(url[29:])+'.html','w') as w :
        w.write(str(soup_page))

    if data == None:
        for id,image,name,title,hospatil,department,hosp_site in zip(ids,images,names,titles,hospatils,departments,hosp_sites):
            data = {
                "id":id.get('id')[6:],
                "image":image.get('src'),
                "name":name.get_text(),
                "title":title.get_text(strip=True),
                "hospatil":hospatil.get_text(),
                "department":list(department.stripped_strings),
                "hosp_site":hosp_site.get('href')
            }

            # 该url+id = 医生详细信息的url
            url = 'http://yyk.39.net/doctor/' + data['id']
            wb_data = requests.get(url, headers=headers)
            soup_id = BeautifulSoup(wb_data.text, 'lxml')
            experiences = soup_id.select('#practiceExperience > div > div:nth-of-type(2)')
            works       = soup_id.select('body > div.doc-head > div.doc-detail.doc-wrap.clearfix > dl > dd > div')
            comments    = soup_id.select('body > div.doc-con > div > div.doc-left > div > div > div.doc-cm-filter.clearfix > div.tag.tag-hide > ul > li > a')
            if works == []:
                works = soup_id.select('body > div.doc-head > div.doc-detail.doc-wrap.clearfix > dl > dd')
            for work in works:
                searchObj_work = re.search(r'擅长领域(.*)', work.get_text())
                if searchObj_work:
                    work_detail = searchObj_work.group()

            try:
                work_detail
            except NameError:
                works = soup_id.select(
                    'body > div.doc-head > div.doc-detail.doc-wrap.clearfix > dl:nth-of-type(2) > dd:nth-of-type(4)')
                for work in works:
                    searchObj_work = re.search(r'擅长领域(.*)', work.get_text())
                    if searchObj_work:
                        work_detail = searchObj_work.group()

            for experience in experiences:
                if experience.get_text():
                    experience_detail = experience.get_text()
            try:
                experience_detail
            except NameError:
                experience_detail = '错误信息'

            if comments == []:
                comment_detail = 0
            else:
                for comment in comments:
                    searchObj_comment = re.search(r'[0-9]\d*', comment.get_text())
                    if searchObj_comment:
                        comment_detail = searchObj_comment.group()

            try:
                data_detail = {
                    "work": work_detail,
                    "experience": experience_detail,
                    "comment": comment_detail
                }
            except UnboundLocalError:
                print('编号%s的医生数据work_detail有错误' % data['id'])
                return []
            #print(data)
            #print(data_detail)

            # 保留html代码 路径:/Users/xuzijian/Desktop/DataCloud
            # page : page
            # detail : detail
            detail_file_path = '/Users/zijianxu/Desktop/DataCloud/detail/'
            with open( detail_file_path+str(data['id'])+'.html','w') as f :
                f.write(str(soup_id))

            # 执行sql语句，将data存入pg
            cur.execute("SELECT * FROM doctors_info WHERE doctors_id =%s" % data['id'])
            rows = cur.fetchall()
            if rows == []:
                cur.execute('''INSERT INTO doctors_info(doctors_id,image,name,title,hospatil,department,hosp_site,work_on,experience,comments) 
                              VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s );''',
                            (data['id'],data['image'],data['name'],data['title'],data['hospatil'],data['department'],data['hosp_site'],data_detail['work'],data_detail['experience'],data_detail['comment']))
                conn.commit()
            else:
                print("编号为%s的医生已存在。\n" % data['id'])




for single_url in urls:
    get_data(single_url)
    print("%s已跑完" % single_url)

conn.close()