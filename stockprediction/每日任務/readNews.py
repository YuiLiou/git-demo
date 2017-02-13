import re
import os
import csv
import time
import codecs
import requests
import pymysql.cursors
from bs4 import BeautifulSoup

# http://www.chinatimes.com/realtimenews/20160809010807-260410
# http://ww2.money-link.com.tw/RealtimeNews/NewsContent.aspx?SN=928093002&PU=0010
# http://udn.com/news/story/7251/1885898
# http://news.ltn.com.tw/news/business/paper/1020159
# http://times.hinet.net/news/19227449
# http://www.appledaily.com.tw/realtimenews/article/finance/20160812/927274/paperart_right
# http://money.udn.com/money/story/5739/1890661-7%E6%9C%88%E7%87%9F%E6%94%B6%E4%B8%8D%E4%BD%B3-%E5%8F%B0%E7%A9%8D%E9%9B%BB%E8%AA%8D%E5%94%AE%E6%AC%8A%E8%AD%89%E8%A1%9D%E7%AC%AC%E4%B8%80
# http://n.yam.com/cnabc/fn/20160809/20160809833784.html
# https://www.moneydj.com/KMDJ/News/NewsViewer.aspx?a=bb3e02cc-14f0-4e29-9177-adb42aba6ad8
# http://www.cnabc.com/news/aall/201607150208.aspx
# http://www.cna.com.tw/news/afe/201607120146-1.aspx
# http://news.sina.com.tw/article/20160812/18241019.html
# http://news.cnyes.com/news/id/3595498
# http://www.ettoday.net/news/20161027/800348.htm
# http://ctee.com.tw/News/ViewCateNews.aspx?newsid=137730&cateid=tgvl
connection = pymysql.connect(host='localhost',
                             user='root',
                             password='12qwaszx',
                             db='news-set',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
specialChar = ['/', '\\', '!', '*', '?', '<', '>', '|', '\'', '"', ':', '[', ']', '\'']

pat1 = 'chinatimes.com/'
pat2 = 'money-link.com.tw/RealtimeNews/'
pat3 = 'udn.com/'
pat4 = 'news.ltn.com.tw/'
pat5 = 'times.hinet.net/'
pat6 = 'www.appledaily.com.tw/'
pat7 = 'udn.com/news/'
pat8 = 'n.yam.com/'
pat9 = 'www.moneydj.com/'
pat10 = 'www.cnabc.com/'
pat11 = 'www.cna.com.tw/'
pat12 = 'news.sina.com.tw/'
pat13 = 'news.cnyes.com/'
pat14 = 'www.ettoday.net/'
pat15 = 'ctee.com.tw/News/'

path = 'company'

files = os.listdir(path)
try:
    with connection.cursor() as cursor:
        for file in files:
            file = file.split('.')[0]
            company = file.replace('+', '(') + ')'
            if not os.path.exists(file):
                os.makedirs(file)
            with open(path + '\\' + file + '.csv', newline='') as csvfile:
                spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
                for row in spamreader:
                    try:
                        dataRow = str(row).replace('[\'', '').replace('\']', '').split(',')
                        url = dataRow[-1]
                        del dataRow[-1]
                        news_title = str(dataRow)
                        for ch in specialChar:
                            news_title = news_title.replace(ch, '')
                        if news_title == '[]' or url[0:4] != 'http':
                            continue
                        if os.path.exists(file + '/' + news_title + '.txt'):
                            # print ('已記錄')
                            continue
                        fileout = codecs.open(file + '/' + news_title + '.txt', 'w', 'utf-8')
                        content = date = time = publisher = ''
                        # time.sleep(1)
                        res = requests.get(url)
                        res.encoding = 'utf-8'
                        soup = BeautifulSoup(res.text, 'html.parser')
                        used = 0
                        # pat15
                        matchObj = re.search(pat15, url)
                        if matchObj and used == 0:
                            used = 1
                            print('工商時報')
                            fileout.write('工商時報' + '\n')
                            publisher = '工商時報'
                            for News in soup.select('div.NewsList'):
                                for ctime in News.select('h5'):
                                    d = (ctime.text.split('|')[0].strip())
                                    date = d[0:4] + '-' + d[4:6] + '-' + d[6:8]
                                    time = ('12:00')
                                    fileout.write(date + ' ' + time + '\n')
                                    break
                                for ctime in News.select('h5.Black'):
                                    date = (ctime.text.split('|')[0].strip().replace('/', '-'))
                                    time = ('12:00')
                                    fileout.write(date + ' ' + time + '\n')
                                    break
                                for p in News.select('p'):
                                    fileout.write(p.text)
                                    content = content + p.text
                                # pat14
                        matchObj = re.search(pat14, url)
                        if matchObj and used == 0:
                            used = 1
                            print('ettody')
                            fileout.write('ettoday' + '\n')
                            publisher = 'ettoday'
                            for ctime in soup.select('span.news-time'):
                                fileout.write(ctime.text + '\n')
                                date = str(ctime.text).split()[0].replace('/', '-').replace('年', '-').replace('月',
                                                                                                              '-').replace(
                                    '日', '')
                                time = str(ctime.text).split()[1]
                            for div in soup.select('div.story section'):
                                for p in div.find_all('p'):
                                    if p.find('a'):
                                        break
                                    fileout.write(p.text)
                                    content = content + p.text
                        # pat13
                        matchObj = re.search(pat13, url)
                        if matchObj and used == 0:
                            used = 1
                            print('鉅亨網')
                            fileout.write('鉅亨網' + '\n')
                            publisher = '鉅亨網'
                            for ctime in soup.select('div._1R6 time'):
                                fileout.write(str(ctime.text).replace('/', '-') + '\n')
                                date = str(ctime.text).split()[0].replace('/', '-').replace('年', '-').replace('月','-').replace('日', '')
                                time = str(ctime.text).split()[1]
                            for sec in soup.select('section._82F'):
                                for div in sec.select('div p'):
                                    fileout.write(div.text)
                                    content = content + div.text
                        # pat12
                        matchObj = re.search(pat12, url)
                        if matchObj and used == 0:
                            used = 1
                            print('新浪新聞')
                            fileout.write('新浪新聞' + '\n')
                            publisher = '新浪新聞'
                            for ctime in soup.select('div#articles cite'):
                                fileout.write(str(ctime.text).split('(')[1].replace(')', '') + '\n')
                                date = str(ctime.text).split()[1].strip('(')
                                time = str(ctime.text).split()[2].strip(')')
                            for div in soup.select('div.pcont'):
                                for p in div.select('p'):
                                    fileout.write(p.text)
                                    content = content + p.text
                                    break
                        # pat11
                        matchObj = re.search(pat11, url)
                        if matchObj and used == 0:
                            used = 1
                            print('中央通訊社(商情網)')
                            fileout.write('中央通訊社(商情網)' + '\n')
                            publisher = '中央通訊社(商情網)'
                            for ctime in soup.select('div.update_times p'):
                                fileout.write(str(ctime.text).replace('發稿時間：', '').replace('/', '-') + '\n')
                                date = str(ctime.text).replace('發稿時間：', '').split()[0].replace('/', '-').replace('年','-').replace('月', '-').replace('日', '')
                                time = str(ctime.text).replace('發稿時間：', '').split()[1]
                                break
                            for div in soup.select('section'):
                                for p in div.select('p'):
                                    fileout.write(p.text)
                                    content = content + p.text
                        # pat10
                        matchObj = re.search(pat10, url)
                        if matchObj and used == 0:
                            used = 1
                            print('中央通訊社')
                            fileout.write('中央通訊社' + '\n')
                            publisher = '中央通訊社'
                            for ctime in soup.select('div.date'):
                                fileout.write(ctime.text + '\n')
                                date = str(ctime.text).split()[0].replace('/', '-').replace('年', '-').replace('月','-').replace('日', '')
                                time = str(ctime.text).split()[1]
                                break
                            for div in soup.select('div.box_2'):
                                for p in div.select('p'):
                                    fileout.write(p.text)
                                    content = content + p.text
                        # pat9
                        matchObj = re.search(pat9, url)
                        if matchObj and used == 0:
                            used = 1
                            publisher = 'MoneyDJ'
                            print('MoneyDJ')
                            fileout.write('MoneyDJ' + '\n')
                            for ctime in soup.select('span#ctl00_ctl00_MainContent_Contents_lbDate'):
                                fileout.write(str(ctime.text).replace('/', '-') + '\n')
                                date = str(ctime.text).split()[0].replace('/', '-').replace('年', '-').replace('月','-').replace('日', '')
                                time = str(ctime.text).split()[1]
                                break
                            for div in soup.select('#highlight'):
                                for p in div.select('article'):
                                    fileout.write(p.text)
                                    content = content + p.text
                        # pat8
                        matchObj = re.search(pat8, url)
                        if matchObj and used == 0:
                            used = 1
                            publisher = 'yam新聞'
                            print('yam新聞')
                            fileout.write('yam新聞' + '\n')
                            for ctime in soup.select('time.time'):
                                fileout.write(ctime.text.replace('年', '/').replace('月', '/').replace('日', '') + '\n')
                                date = str(ctime.text).split()[0].replace('/', '-').replace('年', '-').replace('月','-').replace('日', '')
                                time = str(ctime.text).split()[1]
                                break
                            for div in soup.select('div#news_content'):
                                for p in div.select('p.middle'):
                                    fileout.write(p.text.replace('\n', '').replace('蕃Plus+1+1', ''))
                                    content = content + p.text.replace('\n', '').replace('蕃Plus+1+1', '')

                        # pat7
                        matchObj = re.search(pat7, url)
                        if matchObj and used == 0:
                            used = 1
                            publisher = '聯合報'
                            print('聯合報')  # 2016-08-10 14:23
                            fileout.write('聯合報' + '\n')  # 2016-08-10 14:23
                            for ctime in soup.select('div.story_bady_info_author'):
                                fileout.write(str(ctime.text).replace('\"', '')[0:16] + '\n')
                                date = str(ctime.text).replace('\"', '')[0:16].split()[0].replace('/', '-').replace('年','-').replace('月', '-').replace('日', '')
                                time = str(ctime.text).replace('\"', '')[0:16].split()[1]
                            for div in soup.select('div#story_body_content'):
                                for p in div.select('p'):
                                    fileout.write(p.text)
                                    content = content + p.text
                        # pat6
                        matchObj = re.search(pat6, url)
                        if matchObj and used == 0:
                            used = 1
                            publisher = '蘋果日報'
                            print('蘋果日報')  # 2016-11-01
                            fileout.write('蘋果日報' + '\n')  # 2016-11-01
                            for ctime in soup.select('div.gggs time'):
                                fileout.write(
                                    str(ctime.text).replace('年', '-').replace('月', '-').replace('日', ' ') + '\n')
                                date = str(ctime.text)[0:10].replace('年', '-').replace('月', '-').replace('日', '')
                                time = str(ctime.text)[11:16]
                            for div in soup.select('div.articulum.trans'):
                                for p in div.select('p'):
                                    fileout.write(p.text)
                                    content = content + p.text
                        # pat5
                        matchObj = re.search(pat5, url)
                        if matchObj and used == 0:
                            used = 1
                            publisher = 'Hinet'
                            print('Hinet')
                            fileout.write('Hinet' + '\n')
                            for ctime in soup.select('span.cp'):
                                for a in ctime.select('a'):
                                    fileout.write(str(ctime.text).replace(str(a.text), '').split('(')[0] + '\n')
                                    date = str(ctime.text).replace(str(a.text), '').split('(')[0].split()[0].replace('/', '-')
                                    time = str(ctime.text).replace(str(a.text), '').split('(')[0].split()[1]
                                    break
                            for div in soup.select('div.newsContent'):
                                for p in div.select('p'):
                                    fileout.write(p.text)
                                    content = content + p.text

                        # pat4
                        matchObj = re.search(pat4, url)
                        if matchObj and used == 0:
                            used = 1
                            publisher = '自由時報'
                            print('自由時報')  # 2016-11-03
                            fileout.write('自由時報' + '\n')  # 2016-11-03
                            for ctime in soup.select('div#newstext span'):
                                fileout.write(str(ctime.text) + '\n')
                                date = str(ctime.text).split()[0].replace('/', '-').replace('年', '-').replace('月','-').replace('日', '')
                                time = str(ctime.text).split()[1]
                                break
                            for div in soup.select('div.text.boxTitle'):
                                for p in div.select('p'):
                                    fileout.write(p.text)
                                    content = content + p.text
                        # pat3
                        matchObj = re.search(pat3, url)
                        if matchObj and used == 0:
                            used = 1
                            publisher = '聯合財經網'
                            print('聯合財經網')
                            fileout.write('聯合財經網' + '\n')
                            for ctime in soup.select('#story_bady_info h3'):
                                fileout.write(str(ctime.text).split(' ')[0] + ' ')
                                date = str(ctime.text).split()[0].replace('/', '-').replace('年', '-').replace('月','-').replace('日', '')
                                fileout.write(str(ctime.text).split(' ')[1] + '\n')
                                time = str(ctime.text).split()[1]
                                break
                            for div in soup.select('div#story_body_content'):
                                for p in div.select('p'):
                                    fileout.write(p.text.split('(function()')[0])
                                    content = content + p.text.split('(function()')[0]
                                    break
                                # pat2
                        matchObj = re.search(pat2, url)
                        if matchObj and used == 0:
                            used = 1
                            publisher = '富聯網'
                            print('富聯網')  # 2016/10/12 13:43
                            fileout.write('富聯網' + '\n')  # 2016/10/12 13:43
                            for ctime in soup.select('div.NewsDate'):
                                date20 = str(ctime.text)
                                index = date20.find('20')
                                fileout.write(date20[index:index + 17] + '\n')
                                date = date20[index:index + 17].split()[0].replace('/', '-').replace('年', '-').replace('月', '-').replace('日', '')
                                time = date20[index:index + 17].split()[1]
                            for div in soup.select('div.NewsMainContent'):
                                fileout.write(div.text)
                                content = content + div.text
                        # pat1
                        matchObj = re.search(pat1, url)
                        if matchObj and used == 0:
                            used = 1
                            publisher = '中國時報'
                            print('中國時報')  # 2016-08-09 17:23
                            fileout.write('中國時報' + '\n')  # 2016-08-09 17:23
                            for ctime in soup.select('div.reporter time'):
                                date = str(ctime.text).split()[0].replace('年', '-').replace('月', '-').replace('日', '')
                                time = str(ctime.text).split()[1]
                                fileout.write(
                                    str(ctime.text).replace('年', '-').replace('月', '-').replace('日', '') + '\n')
                            for div in soup.select('article.clear-fix'):
                                for article in div.select('article.clear-fix'):
                                    for p in article.select('p'):
                                        fileout.write(p.text)
                                        content = content + p.text
                        fileout.close()
                        if used == 0:
                            os.remove(file + '/' + news_title + '.txt')
                            print(url)
                        elif used == 1:
                            if time[0:2] == '下午':
                                time = time.replace('下午', '')
                            elif time[0:2] == '上午':
                                time = time.replace('上午', '')
                            elif time == '':
                                time = '12:00'
                            sql = "INSERT INTO `google-news` (`title`, `publisher`, `date`, `time`, `content`, `company`) VALUES (%s,%s,%s,%s,%s,%s)"
                            cursor.execute(sql, (news_title, publisher, date, time, content, company))
                            connection.commit()
                            print(date, time, news_title, company)
                    except:
                        pass
finally:
    connection.close()
