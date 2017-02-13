import pymysql.cursors
import datetime
import csv
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
#print ((t1<t2))
com_list =['2330','3481','3673','4904','4938','5880','6505']
try:
    with connection.cursor() as cursor, connection2.cursor() as cursor2:
        for com in com_list:
            trading = list()
            sql = "SELECT * FROM `stock-price` WHERE `company`=%s"
            cursor.execute(sql, (com))
            for row in cursor:
                trading.append([row['date'],row['wave1'],row['wave2'],row['wave3']])
            sql2 = "SELECT * FROM `google-news` WHERE `company` LIKE %s"
            cursor.execute(sql2, ('%'+com+'%'))
            for row in cursor:
                sdate = (row['date'])
                wave = 'null'
                if len(sdate.split('-')) == 3:
                    sdate = datetime.date(int(sdate.split('-')[0]), int(sdate.split('-')[1]), int(sdate.split('-')[2]))
                    stime = (row['time'])
                    if len(stime.split(':')) > 1 or stime == '':
                        # print (sdate)
                        trading_index = -1
                        for i in range(len(trading)):
                            #if i == 0:
                                #continue
                            if len(str(trading[i][0]).split('-')) > 2:
                                year = int(trading[i][0].split('-')[0])
                                newdate = datetime.date(year, int(trading[i][0].split('-')[1]),
                                                        int(trading[i][0].split('-')[2]))
                                if newdate == sdate:
                                    # print ('找到交易日')
                                    trading_index = i
                        if trading_index == -1:
                            # print ('找不到交易日')
                            for i in range(len(trading)):
                                #if i == 0:
                                    #continue
                                year = int(str(trading[i][0]).split('-')[0])
                                newdate = datetime.date(year, int(trading[i][0].split('-')[1]),
                                                        int(trading[i][0].split('-')[2]))
                                if newdate > sdate:
                                    wave = trading[i][1]
                                    # print ('new date:',newdate,'wave:',wave)
                                    trading_index = i
                                    break
                    if stime != '':
                        h = stime.split(':')[0]
                        if h[0] == '上' or h[0] == '下':
                            h = int(h[2:])
                        m = int(stime.split(':')[1])
                        stime2 = datetime.time(int(h), m, 0)
                        # print (stime2)
                        if stime2 < open_time:
                            wave = trading[trading_index][1]
                            # print ('開盤前',wave)
                        elif stime2 >= open_time and stime2 <= close_time:
                            wave = trading[trading_index][2]
                            # print ('盤中',wave)
                        elif stime2 > close_time:
                            wave = trading[trading_index][3]
                            # print ('盤後',wave)
                    elif stime == '':
                        wave = trading[trading_index][2]
                try:
                    sql3 = "UPDATE `google-news-segment` SET `label`=%s WHERE `date`=%s and `time`=%s and `title`=%s and `company` LIKE %s"
                    # print(wave,row['date'],row['time'],row['title'])
                    cursor2.execute(sql3, (wave, row['date'], row['time'], row['title'], '%'+com+'%'))
                    connection2.commit()
                    print('update', com, row['date'])
                except:
                    print('sql error')
finally:
        connection.close()
        connection2.close()