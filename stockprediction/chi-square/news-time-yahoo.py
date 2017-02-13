import pymysql.cursors
import datetime
import csv
connection = pymysql.connect(host='localhost',
                                user='root',
                                password='12qwaszx',
                                db='news-set',
                                charset='utf8mb4',
                                cursorclass=pymysql.cursors.DictCursor)
trading = list()
try:
    with connection.cursor() as cursor:
        with open('table.csv') as csvfile:
            sreader = csv.reader(csvfile)
            for r in sreader:
                trading.append(r)
            for i in range(len(trading)):
                try:
                    if i == 0:
                        continue
                    elif i == len(trading) - 1:
                        wave = 0
                    else:
                        wave = float(trading[i][4]) - float(trading[i+1][4])
                    trading[i][0] = trading[i][0].replace('/','-')
                    today_open = float(trading[i][1])
                    today_close = float(trading[i][4])
                    if i - 1 >= 0:
                        pro_open = float(trading[i + 1][1])
                    else:
                        pro_open = 0
                    if i + 1 < len(trading):
                        pre_close = float(trading[i - 1][1])
                    else:
                        pre_close = 0
                    # 當日開盤價 / 前日收盤價
                    if today_open > pre_close:
                        wave1 = '上漲'
                    elif today_open == pre_close:
                        wave1 = '持平'
                    elif today_open < pre_close:
                        wave1 = '下跌'
                    # 當日收盤價 / 當日開盤價
                    if today_close > today_open:
                        wave2 = '上漲'
                    elif today_close == today_open:
                        wave2 = '持平'
                    elif today_close < today_open:
                        wave2 = '下跌'
                    # 次日開盤架 / 當日收盤價
                    if pro_open > today_close:
                        wave3 = '上漲'
                    elif pro_open == today_close:
                        wave3 = '持平'
                    elif pro_open < today_close:
                        wave3 = '下跌'
                    sql = "INSERT INTO `stock-price` (`company`,  `date`,  `open`, `high`, `low`, `close`, `volume`, `wave0`,`wave1`,`wave2`,`wave3`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                    cursor.execute(sql,('market',trading[i][0],trading[i][1],trading[i][2],trading[i][3],trading[i][4],trading[i][5],wave,wave1,wave2,wave3))
                    connection.commit()
                except:
                    print ('insert error')
        csvfile.close()
finally:
    connection.close()