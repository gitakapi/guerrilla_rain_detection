import csv
import datetime
import sys

sys.stdout = open("text.txt","w")

fp = open('hokurikudate.csv')

for line in fp :
    txt = ((line.replace('\n','')).split(',')[0]).split('/') + ((line.replace('\n','')).split(',')[1]).split(':')
    txt[4] = txt[4][0] + '0'
    d = datetime.datetime(int(txt[0]),int(txt[1]),int(txt[2]),int(txt[3]),int(txt[4]))
    d = d - datetime.timedelta(hours=2)
    for i in range(17) :
        d = d + datetime.timedelta(minutes=10)
        print(d)

f = open('datetime.txt', 'w')
fp = open('text.txt')
for line in fp :
    txt = line.replace(' ','')
    txt = txt.replace('-','')
    txt = txt.replace(':','')
    f.write(txt)
