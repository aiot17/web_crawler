import requests, bs4, re, os,time, random,json
from datetime import datetime

'''誠品'''
def eslite():
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)\
        Chrome/83.0.4103.61 Safari/537.36'}
    nowTime = datetime.now()
    downloadTime = '{}年{}月{}日{}時{}分'.format(nowTime.year,nowTime.month,nowTime.day,nowTime.hour,nowTime.minute)
    url = 'http://www.eslite.com/saleboard_bookstore.aspx'
    htmlfile = requests.get(url,headers=headers)
    soup = bs4.BeautifulSoup(htmlfile.text,'lxml')
    root = soup.find('div',class_='ST_mainbox')
    subdiv = root.find_all('div',class_='ST_box')
    finTop10 = []
    psyTop10 = []
    for i in subdiv:
        # print(i.p.text.strip()) #分類標籤
        if i.p.text.strip() == '財經／商業':
            info = i.find('div',class_='ST_boxB').find_all('a')
            for j in info:
                fin = {}
                # print(j['title'])
                # print(j['href'])
                fin['title'] = j['title']
                fin['url'] = j['href']
                finTop10.append(fin)
        elif i.p.text.strip() == '心理勵志':
            info = i.find('div',class_='ST_boxB').find_all('a')
            for k in info:
                psy = {}
                # print(k['title'])
                # print(k['href'])
                psy['title'] = k['title']
                psy['url'] = k['href']
                psyTop10.append(psy)
    return psyTop10,finTop10

'''博客來'''
def getRankNoSavingWeb(request,rank_no=1):
    ebook30dayranking = 'https://www.books.com.tw/web/sys_cebtopb/cebook?loc=subject_004'
    general30dayRanking = 'https://www.books.com.tw/web/sys_saletopb/books/'
    newGeneral30dayRanking = 'https://www.books.com.tw/web/sys_newtopb/books/'
    gbusiness30dayranking = 'https://www.books.com.tw/web/sys_saletopb/books/02/?loc=P_0002_003'
    newBusiness30dayRanking = 'https://www.books.com.tw/web/sys_newtopb/books/02/?loc=P_0002_003'
    gPyscho30dayRanking = 'https://www.books.com.tw/web/sys_saletopb/books/07/?loc=P_0002_008'
    newPychology30dayRanking = 'https://www.books.com.tw/web/sys_newtopb/books/07/?loc=P_0002_008'

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)\
            Chrome/83.0.4103.61 Safari/537.36'}
    titles = {'rank1':'電子書30日暢銷榜','rank2':'30日暢銷榜','rank3':'新書30日暢銷榜',
              'rank4':'商業30暢銷榜','rank5':'商業新書30日暢銷榜','rank6':'心理學書30暢銷榜',
                    'rank7':'心理學新書30日暢銷榜'}
    marker = ''
    if rank_no == 1:
        url_input = ebook30dayranking
        title = titles['rank1']
    elif rank_no == 2:
        url_input = general30dayRanking
        title = titles['rank2']
    elif rank_no == 3:
        url_input = newGeneral30dayRanking
        title = titles['rank3']
    elif rank_no == 4:
        url_input = gbusiness30dayranking
        title = titles['rank4']
    elif rank_no == 5:
        url_input = newBusiness30dayRanking
        title = titles['rank5']
    elif rank_no == 6:
        url_input = gPyscho30dayRanking
        title = titles['rank6']
    elif rank_no == 7:
        url_input = newPychology30dayRanking
        title = titles['rank7']
    elif rank_no == 8:
        withinTop100bookList, title, message = catorized()
        marker = '1'
    elif rank_no == 9:
        psy, fin = eslite()
        marker = '2'
        titleF = '財經TOP10排行榜'
    elif rank_no == 10:
        psy, fin = eslite()
        marker = '3'
        titleP = '心理學TOP10排行榜'
    else:
        url_input = ebook30dayranking
    try:
        htmlfile = requests.get(url_input, headers=headers)
        soup = bs4.BeautifulSoup(htmlfile.text, 'lxml')
        head = soup.find_all('li', class_='item')
        bookTop100 = []
        for i in head:
            # rankNums = i.find('div',class_='stitle').text.strip()
            # print(rankNums)
            eachBook = {}
            rankNumsTop = i.find('div', class_='stitle').span.text.strip()  # top
            rankNumNum = i.find('div', class_='stitle').p.find('strong', class_='no').text.strip()  # 排名的數字1~100
            # eachBook[rankNumsTop]=rankNumNum
            eachBook['labRank'] = rankNumsTop
            eachBook['Num'] = rankNumNum
            # print(rankNumsTop,rankNumNum)
            bookTitles = i.find('div', class_='type02_bd-a').h4.text.strip()  # 書名
            # eachBook['書名']=bookTitles
            eachBook['labTitle'] = '書名: '
            eachBook['bookTitle'] = bookTitles
            # print(bookTitles)
            authors = i.find('div', class_='type02_bd-a').li.text.strip()
            authTitleName = authors.split('：')  # [0]標籤 [1]作者
            # eachBook[authTitleName[0]] = authTitleName[1]
            eachBook['labAuth'] = authTitleName[0]
            eachBook['author'] = authTitleName[1]
            # print(authTitleName)
            prices = i.find('li', class_='price_a').text.strip().split('：')[1]  # 價格
            # eachBook['價格'] = prices
            eachBook['labPrice'] = '價格: '
            eachBook['price'] = prices
            # print(prices)
            urlLinks = i.find('div', class_='type02_bd-a').h4.a['href']  # 網址
            eachBook['網址'] = urlLinks
            # print(urlLinks)
            # imgUrlraws = i.find('a').find('img',class_='cover')['src'].split('=')[1]
            # pattern = '(.*).jpg'
            # imgUrls = re.search(pattern,imgUrlraws).group()#下載網址
            # eachBook['圖片網址'] = imgUrls
            bookTop100.append(eachBook)
            # print(imgUrlraws)
        # print(bookTop100)
        # allRanking[rankTitles[title]] = bookTop100
        # title+=1
    except:
        pass
    nowTime = datetime.now()
    downloadTime = '{}年{}月{}日{}時{}分的即時榜'.format(nowTime.year, nowTime.month, nowTime.day, nowTime.hour, nowTime.minute)
    return  render(request,'book.html',locals())

"""博客來之分類書籍函數開端"""
def catorized():
    ebook30dayranking = 'https://www.books.com.tw/web/sys_cebtopb/cebook?loc=subject_004'
    ebook30dayranking = 'https://www.books.com.tw/web/sys_cebtopb/cebook?loc=subject_004'
    general30dayRanking = 'https://www.books.com.tw/web/sys_saletopb/books/'
    newGeneral30dayRanking = 'https://www.books.com.tw/web/sys_newtopb/books/'
    gbusiness30dayranking = 'https://www.books.com.tw/web/sys_saletopb/books/02/?loc=P_0002_003'
    newBusiness30dayRanking = 'https://www.books.com.tw/web/sys_newtopb/books/02/?loc=P_0002_003'
    gPyscho30dayRanking = 'https://www.books.com.tw/web/sys_saletopb/books/07/?loc=P_0002_008'
    newPychology30dayRanking = 'https://www.books.com.tw/web/sys_newtopb/books/07/?loc=P_0002_008'

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)\
            Chrome/83.0.4103.61 Safari/537.36'}
    allGeneralUrls = [ebook30dayranking,general30dayRanking,newGeneral30dayRanking]
    pysFinUrls = [gbusiness30dayranking,newBusiness30dayRanking,gPyscho30dayRanking,newPychology30dayRanking]
    generalList = []
    nowTime = datetime.now()
    downloadTime = '{}年{}月{}日{}時{}分'.format(nowTime.year,nowTime.month,nowTime.day,nowTime.hour,nowTime.minute)
    for url in allGeneralUrls:
        htmlfile = requests.get(url,headers=headers)
        soup = bs4.BeautifulSoup(htmlfile.text,'lxml')
        head = soup.find_all('li',class_='item')
        for i in head:
            bookTitles = i.find('div', class_='type02_bd-a').h4.text.strip()  # 書名
            generalList.append(bookTitles)
    subjectList = []
    for url in pysFinUrls:
        htmlfile = requests.get(url,headers=headers)
        soup = bs4.BeautifulSoup(htmlfile.text,'lxml')
        head = soup.find_all('li',class_='item')
        for i in head:
            bookTitles = i.find('div', class_='type02_bd-a').h4.text.strip()  # 書名
            subjectList.append(bookTitles)
    withinTop100books = []
    for i in range(len(generalList)):
        for j in range(len(subjectList)):
            if generalList[i] == subjectList[j]:
                withinTop100books.append(subjectList[j])
    withinTop100bookList = set(withinTop100books)
    title = 'Top100之內的心理學與商業管理書籍'
    message = '三類總榜(包含暢銷,電子書,新書)中,一共有{}本心理與商業理財書籍'.format(len(withinTop100bookList))
    return withinTop100bookList,title, message
"""分類書籍函數末端"""

