import re

"""标注BIEO"""
work_on = []
with open('/Users/xuzijian/Desktop/train/new_test_info.txt','r') as f, open('/Users/xuzijian/Desktop/train/new_trained_found.txt','w') as ft:
    for line in f.readlines():
        line = line.strip()
        if line != '':
            if line[-1] == 'B':
                work_on.append(line[0])
            elif line[-1] == 'I':
                work_on.append(line[0])
            elif line[-1] == 'E':
                work_on.append(line[0])
                work_on.append('/')
        else:
            work_on.append('\n')

    for i in work_on:
        ft.write(i)
