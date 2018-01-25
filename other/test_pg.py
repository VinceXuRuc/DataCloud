import psycopg2
'''测试字符串从pg中取出来的形式
conn = psycopg2.connect(database="datacloud", user="postgre", password="106524", host="127.0.0.1", port="5432")
cur = conn.cursor()

cur.execute("SELECT work_on FROM doctors_info ORDER BY doctors_id ASC " )
rows = cur.fetchall()
for row in rows:
    print(row[0])
conn.commit()
conn.close()
'''

'''统计文件中"缺失数据"的个数
count = 0;
with open('/Users/xuzijian/Desktop/data_found.txt' , 'r') as f :
    for line in f.readlines():
        line = line.strip()
        if line == '缺失数据':
            count = count + 1

print(count)


with open('/Users/xuzijian/Desktop/data_words.txt','r') as f , open('/Users/xuzijian/Desktop/words.txt','w') as ft :
    for line in f.readlines():
        line = line.strip()
        line = list(line)
        for i in line[:-1]:
            ft.write(i)
            ft.write(" ")
            ft.write(line[-1])
            ft.write('\n')

"""从pg中取得work_on字段"""
conn = psycopg2.connect(database="datacloud", user="postgre", password="106524", host="127.0.0.1", port="5432")
cur = conn.cursor()

cur.execute("SELECT work_on FROM doctors_info ORDER BY doctors_id ASC ")
rows = cur.fetchall()

with open('/Users/xuzijian/Desktop/test_data_found.txt','r') as f:
    for line in f.readlines():
        line = line.strip()
        words = line.split('/')
        start_idx = 1
        end_idx = 3
        list_words = list(words[0])
        for i in range(start_idx,end_idx):
            list_words[i] = 'I'
        print(list_words)
'''

with open('/Users/xuzijian/Desktop/train/new_test.txt' ,'r') as r , open('/Users/xuzijian/Desktop/test_flag_words.txt','r') as f ,\
    open('/Users/xuzijian/Desktop/train/test_final_words.txt','w') as w:
    for r_line,f_line in zip(r.readlines(),f.readlines()):
        r_line = r_line.strip()
        f_line = f_line.strip()
        w.write(r_line)
        w.write("\t")
        w.write(f_line)
        w.write('\n')


with open('/Users/xuzijian/Desktop/data_found.txt','r') as r :
    for line in r.readlines():
        line = line.strip()
        line = re.sub("[\s+\.\!\/_,$%^*(+\"\']+|[+——！，。？、~@#￥%……&*（）]+", "", line)
        flag = matchFromFound(line)
        writeToFile(flag)