# -*- coding: utf-8 -*-
"""
Created on Sun Feb 26 10:42:53 2017

@author: admin
"""

import requests
from bs4 import BeautifulSoup
import os
import time

def GetContent(url, refer='http://girl-atlas.net'):
    #该函数获取url对应的内容，并用BeautifulSoup处理，最后返回一个BeautifulSoup对象
    headers = {'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"}##浏览器请求头（大部分网站没有这个请求头会报错、请务必加上哦）
    headers['Referer'] = refer
    
    try:
        html_get = requests.get(url, headers=headers)    
        return html_get
    except:
        print('Error:'+'Get Content from '+url+' ERROR')
        time.sleep(3)
        try:
            html_get = requests.get(url, headers=headers)    
            return html_get
        except:
            print('Error[2nd]:'+'Get Content from '+url+' ERROR')
            return 0
        
        
        
def GetPageUrl():
    #该函数从首页获取不同页的页码，并合成页码链接
    url = 'http://girl-atlas.net/?p=1'
    html_Soup = SoupUrl(GetContent(url))
    max_page = int(html_Soup.findAll('li')[-9].text) ## 结果一般是数字，如253
    pageurl = []
    baseurl = 'http://girl-atlas.net/'
    for i in range(1, max_page+1):
        pageurl.append(baseurl + '?p=' + str(i))
    return pageurl
    
def GetAlbumUrl(pageurl_single):
    #该函数从每个页码链接获取专辑的链接
    url = pageurl_single
    soup = SoupUrl(GetContent(url))
    album_url = []
    baseurl = 'http://girl-atlas.net'
    for i in soup.findAll('h2'):
        album_url.append(baseurl + i.a['href'])
    return album_url
    
def SoupUrl(html_get):
    #将requests get的内容转化为Soup
    html_Soup = BeautifulSoup(html_get.text, 'lxml')
    return html_Soup
    
def GetAlbumTitle(soup):
    #给定album页面的soup，然后取得其标题，返回标题
    
    title = soup.h3.text.replace(' ','_').replace(':','_').replace('?','_') ##获取标题，通常结果是'[Wanibooks]_2011-05月号_#83_矶山沙耶香(磯山さやか)写真集_2nd_week'
    datenum = soup.h3.next_sibling.next_sibling.text.find('20') ##获取日期的编号
    date=''
    for i in range(0,10):
        date = date + soup.h3.next_sibling.next_sibling.text[datenum+i]
    date = date.replace('/','-')
    return '[' + date + ']' + title
    
def GetImgUrl(soup):
    #该函数从每个albumurl的soup里获取图片url
    #soup = SoupUrl(GetContent(album_url_single))
    img_url=[]
    for i in soup.section.findAll('img'):
        try:
            tmp = i['src']
            #print('src')
        except:
            tmp = i['delay']
            #print('delay')
        if tmp=='https://girlatlasfile.b0.upaiyun.com/static/img/arrowkeys.gif':
            pass
        else:
            img_url.append(tmp)
    return img_url
    
def mkdir(path):
    #建立文件夹，并提示是否成功
    path = path.strip()
    isExists = os.path.exists(os.path.join("E:\girlatlas", path))
    if not isExists:
        print(u'建了一个名字叫做', path, u'的文件夹！')
        os.makedirs(os.path.join("E:\girlatlas", path))
        return True
    else:
        print(u'名字叫做', path, u'的文件夹已经存在了！')
        return False
        
def SaveImg(album_url_single):
    #存储图片到硬盘
    try:    
        soup = SoupUrl(GetContent(album_url_single))
        title = GetAlbumTitle(soup)
        
        dir_root = "E:\girlatlas\\"
        os.chdir(dir_root)
        if mkdir(title):
            os.chdir(dir_root+title)
            imgurl = GetImgUrl(soup)
            name = 1
            for i in imgurl:
                img = GetContent(i, album_url_single)
                f = open(str(name)+'.jpg', 'wb')##写入多媒体文件必须要 b 这个参数！！必须要！！
                f.write(img.content) ##多媒体文件要是用conctent哦！
                f.close()
                name = name+1
    except:
        return 0
        
pageurl = GetPageUrl()
for i in pageurl:
    print(i)
    albumurl = GetAlbumUrl(i)
    for url in albumurl:
        if SaveImg(url)==0 :
            dir_root = "E:\girlatlas\\"
            os.chdir(dir_root)
            f = open('log.txt', 'a')
            f.write('Error[2nd]:'+'Get Content from '+url+' ERROR'+'\n')
            f.close()
            

