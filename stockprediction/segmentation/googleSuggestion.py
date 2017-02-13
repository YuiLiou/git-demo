import requests, json, os, pymysql, re
from ckipclient import CKIPClient
specialChar = ['／','/','\\','!','！','*','＊','？','?','＜','＞','<','>','|','＼','\'','"','“','”',
               ':','：','、','，',',','。','.','※','（','）','(',')','〔','〕','[',']','《','》','「','」',
               '【','】','『','』','＆','-',' ','　','\n','\t','；',';',' ','　','%','％']
com_list =['2330(台積電)','1216(統一)','1301(台塑)','1303(南亞)','1326(台化)',
           '2002(中鋼)','2317(鴻海)','2354(鴻準)',
           '2412(中華電)','2454(聯發科)','2498(宏達電)','2882(國泰金)']
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
        for com in com_list:
            sql = "SELECT * FROM `google-news` WHERE `company`=%s"
            cursor.execute(sql,(com))
            for row in cursor:
                if row['date']=='' and row['time']=='':
                    continue
                try:
                    new_content = str()
                    raw_content = row['content'].strip()
                    raw_content = p.sub('',raw_content)
                    article = ckip.segment(raw_content)
                    for words in article:
                        for i in range(len(words)):
                            newWord = words[i][0]
                            checkC = 0
                            for c in specialChar:
                                if newWord == c:
                                    checkC = 1
                            if checkC == 0:
                                new_content = new_content + newWord +'、'
                    try:
                        with connection2.cursor() as cursor2:
                            sql2 = "INSERT INTO `google-news-segment` (`date`,`time`,`title`,`content`,\
                            `publisher`,`company`,`seg-tool`,`alpha`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
                            cursor2.execute(sql2, (row['date'],row['time'],row['title'],new_content,row['publisher'],\
                            row['company'],'ckip',str(alpha)))
                        connection2.commit()
                        print ('connection2 commit')
                    except Exception as e:
                        print(str(e))
                except Exception as e:
                    print(str(e))
finally:
    connection.close()
    connection2.close()             
