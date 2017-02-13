# -*- coding: utf-8 -*-
import csv,pymysql
from grs import TWSEOpen, Stock
connection = pymysql.connect(host='140.116.96.202',
                                user='user',
                                password='12qwaszx',
                                db='news-set',
                                charset='utf8mb4',
                                cursorclass=pymysql.cursors.DictCursor)
com_list =['1101','1102','1216','1301','1303','1326',
           '1402','1722','2002','2105','2201','2207',
           '2301','2303','2311','2317','2324','2325',
           '2330','2347','2353','2354','2357','2382',
           '2409','2412','2454','2474','2498','2801',
           '2880','2881','2882','2883','2885','2886',
           '2890','2891','2892','2912','3008','3045',
           '3231','3481','3673','4904','4938','5880','6505']
try:
    with connection.cursor() as cursor:
        for com in com_list:
            com = com.split('+')[0]
            stock = Stock(com,30)
            stock.out_putfile(com+'[30-month].csv')
            with open(com+'[30-month].csv', 'rb') as csvfile:
                info = list()
                spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
                for r in spamreader:
                    if len(r[0].split(','))>=9:
                        info.append(r[0].split(','))
                for r2 in info:
                    r2[0] = str(int(r2[0].split('/')[0])+1911) + '-' +r2[0].split('/')[1]+'-'+r2[0].split('/')[2]
                for i in range(len(info)):
                    today_open = float(info[i][3])
                    today_close = float(info[i][6])
                    if i-1 >=0 :
                        pre_close = float(info[i-1][6])
                    else:
                        pre_close = 0
                    if i+1 < len(info):
                        pro_open = float(info[i+1][3])
                    else:
                        pro_open = 0
                    # 當日開盤價 / 前日收盤價
                    if today_open > pre_close:
                        wave1 = 'positive'
                    elif today_open == pre_close:
                        wave1 = 'neutral'
                    elif today_open < pre_close:
                        wave1 = 'negative'
                    # 當日收盤價 / 當日開盤價
                    if today_close > today_open:
                        wave2 = 'positive'
                    elif today_close == today_open:
                        wave2 = 'neutral'
                    elif today_close < today_open:
                        wave2 = 'negative'
                    # 次日開盤架 / 當日收盤價
                    if pro_open > today_close:
                        wave3 = 'positive'
                    elif pro_open == today_close:
                        wave3 = 'neutral'
                    elif pro_open < today_close:
                        wave3 = 'negative'
                    # 3MA
                    MA3 = 0
                    MA5 = 0
                    MA7 = 0
                    MA10 = 0
                    k = 0
                    for j in range(-2,1):
                        if i+j >= 0:
                            MA3 = MA3 + float(info[i+j][6])
                            k = k + 1
                    MA3 = MA3 / k
                    # 5MA
                    k = 0
                    for j in range(-4,1):
                        if i+j >= 0:
                            MA5 = MA5 + float(info[i+j][6])
                            k = k + 1
                    MA5 = MA5 / k
                    # 7MA
                    k = 0
                    for j in range(-6,1):
                        if i+j >= 0:
                            MA7 = MA7 + float(info[i+j][6])
                            k = k + 1
                    MA7 = MA7 / k
                    # 10MA
                    k = 0
                    for j in range(-9,1):
                        if i+j >= 0:
                            MA10 = MA10 + float(info[i+j][6])
                            k = k + 1
                    MA10 = MA10 / k
                    try:
                        sql = "INSERT INTO `stock-price` (`company`,`date`,`volume`,`open`,`high`,`low`,`close`,`wave0`,`transactions`,\
                        `MA3`,`MA5`,`MA7`,`MA10`,`wave1`,`wave2`,`wave3`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                        cursor.execute(sql,(com,info[i][0],info[i][1],info[i][3],info[i][4],info[i][5],info[i][6],info[i][7],info[i][8],\
                                            MA3,MA5,MA7,MA10,wave1,wave2,wave3))
                        connection.commit()
                        print 'connection commit'
                    except:
                        print 'sql error'
                        
finally:
    connection.close()
