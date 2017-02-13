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
connection3 = pymysql.connect(host='localhost',
                                user='root',
                                password='12qwaszx',
                                db='news-set',
                                charset='utf8mb4',
                                cursorclass=pymysql.cursors.DictCursor)
segtool = 'ckip'
alpha = '0'
company = '2330(台積電)'
try:
    with connection.cursor() as cursor, connection2.cursor() as cursor2:
        sql = "SELECT COUNT(DISTINCT(`title`)) FROM `term-freq` WHERE `seg-tool`=%s AND `alpha`=%s AND `company`=%s"
        # 文章篇數
        cursor.execute(sql,(segtool,alpha,company))
        result = cursor.fetchone()
        newsCount = result['COUNT(DISTINCT(`title`))']
        sql2 = "SELECT DISTINCT(`term`) FROM `term-freq` WHERE `seg-tool`=%s AND `alpha`=%s AND `company`=%s"
        cursor.execute(sql2,(segtool,alpha,company))
        i = 0
        for row in cursor:
            #if i == 30 :
            #    break
            term = row['term']
            sql3 = "SELECT `polarity2`, COUNT(DISTINCT(`title`)) FROM `term-freq` WHERE `seg-tool`=%s AND `alpha`=%s AND \
            `company`=%s AND `term`=%s GROUP BY `polarity2`" # term - document frequency
            cursor2.execute(sql3,(segtool,alpha,company,term))
            for row2 in cursor2:
                if row2['polarity2']=='positive':
                    n_pos_freq = row2['COUNT(DISTINCT(`title`))']
                if row2['polarity2']=='neutral':
                    n_neu_freq = row2['COUNT(DISTINCT(`title`))']
                if row2['polarity2']=='negative':
                    n_neg_freq = row2['COUNT(DISTINCT(`title`))']
            
            sql4 = "SELECT `polarity2`, COUNT(DISTINCT(`title`)) FROM `term-freq` WHERE `seg-tool`=%s AND `alpha`=%s AND \
            `company`=%s AND `term`!=%s GROUP BY `polarity2`" # term - document frequency
            cursor2.execute(sql4,(segtool,alpha,company,term))
            for row2 in cursor2:
                if row2['polarity2']=='positive':
                    np_pos_freq = row2['COUNT(DISTINCT(`title`))']
                if row2['polarity2']=='neutral':
                    np_neu_freq = row2['COUNT(DISTINCT(`title`))']
                if row2['polarity2']=='negative':
                    np_neg_freq = row2['COUNT(DISTINCT(`title`))']            
            # positive-chi
            A = n_pos_freq
            B = n_neg_freq + n_neu_freq
            C = np_pos_freq
            D = np_neg_freq + np_neu_freq
            chi_pos = (newsCount*((A*D-C*B)^2))/((A+C)*(B+D)*(A+B)*(C+D))
            # negative-chi
            A = n_neg_freq
            B = n_pos_freq + n_neu_freq
            C = np_neg_freq
            D = np_pos_freq + np_neu_freq
            chi_neg = (newsCount*((A*D-C*B)^2))/((A+C)*(B+D)*(A+B)*(C+D))
            # neutral-chi
            A = n_neu_freq
            B = n_pos_freq + n_neg_freq
            C = np_neu_freq
            D = np_pos_freq + np_neg_freq
            chi_neu = (newsCount*((A*D-C*B)^2))/((A+C)*(B+D)*(A+B)*(C+D))
            print (term, chi_pos, chi_neg, chi_neu)
            with connection3.cursor() as cursor3:
                try:
                    sql5 = "INSERT INTO `term-power2` (`seg-tool`,`alpha`,`company`,`term`,\
                    `chi_pos`,`chi_neg`,`chi_neu`) VALUES (%s,%s,%s,%s,%s,%s,%s)"
                    cursor3.execute(sql5,(segtool,alpha,company,term,chi_pos,chi_neg,chi_neu))
                    connection3.commit()
                except:
                    print('insert error')
finally:
    connection.close()
    connection2.close()
    connection3.close()

