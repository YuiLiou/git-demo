import requests
from bs4 import BeautifulSoup
import re
import os
import datetime
import pymysql.cursors
date_split = re.compile('2.*日')
time_split = re.compile(r'(上午|下午)(\d{1,2}:\d{1,2})')
specialChar = ['[',']','(',')','\'']
connection = pymysql.connect(host='localhost',
                             user='root',
                             password='12qwaszx',
                             db='news-set',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
try:
    with connection.cursor() as cursor:
        for j in range(1,41):
            titlelist = []
            datelist = []
            timelist = []
            contentlist = []
            
            index = 'https://tw.news.yahoo.com/stock/archive/' + str(j) +'.html' #新聞類別網址取代處
            try:
                res = requests.get(index)
                soup = BeautifulSoup(res.text,"html.parser")
                for title in soup.select('ul.yom-list-wide.thumbnail'):
                    for i in range(0,25):
                        titlelist.append(title.select('h4')[i].text.replace(" ","").replace(">","").replace("<","").replace("?","").replace("/","").replace('"',"").replace("*","").replace(":","").replace("|","").replace('\\',""))
                        #print (title.select('h4')[i].text) #Title
                        date =str(date_split.findall(title.select('cite')[i].text))
                        datelist.append(date)
                        #print (str(date_split.findall(title.select('cite')[i].text))) #date
                        time = str(time_split.findall(title.select('cite')[i].text))
                        timelist.append(time)
                        contentlist.append(title.select('h4')[i].select('a')[0].attrs.get('href'))
                        #print (title.select('h4')[i].select('a')[0].attrs.get('href')) #href
            except:
                print("Error")
            for k in range(len(contentlist)):
                dirName = 'D:/DataSet/stock/'+datelist[k]  #檔案存放處
                if os.path.exists(dirName):
                    print(" ")
                else:
                    os.mkdir(dirName)
                print (contentlist[k])
                try:
                    date = datelist[k].replace('年','-').replace('月','-').replace('日','')
                    line = timelist[k].strip()
                    res1 =requests.get('https://tw.news.yahoo.com/'+contentlist[k])
                    soup1 = BeautifulSoup(res1.text,"html.parser")
                    fileName = titlelist[k]
                    for c in specialChar:
                        line = line.replace(c,'')
                        date = date.replace(c,'')                       
                    ifmorning = line.split(',')[0]
                    time1 = line.split(',')[1]
                    if ifmorning == '上午':                
                        hour = int(time1.split(':')[0])
                        if hour == 12:
                            hour=0
                    elif ifmorning == '下午':
                        hour = int(time1.split(':')[0])+12
                        if hour == 24:
                            hour=12                
                    minute = int(time1.split(':')[1])
                    second = 0
                    datetime1 = datetime.time(hour,minute,second)

                    fileout = open(dirName + '/'+fileName+'.txt','w',encoding='utf-8')
                    for content in soup1.select('div.yom-mod.yom-art-content'):
                        if content.text !="":
                            print (fileName +" OK")
                            fileout.write(timelist[k]+'\n')
                            fileout.write(content.text)
                            try:
                                sql = "INSERT INTO `yahoo-news` (`title`, `date`, `time`, `content`) VALUES (%s,%s,%s,%s)"
                                cursor.execute(sql, (fileName, date, datetime1, content.text))
                                connection.commit()
                            except:
                                print('mysql error')
                    fileout.close()
                except:
                    print("Error")
finally:
	connection.close()

