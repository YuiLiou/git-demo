import pymysql.cursors
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
com_list = ['2330(台積電)']
alpha = '0'
segtool = 'ckip'
try:
    with connection.cursor() as cursor, connection2.cursor() as cursor2:
        for com in com_list:
            sql = "SELECT * FROM `google-news-segment` AS g WHERE NOT EXISTS (SELECT * FROM `term-freq` AS tf WHERE \
                   tf.title=g.title AND tf.date=g.date AND tf.company=%s AND tf.`seg-tool`=%s AND tf.alpha=%s)"
            countC = 1
            cursor.execute(sql, (com,segtool,alpha))
            for row in cursor:   # 每一篇文章
                doc_term = dict()
                content = row['content'].split('、')
                #每一個字詞
                for con in content:
                    if con not in doc_term:
                        doc_term[con] = 1
                    else:
                        doc_term[con] += 1
                print ('data',countC)
                countC = countC + 1
                try:
                    for term in doc_term.keys():
                        sql2 = "INSERT INTO `term-freq` (`date`,`title`,`term`,`freq`,`polarity`,`polarity2`,`seg-tool`,`alpha`,`company`) VALUES (%s,%s,%s,%s,%s,%s,%s)"
                        cursor2.execute(sql2,(row['date'], row['title'],term,doc_term[term],row['label'],row['label2'],row['seg-tool'],row['alpha'],row['company']))
                        connection2.commit()
                    print ('connection commit')
                except:
                    print ('duplicate entry')
finally:
    connection.close()
    connection2.close()
