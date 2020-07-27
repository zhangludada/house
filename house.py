

import requests
import re
from pyquery import PyQuery as pq
import time
import json

def html_parse(url):
    headers = {
        'Referer': 'https://sh.lianjia.com/ershoufang/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0',
    }

    r=requests.get(headers=headers,url=url,allow_redirects=False)
    if r.status_code==200:
        doc=pq(r.text)
        data=[]
        div=doc('div')('.info')('.clear')
        for i in div.items():
            d={}
            slipt='################'
            title=i('a').text()
            link=i('a').attr('href')
            community=i('.flood')('a').text()
            detail=i('.address').text()
            total_price=i('.priceInfo')('.totalPrice').text()
            unitprice=i('.priceInfo')('.unitPrice').text()

            d['app']='链家'
            d['title']=title
            d['link']=link
            d['community']=community
            d['detail']=detail
            d['total_price']=total_price
            d['unitprice']=unitprice

            write_file('链家.json',d)

            data.append(d)
        print(url+'爬取成功')
        return data
    else:
        write_file('fail_url.txt',url)
        print(url+'爬取失败')
        return url
        # print(slipt)
        # print('title:'+title)
        # print('link:'+link)
        # print('community:'+community)
        # print('detail:'+detail)
        # print('total_price:'+total_price)
        # print('unitprice:'+unitprice)

#create url list
def url_ls():
    url = ['https://sh.lianjia.com/ershoufang/']
    for i in range(2, 101):
        url_page = 'https://sh.lianjia.com/ershoufang/pg{}/'.format(i)
        url.append(url_page)

    return url

def write_file(filename,data):
    with open(filename,mode='a',encoding='utf-8') as f:
        json.dump(data,f,ensure_ascii=False)

def main():
    page=1
    for url in url_ls():
        html_parse(url)
        print('第{}页完成,一共{}页'.format(page,len(url_ls())))
        page+=1
        time.sleep(6)

main()






