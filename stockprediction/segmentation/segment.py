#encoding=utf-8
import jieba
import os
import codecs
jieba.set_dictionary('dict.txt.big')
infile = 'D:\\每日任務'
outfile = 'D:\\斷詞內容'
com_list =['1101+台泥',
           '1102+亞泥',  '1216+統一', '1301+台塑',  '1303+南亞',  '1326+台化',
           '1402+遠東新','1722+台肥',  '2002+中鋼', '2105+正新',   '2201+裕隆',  '2207+和泰車',
           '2301+光寶科','2303+聯電',  '2311+日月光', '2317+鴻海', '2324+仁寶',  '2325+矽品',
           '2330+台積電','2347+聯強',  '2353+宏碁',  '2354+鴻準',  '2357+華碩',  '2382+廣達',
           '2409+友達',  '2412+中華電','2454+聯發科', '2474+可成', '2498+宏達電', '2801+彰銀',
           '2880+華南金','2881+富邦金','2882+國泰金', '2883+開發金','2885+元大金', '2886+兆豐金',
           '2890+永豐金','2891+中信金','2892+第一金', '2912+統一超','3008+大立光', '3045+台灣大',
           '3231+緯創',  '3474+華亞科','3481+群創',  '3673+宸鴻',  '3697+晨星',  '4904+遠傳',
           '4938+和碩',  '5880+合庫金','6505+台塑化',]
specialChar = ['/','\\','!','*','?','<','>','|','\'','"',':','、','，','。','(',')','[',']','-']
for com in com_list:
    files = os.listdir(infile+'\\'+com)
    for file in files:
        content = open (infile+'\\'+com+'\\'+file,encoding='utf-8',).read()
        words = jieba.cut(content, cut_all=False)
        
        if not os.path.exists(outfile+'\\'+com):
            os.makedirs(outfile+'\\'+com)
        fileout = codecs.open(outfile+'\\'+com+'\\'+file,'w','utf-8')
        for word in words:
            checkS = 0
            for char in specialChar:
                if char == word:
                    checkS = 1
            if checkS==0 and len(word)>0:
                fileout.write (word+'、')
        fileout.close()
