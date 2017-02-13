import os
import pymysql.cursors
connection = pymysql.connect(host='localhost',
                                user='root',
                                password='12qwaszx',
                                db='google-news',
                                charset='utf8mb4',
                                cursorclass=pymysql.cursors.DictCursor)
path = 'company'
companies = os.listdir(path)
try:
    with connection.cursor() as cursor:
        for company in companies:
            company = company.split('.')[0]
            c = (company.replace('+','(')+')')
            files = os.listdir(company)
            for file in files:
                title = file.split('.')[0]
                text = open(company+'/'+file,encoding='utf-8')
                counter = 0
                content = date = time = publisher = ''
                for line in text:
                    if counter == 0:
                        #print ('news',line)
                        publisher = line
                        pass
                    elif counter == 1:
                        #print ('time',line)
                        try:
                            date = line.split()[0].replace('/','-').replace('年','-').replace('月','-').replace('日','')
                            time = line.split()[1]
                            #print (date)
                            #print (time)
                        except:
                            pass
                    else:
                        pass
                        content = content + line            
                    counter = counter + 1                
                sql = "INSERT INTO `each-news` (`title`, `publisher`, `date`,`time`,`content`, `company`) VALUES (%s,%s,%s,%s,%s,%s)"
                cursor.execute(sql, (title, publisher, date, time, content, c))
                print (title,c)
                connection.commit()
finally:
    connection.close()          
    

