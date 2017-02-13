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
open_time = datetime.time(9,0,0)
close_time = datetime.time(13,30,0)
try:
    with connection.cursor() as cursor:
        trading = list()
        sql = "SELECT * FROM `stock-price` WHERE `company`=%s"
        cursor.execute(sql,('market'))
        for row in cursor:
            trading.append([row['date'],row['wave1'],row['wave2'],row['wave3']])
        sql2 = "SELECT * FROM `yahoo-news`"
        cursor.execute(sql2)
        for row2 in cursor:
            sdate = row2['date']
            stime = row2['time']
            if sdate != '' and stime!= '':
                trading_index = -1
                for i in range(len(trading)):
                    if trading[i][0] == sdate:
                        #print ('找到交易日')
                        trading_index = i
                if trading_index == -1:
                    #print ('找不到交易日')
                    for i in range(len(trading)):
                        if trading[i][0] > sdate:
                            #print (trading[i][0],sdate)
                            trading_index = i
                            break
                stime = str(stime)
                stime = datetime.time(int(stime.split(':')[0]),int(stime.split(':')[1]),int(stime.split(':')[2]))
                if stime < open_time:
                    wave = trading[trading_index][1]
                    # print ('開盤前',wave)
                elif stime >= open_time and stime <= close_time:
                    wave = trading[trading_index][2]
                    # print ('盤中',wave)
                elif stime > close_time:
                    wave = trading[trading_index][3]
                    # print ('盤後',wave)
                try:
                    with connection2.cursor() as cursor2:
                        sql3 = "UPDATE `yahoo-news` SET `label`=%s WHERE `date`=%s and `time`=%s and `title`=%s"
                        cursor2.execute(sql3, (wave, row2['date'], row2['time'], row2['title']))
                        connection2.commit()
                        print('update', row2['title'])
                except:
                    print('sql error')
finally:
    connection.close()
