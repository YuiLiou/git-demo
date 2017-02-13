import csv
import os
from datetime import date
from os import rename
from robobrowser import RoboBrowser
com_list =['1101+台泥',  '1102+亞泥',  '1216+統一', '1301+台塑',  '1303+南亞',  '1326+台化',
           '1402+遠東新','1722+台肥',  '2002+中鋼', '2105+正新',   '2201+裕隆',  '2207+和泰車',
           '2301+光寶科','2303+聯電',  '2311+日月光', '2317+鴻海', '2324+仁寶',  '2325+矽品',
           '2330+台積電','2347+聯強',  '2353+宏碁',  '2354+鴻準',  '2357+華碩',  '2382+廣達',
           '2409+友達',  '2412+中華電','2454+聯發科', '2474+可成', '2498+宏達電', '2801+彰銀',
           '2880+華南金','2881+富邦金','2882+國泰金', '2883+開發金','2885+元大金', '2886+兆豐金',
           '2890+永豐金','2891+中信金','2892+第一金', '2912+統一超','3008+大立光', '3045+台灣大',
           '3231+緯創',  '3474+華亞科','3481+群創',  '3673+宸鴻', '4904+遠傳',
           '4938+和碩',  '5880+合庫金','6505+台塑化',]
num = 1000
month = str(date.today()).split('-')[1]
day = str(date.today()).split('-')[2]
rename('company', 'company'+month+day)
if not os.path.exists('company'):
    os.makedirs('company')
for com in com_list:
    com = com.replace(" ","+")
    url = "https://www.google.com/search?q="+com+"&tbm=nws&num="+str(num)+"&filter=0&cr=tw&ie=utf-8&oe=utf-8&hl=zh-TW"
    browser = RoboBrowser(user_agent='a python robot')
    browser.session.headers['User-Agent'] # a python robot
    browser.open(url)
    news_list = list()
    f = open('company\\'+com+'.csv','w')
    w = csv.writer(f)
    for body in browser.select('div#search'):
        for div in body.select('div.g'):
            for a in div.select('h3 a'):
                hreff = str(a.attrs.get('href')).replace('%3F','?').replace('%3D','=').replace('%26','&').replace('/url?q=','')
                href = hreff.split('&sa=U')[0]
                print (a.text)
                #print ('(',href,')')
                try:
                    w.writerow ([a.text,href])
                except:
                    print ('error',a.text)
                    w.writerow (['error',href])              
                
    f.close()
    
