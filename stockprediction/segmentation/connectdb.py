import pymysql.cursors
connection = pymysql.connect(host='localhost',
                                user='root',
                                password='12qwaszx',
                                db='news-set',
                                charset='utf8mb4',
                                cursorclass=pymysql.cursors.DictCursor)
count=0
try:
    with connection.cursor() as cursor:
        sql = "SELECT `content` FROM `google-news` WHERE `company`=%s"
        cursor.execute(sql, ('1101(台泥)',))
        for row in cursor:
            if count==5:
                break
            print(count,':',row['content'])
            count=count+1
finally:
    connection.close()
