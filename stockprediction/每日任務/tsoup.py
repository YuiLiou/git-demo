import requests
from bs4 import BeautifulSoup
url = 'http://ctee.com.tw/News/EditorChoice.aspx?yyyymmdd=20161124&filename=4fc7d66c-f187-49fd-8584-c96977c6d031.png'
res = requests.get(url)
res.encoding = 'utf-8'
soup = BeautifulSoup(res.text, 'html.parser')
print ('工商時報')
for News in soup.select('div.NewsList'):
    for ctime in News.select('h5.Black'):
        date = (ctime.text.split('|')[0].strip())
        time = ('12:00')
        print (date,time)
        break
    for ctime in News.select('h5'):
        date = (ctime.text.split('|')[0].strip())
        date2 = date[0:4] + '-' + date[4:6] + '-' + date [6:8]
        time = ('12:00')
        print (date2,time)
        break
    for p in News.select('p'):
        print (p.text)
        
