#!/usr/bin/python
# -*- coding: utf-8 -*-
#Filenaem: testsogou.py

import os,sys,time,urllib2,re
import cookielib
import multiprocessing
import datetime,time

#定义存储完整的数据字典
#keyword: 具体短链接地址,发布时间,标题,平均每天浏览量,更新时间,总浏览量,链接地址
userJinYanAll={}

#提取用户总共有多少经验
def tiquNumber(url):
    # print '2-1'
    regex = re.compile(r'&pn=(\d{1,10})"')
    # print '2-11'
    web=urllib2.urlopen(url).read()
    # print '2-12'
    num= regex.findall(web)
    if not len(num):
        num.append(1)
    num=map(int,num)
    num.sort()
    return num[-1]

#拼接每一页的链接，返回链接的列表
def retJinYanYe(url,num):
    # print '准备获取分页页面...'
    yesNumLianjie=[]
    for i in range(0,num+1,7):
        yesNumLianjie.append(url+"&pn="+str(i))
    return yesNumLianjie

#返回分页经验
def retNumTitle(jylist):
    # print '2-2'
    numjisu=0
    for url in jylist:
        numjisu+=1
        #定义正则,链接,发布时间,标题
        regex_href = re.compile(r'<p class="tit"><a href="(.{1,200})" title="')
        regex_time=re.compile('<span class="exp-time">(.{1,12})</span>')
        regex_title=re.compile('" title="(.{1,80})" target="_blank">')
        #定义字典关键词
        regex_keyword=re.compile('e/(.{1,50}).html')
        #获取web分页中的数据
        web=urllib2.urlopen(url).read()
        #获取链接，发布时间，标题
        href=regex_href.findall(web)
        exp_time=regex_time.findall(web)
        title=regex_title.findall(web)
        #进行循环添加至列表的字典中
        # print url
        for i in range(0,len(title)):
            #定义一个空列表，用于添加至列表字典中
            userlist=[]
            keyword = regex_keyword.findall(href[i])
            # print keyword
            userlist.append(href[i])
            userlist.append(exp_time[i])
            userlist.append(title[i])
            # print keyword
            userJinYanAll[keyword[0]]=userlist
        # printstdout('\r正在获取第  %i  页的经验信息...' % numjisu)


        # print userJinYanAll

#根据地址,使用cookie浏览具体页面,返回浏览量,更新时间
def retLiuLanNum(keyword,url,i):
    # print '4'
    loginUrl='http://jingyan.baidu.com'+url
    #以cookie来访问具体的网页
    # cj = cookielib.CookieJar()
    # opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    # urllib2.install_opener(opener)
    # resp = urllib2.urlopen(loginUrl)
    req=urllib2.Request(loginUrl,data="")
    f=urllib2.urlopen(req).read()
    regex_liulannum = re.compile(r'<span class="views">(\d{1,10})</span>')
    regex_updateTime=re.compile(r'<time>(.{1,20})</time>')
    viewsNum=regex_liulannum.findall(f)
    updateTime=regex_updateTime.findall(f)
    #平均流量
    if int(viewsNum[0])!=0:
        jianGeDay=pingJunNum(keyword,updateTime[0],viewsNum[0])
        pjNum=int(viewsNum[0])/int(jianGeDay)/1.00
        if pjNum<1:
            userJinYanAll[keyword].append('-')
        else:
            userJinYanAll[keyword].append(str(pjNum))
        # print pjNum
    else:
        userJinYanAll[keyword].append('-')
    # print pingJunNum(keyword,updateTime,viewsNum)
    # sys.exit()
    # print viewsNum,updateTime
    userJinYanAll[keyword].append(updateTime[0])
    userJinYanAll[keyword].append(viewsNum[0])
    userJinYanAll[keyword].append(loginUrl)
    # print '5'
    # print userJinYanAll
    # sys.exit()
    # print str(i)+"\t\t"+userJinYanAll[keyword][1]+"\t"+userJinYanAll[keyword][5]+"\t"+userJinYanAll[keyword][3]+"\t"+userJinYanAll[keyword][2]+"\t"+userJinYanAll[keyword][6]

def getcookie():
    # loginUrl='http://jingyan.baidu.com/article/ed2a5d1f1938f909f7be174f.html'
    loginUrl='http://jingyan.baidu.com/article/c843ea0b9b851b77931e4aea.html'
    cj = cookielib.CookieJar()
    opener=urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    urllib2.install_opener(opener)
    resp=urllib2.urlopen(loginUrl)
    f = urllib2.urlopen(url= loginUrl)

def menu(url):
    # print '2'
    try:
        # print '2-3'
        #获取用户姝经验分页
        # print '提取经验总数量...'
        numYe=tiquNumber(url)
        #根据分页链接获取每页上面的链接
        # print '2-4'
        jylist=retJinYanYe(url,numYe)
        # print '2-5'
        # print '总共有:%s页经验.'%len(jylist)
        # print '根据分页信息获取具体链接..'
        # print jylist
        retNumTitle(jylist)
        # print '2-6'
        # for t in jylist:
            #根据链接生成字典数据
            # retNumTitle(t)
        # print '共有:%s篇经验.'%len(userJinYanAll)
        # print '获取Cookie信息中...'
        getcookie()
        # print '获取每篇经验具体的经验信息,此时间比较久,请耐心等待...'
        # print '----------输出具体的经验列表----------'
        # print '序列\t发布时间\t总浏量\t平均每天的浏览量\t\t标题\t\t\t具体链接'
        i=0

        for k,v in userJinYanAll.items():
            # print '3'
            i+=1
            retLiuLanNum(k,v[0],i)
            # print "%s:%s"%(k,v)
        # for k,v in userJinYanAll.items():
            # print k,v
            # print v[4]+"\t"+v[2]+"\t"+v[1]+"\t"+v[3]+"\t"+v[5]
        # print '-'*50
        #print userJinYanAll
        # userjianyanpaixu=sorted(userJinYanAll.iteritems(),key=lambda asd:asd[1],reverse=True)
        # for k,v in userjianyanpaixu.items():
        #     i+=1
        #     print str(i)+"\t\t"+userjianyanpaixu[1]+"\t"+userjianyanpaixu[5]+"\t"+userjianyanpaixu[3]+"\t"+userjianyanpaixu[2]+"\t"+userjianyanpaixu[6]
        # print '6'
        # print userJinYanAll
        # print '7'
        # tesret='99'
        return  userJinYanAll
        # print '8'
    except KeyboardInterrupt,e:
        return  "QUIT"
        # print "QUIT"

def printstdout(printname):
    sys.stdout.write("\r%s"%printname)
    sys.stdout.flush()

def pingJunNum(keyword,update,num):
    # print keyword,update,num
    updatetime=datetime.datetime.strptime(update,'%Y-%m-%d %H:%M')
    newde=datetime.datetime.now()
    chadate= newde-updatetime
    return str(chadate).split(' ')[0]

def sys_input():
    url_sogou='http://wenwen.sogou.com/z/q187003452.htm?sw=%E9%82%AE%E4%BB%B6%E8%90%A5%E9%94%80&ch=new.w.search.6&&ch=7'
    web=urllib2.urlopen(url_sogou).read()
    regex_title = re.compile(r'<h3 id="questionTitle">(.{1,100})</h3>')
    title=regex_title.findall(web)

    regex_way=re.compile(r'<div class="answer-con">(.{1,50000})</div>')
    way=regex_way.findall(web)
    return way
    # print web
    # raw_str=urllib2.quote(raw_input('请输入用户百度经验ID: '))
    # url=url_baidu+raw_str
    # url='http://jingyan.baidu.com/user/npublic/expList?un=QQ1520018443'
    # menu(url)
    # userjianyanpaixu=sorted(userJinYanAll.iteritems(),key=lambda asd:asd[1],reverse=True)
    # print userjianyanpaixu
    # for i in userjianyanpaixu:
        # print i[1]

def sys_input2(baiduid):
    try:
        url_baidu='http://jingyan.baidu.com/user/npublic/expList?un='
        raw_str=urllib2.quote(baiduid)
        url=url_baidu+baiduid
        # print '1'
        jylist=menu(url)
        return jylist
        # url='http://jingyan.baidu.com/user/npublic/expList?un=QQ1520018443'
        # menu(url)
    except:
        return 'ERROR'


if __name__=="__main__":
    print sys_input()




