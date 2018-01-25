# coding:utf-8
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
'''
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
'''

conn = psycopg2.connect(database="datacloud", user="postgres", password="106524", host="127.0.0.1", port="5432")
cur = conn.cursor()
cur.execute("SELECT doctor_id,work_on FROM doctor_info ORDER BY doctor_id ASC ")
rows = cur.fetchall()
for row in rows:
    new_work_on = ""
    work_on = []
    work_on = matchFromDict(row[1])
    for j in work_on:
        new_work_on = new_work_on + j + '/'
    cur.execute("UPDATE doctor_info SET work_on ='%s' WHERE doctor_id =%s " % (new_work_on,str(row[0])))
    i = i + 1
    print("第%d行数据写入db中" % i)
conn.commit()
conn.close()