import jieba
import jieba.posseg as pseg
import re

work_on = []

""" 将work_on字段中的字拆成单字，并对其按照BIEO进行标注，生成CRF++的训练语料库"""
def matchFromFound(chart):
    count = 0
    flag = []
    for part in range(len(chart)):
        flag.insert(part,'O')
    if chart is None:
        return []
    with open('/Users/xuzijian/Desktop/data_found.txt', 'r') as ft:
        for line in ft.readlines():
            line = line.strip()
            str = line.split('/')
            for i in str[:-1]:
                if chart.find(i) != -1:
                    count = count + 1
                    start_idx = chart.find(i)
                    end_idx = start_idx + len(i) - 1
                    flag[start_idx] = 'B'
                    flag[end_idx] = 'E'
                    for j in range(start_idx+1,end_idx):
                        flag[j] = 'I'

        if count == 0:
            flag = list(chart)
            for i in range(len(flag)):
                flag[i] = 'O'
    return flag


def writeToFile(flag):
    with open('/Users/xuzijian/Desktop/test_flag_words.txt','a+') as w :
        for i in flag:
            w.write(i)
            w.write('\n')
        w.write('\n')


"""将work_on字段用jieba分词并标注词性，单字作为一行"""
with open('/Users/xuzijian/Desktop/data_found.txt' ,'r') as f , open('/Users/xuzijian/Desktop/new_test.txt', 'w') as ft:
    for line in f.readlines():
        line = line.strip()
        line = re.sub("[\s+\.\!\/_,$%^*(+\"\']+|[+——！，。？、~@#￥%……&*（）]+", "", line)
        words = pseg.cut(line)
        for word, flag in words:
            for i in word:
                ft.write(i)
                ft.write("\t")
                ft.write(flag)
                ft.write('\n')
        ft.write('\n')
