import requests, json, os, pymysql
import datetime
import re
from ckipclient import CKIPClient
specialChar = ['／','/','\\','!','！','*','＊','？','?','＜','＞','<','>','|','＼','\'','"','“','”',
               ':','：','、','，',',','。','.','※','（','）','(',')','〔','〕','[',']','《','》','「','」',
               '【','】','『','』','＆','-',' ','　','\n','\t','；',';',' ','　','%','％']    
connection = pymysql.connect(host='localhost',
                                user='root',
                                password='12qwaszx',
                                db='news-set',
                                charset='utf8mb4',
                                cursorclass=pymysql.cursors.DictCursor)
connection2 = pymysql.connect(host='localhost',
                                user='root',
                                password='12qwaszx',
                                db='news-set',
                                charset='utf8mb4',
                                cursorclass=pymysql.cursors.DictCursor)
URL="http://suggestqueries.google.com/complete/search?client=firefox&hl=zh-TW&cr=tw&q="
alpha = 1
p = re.compile('\d+')
ckip = CKIPClient('127.0.0.1', 1501, 'Joel', '12qwaszx')
try:
    with connection.cursor() as cursor:
        sql = "SELECT * FROM `yahoo-news`"
        cursor.execute(sql)
        for row in cursor:
            if row['date']=='' and row['time']=='':
                continue            
            try:
                new_content = str()
                paragraph = str(row['content']).split('\n')
                for para in paragraph:
                    para = p.sub('',para)
                    article = ckip.segment(para)
                    for words in article:                
                        end = 0                        
                        for i in range(len(words)):
                            if end == 1:
                                break
                            newWord = words[i][0]
                            checkC = 0
                            for c in specialChar:
                                if newWord == c:
                                    checkC = 1
                                    break
                            if checkC == 0:                                
                                new_content = new_content + '、' + newWord                                
                try:
                    with connection2.cursor() as cursor2:
                        sql2 = "INSERT `yahoo-news-segment` (`date`, `time`, `title`, `segment`, `alpha`) VALUES (%s,%s,%s,%s,%s)"
                        cursor2.execute(sql2, (row['date'],row['time'],row['title'],new_content,alpha))
                        connection2.commit()
                    print (datetime.datetime.now(),'connection2 commit')
                except Exception as e:
                    print (str(e))
            except Exception as e:
                print (str(e))
finally:
    connection.close()
    connection2.close()             
