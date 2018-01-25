import jieba.analyse

'''
jieba.analyse.set_stop_words('/Users/xuzijian/Desktop/stop_words.txt')

with open('/Users/xuzijian/Desktop/new.txt','r') as f, open('/Users/xuzijian/Desktop/new_data.txt','w') as w :
    for line in f.readlines():
        line = line.strip()
        tags = jieba.analyse.extract_tags(line,20,allowPOS=('ns','n'))
        for tag in tags:
            w.write(tag)
        w.write('\n')


with open('/Users/xuzijian/Desktop/new.txt','r') as r , open('/Users/xuzijian/Desktop/new_data.txt','w') as w:
    for line in r.readlines():
        line = line.strip()
        lines = line.split('/')
        for l in lines:
            if len(l)>2:
                w.write(l)
                w.write('/')
        w.write('\n')
'''

import psycopg2
i = 0
work_on = []

def matchFromDict(chart):
    if chart is None:
        return []
    with open('/Users/xuzijian/Desktop/FILE *fp/DataCloud/data/disease_1.txt','r') as d:
        for line in d.readlines():
            line = line.strip()
            if chart.find(line) != -1:
                work_on.append(line)
                chart = chart.replace(line, '')
    return work_on

def writeToFile(work_on):
    f = open('/Users/xuzijian/Desktop/data_found.txt', 'a+')
    if work_on == ['']:
        f.write('缺失数据\n')
    else:
        for work in work_on:
            if work != '':
                f.write(work)
                f.write('/')
        f.write('\n')
        f.close()

conn = psycopg2.connect(database="datacloud", user="postgre", password="106524", host="127.0.0.1", port="5432")
cur = conn.cursor()
cur.execute("SELECT doctor_id,work_on FROM doctor_info ORDER BY doctor_id ASC ")
rows = cur.fetchall()
for row in rows:
    new_work_on = ""
    work_on = []
    work_on = matchFromDict(row[1])
    for i in work_on:
        new_work_on = new_work_on + i + '/'
    print(new_work_on)