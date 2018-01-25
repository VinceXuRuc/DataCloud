
#保存处理后的中间结果
work_on = []

#读取文件，用括号切分每一行字符，将拆分后的字符串写入work_on
def findBetween():
    with open('/Users/xuzijian/Desktop/disease_3.txt','r') as d:
        for line in d.readlines():
            line = line.strip()
            if line.find('(') != -1:
                for str_l in line.split(')'):
                    for i in str_l.split('('):
                        if i != '':
                            work_on.append(i)
    return work_on

#将work_on中的字符写入新的文件.
def writeToFile(work_on):
    with open('/Users/xuzijian/Desktop/disease_5.txt','a') as f:
        for line in work_on:
            f.write(line)
            f.write('\n')

#去掉文件中字符长度为1的字符
def deleteOneLenStr():
    with open('/Users/xuzijian/Desktop/disease_4.txt','r') as f, open('/Users/xuzijian/Desktop/disease_5.txt' , 'w') as ft :
        for line in f.readlines():
            line = line.strip()
            if len(line) != 1:
                ft.write(line)
                ft.write('\n')
            else:
                print(line)

#读取文件，用逗号进行切分(字符串中不包含括号)
def splitByDot():
    with open('/Users/xuzijian/Desktop/disease_5.txt','r') as f:
        for line in f.readlines():
            line = line.strip()
            if line.find(',') != -1 and line.find('(') == -1 :
                for i in line.split(','):
                    work_on.append(i)
    return work_on

#把处理后的disease_5.txt以追加模式写入disease_3.txt
def updateToFile():
    with open('/Users/xuzijian/Desktop/disease_5.txt','r') as r, open('/Users/xuzijian/Desktop/disease_3.txt','a') as w:
        for line in r.readlines():
            line = line.strip()
            w.write(line)
            w.write('\n')

#对文件中的字符串从长到短排序
def sortByLen():
    with open('/Users/xuzijian/Desktop/disease.txt', 'r') as f:
        for line in f.readlines():
            line = line.strip()
            work_on.append(line)

    work_on.sort(key=lambda x: len(x), reverse=True)
    with open('/Users/xuzijian/Desktop/disease_1.txt', 'w') as d:
        for work in work_on:
            d.write(work)
            d.write('\n')

#读取文件，将文件中的重复值去掉，但保留原list的顺序，最后写入新的文件
def distinctAndSort():
    with open('/Users/xuzijian/Desktop/disease.txt','r') as r:
        for line in r.readlines():
            line = line.strip()
            work_on.append(line)
    new_work_on = sorted(set(work_on), key=work_on.index)
    with open('/Users/xuzijian/Desktop/disease.txt', 'w') as w:
        for i in new_work_on:
            w.write(i)
            w.write('\n')

#test str
#str = "肾炎,动脉硬化性,良性高血压"
#work_on = splitByDot()
#writeToFile(work_on)
#updateToFile()
#sortByLen()
#distinctAndSort()
#work_on = findBetween()
#writeToFile(work_on)
#if str.find(','):
#    idx = str.find(',')
#    print(str[:idx])
