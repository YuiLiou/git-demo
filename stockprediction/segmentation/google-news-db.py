import pymysql.cursors
import jieba
specialChar = ['/','\\','!','！','*','＊','？','?','＜','＞','<','>','|','\'','"','“','”',
               ':','：','、','，',',','。','※','（','）','(',')','[',']','《','》','「','」',
               '【','】','『','』','＆','-',' ','　','\n','\t','；',';']               
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
try:
    with connection.cursor() as cursor,connection2.cursor() as cursor2:
        sql = "SELECT * FROM `google-news`"
        cursor.execute(sql)
        for row in cursor:            
            date = row['date']
            time = row['time']
            title = row['title']
            content = row['content'].strip()
            publisher = row['publisher']
            company = row['company']
            newContent=''            
            words = jieba.cut(content, cut_all=False)
            for word in words:
                checkS = 0
                for char in specialChar:
                    if char == word:
                        checkS = 1
                if checkS==0:
                    newContent = newContent + word + '、'                        
            sql2 = "INSERT INTO `google-news-segment` (`date`,`time`,`title`,`content`,`publisher`,`company`,`seg-tool`,`alpha`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor2.execute(sql2,(date,time,title,newContent,publisher,company,'jieba','0'))
            connection2.commit()
finally:
    connection.close()
    connection2.close()
