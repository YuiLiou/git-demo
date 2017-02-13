import pymysql.cursors
import datetime
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
segtool = 'ckip'
com_list =['2330','3481','3673','4904','4938','5880','6505']
try:
    with connection.cursor() as cursor, connection2.cursor() as cursor2:
        for com in com_list:
            trading = list()
            sql = "SELECT * FROM `stock-price` WHERE `company`=%s AND `wave4` IS NULL"
            cursor.execute(sql, (com))
            for row in cursor:
                wave4 = str()
                if row['close'] >= row['MA5'] > row['MA10']:
                    wave4 = 'positive'
                elif row['MA10'] > row['MA5'] >= row['close']:
                    wave4 = 'negative'
                else:
                    wave4 = 'neutral'
                try:
                    sql2 = "UPDATE `stock-price` SET `wave4`=%s WHERE `company`=%s AND `date`=%s"
                    cursor2.execute(sql2,(wave4,com,row['date']))
                    connection2.commit()
                    print ('update stock-price success!')
                except:
                    print ('update error')
            sql2 = "SELECT * FROM `google-news-segment` WHERE `company` LIKE %s"
            cursor.execute(sql2, ('%'+com+'%'))
            for row in cursor:
                wave4 = 0
                sql3 = "SELECT * FROM `stock-price` WHERE `company` LIKE %s AND `date`=%s"
                cursor2.execute(sql3, ('%'+com+'%',row['date']))
                row2 = cursor2.fetchone()
                if row2 is not None:
                    wave4 = row2['wave4']
                else:
                    sql4 = "SELECT * FROM `stock-price` WHERE `company` LIKE %s AND `date` > %s ORDER BY `date` ASC"
                    cursor2.execute(sql4, ('%'+com+'%',row['date']))
                    row3 = cursor2.fetchall()
                    wave4 = row3[0]['wave4']
                try:
                    sql5 = "UPDATE `google-news-segment` SET `label2`=%s WHERE `date`=%s AND `time`=%s AND `title`=%s AND `company`=%s AND `publisher`=%s AND `seg-tool`=%s AND `alpha`=%s"
                    cursor2.execute(sql5,(wave4,row['date'],row['time'],row['title'],row['company'],row['publisher'],row['seg-tool'],row['alpha']))
                    connection2.commit()
                    print ('update segment success!')
                except:
                    print ('update google seg error')
finally:
    connection.close()
    connection2.close()