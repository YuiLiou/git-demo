from ckipclient import CKIPClient
import pymysql.cursors
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
CKIP_IP='127.0.0.1'
CKIP_PORT=1501
CKIP_USERNAME='Joel'
CKIP_PASSWORD='12qwaszx'
ckip = CKIPClient(CKIP_IP, CKIP_PORT, CKIP_USERNAME, CKIP_PASSWORD)
alpha = 0.2
def GoogleSuggestion(word):
    headers = {'User-agent':'Mozilla/5.0'}
    response = requests.get(URL+word, headers=headers)
    result = json.loads(response.content.decode('utf-8'))
    wfreq = len(result[1])  # 建議字個數
    if wfreq == 0 :
        return 0
    else:
        wset = set()
        for extend in result[1]: # 建議字列表
            strr = extend.replace(result[0],'').strip()
            if strr == '':
                wset.add('')
            else:
                wset.add(strr[0])
                break
        #print (word,result)
        return (len(wset)/wfreq)
try:
    with connection.cursor() as cursor,connection2.cursor() as cursor2:
        sql = "SELECT * FROM `google-news` WHERE `company`=%s"
        cursor.execute(sql,('2330(台積電)'))
        for row in cursor:
            if row['content']=='':
                print ('content missing')
                continue
            if row['date']=='' and row['time']=='':
                print ('time missing')
                continue
            try:
                sample_text = row['content'].strip()
                sample_results = ckip.segment(sample_text)
                date = row['date']
                time = row['time']
                title = row['title']
                publisher = row['publisher']
                company = row['company']
                newContent = ''
                newWord = ''
                for article in sample_results:
                    i=0
                    end = 0
                    while i < len(article):
                        
                        if end == 1:
                            break
                        checkS = 0
                        for c in specialChar:
                            if article[i][0]==c:
                                checkS = 1
                                break
                        if checkS == 0:
                            newWord = article[i][0]
                            for j in range(1,6):
                                if i + j >= len(article):
                                    end = 1
                                    break
                                if (GoogleSuggestion(newWord+article[i+j][0])) >= alpha:
                                    newWord = newWord + article[i+j][0]
                                else:
                                    i = i + j
                                    break                          
                        print (newWord)
                        i = i + 1

                        '''
                        checkS = 0                
                        for c in specialChar:
                            if word[0]==c:
                                checkS = 1
                                break                            
                        if checkS == 0:
                            newContent = newContent + word[0] + '、'
                            '''
                
                try:
                    sql2 = "INSERT INTO `google-news-segment` (`date`,`time`,`title`,`content`,`publisher`,`company`,`seg-tool`,`alpha`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
                    cursor2.execute(sql2,(date,time,title,newContent,publisher,company,'ckip','0'))
                    connection2.commit()
                except:
                    print ('sql error')
            except:
                print ('seg error')                      
finally:
    connection.close()
    connection2.close()
