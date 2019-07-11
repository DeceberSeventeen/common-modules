#!/usr/bin/python2
# -*- coding: utf-8 -*-

import re
import sys
import time
import email
import nntplib
import poplib
from nntplib import NNTP
from chardet import detect


class GetpEmail():
    '''wait ......
    popObj = poplib.POP3("mail.aaaaaa.com",110)
    popObj.user("yanglin")
    popObj.pass_("111111Aa")
    popObj.stat()
    popObj.list()
    popObj.set_debuglevel(3)
    popObj.getwelcome()
    popObj.quit()
'''


class GetNews(object):
    '''获取news 的信息！
        获取news 的信息并不要使用nntp模块自带的方法，主要是获取head 然后取拆分和head获取所需数据
        这样各个元素容易配套，一一对应！
        所以这个类有getHead的方法，返回字典，除了body其他都有
        还有一个getArticle(),根据id获取全文包括head！'''

    # 初始化类
    def __init__(self, server, port=119, userName=None, passWord=None):
        if userName is not None:
            self.nntpObj = NNTP(server, port, userName, passWord)
        else:
            self.nntpObj = NNTP(server, port)

# 设置要访问的组，返回一个元组（响应， 计数， 第一条id，最后一条id）

    def setGroup(self, groupName):
        resp, count, first, last, name = self.nntpObj.group(groupName)
        return (resp, count, first, last, name)

# 退出nntp 连接

    def quitService(self):
        self.nntpObj.quit()

# 获取news的正文内容

    def getArticle(self, id_str, filePath=None):
        art = self.nntpObj.article(str(id_str))
        if None != filePath:
            self.__write(art[3], filePath)
        else:
            pass
        return art[3]

    def getMainBody(self, id_str, filePath=None):
        body = self.nntpObj.body(str(id_str))
        if None != filePath:
            self.__write(body[3])
        else:
            pass
        return body[3]

# 通过id获取头并格式成一个字典，如果不存在则返回None

    def __getDictHead(self, id_str):
        try:
            head = self.nntpObj.head(str(id_str))
        except nntplib.NNTPTemporaryError as e:
            # head = self.quitService()
            print e
            print 'Not found news,id = %s  !' % str(id_str)
            return
        headResult = self.__formatHeadToDict(head)
        return headResult

# 格式head字符串，生成字典

    def __formatHeadToDict(self, headList):
        rsp_id_messageID = headList[0].split(' ')
        headMain = headList[3]
        resultDict = {
            'respNum': rsp_id_messageID[0],
            'ID': rsp_id_messageID[1]
        }
        lastKey = ''
        for i in range(len(headMain)):
            tmp = headMain[i].split(':', 1)
            if 2 == len(tmp) and '=?' not in tmp[0][0:3]:
                resultDict[tmp[0]] = tmp[1].strip(
                ) if 'Subject' != tmp[0] else self.__dumpMailBase64(
                    tmp[1].strip())
                lastKey = tmp[0]
                # print lastKey
            else:
                __tmp = headMain[i].strip(
                ) if 'Subject' != lastKey else self.__dumpMailBase64(
                    headMain[i].strip())
                resultDict[lastKey] = resultDict[lastKey] + __tmp
        resultDict['From'] = self.__dumpMailBase64(resultDict['From'].strip())
        return resultDict

# 解析邮件的标题

    def __dumpMailBase64(self, subject_str):
        detail = email.Header.decode_header(subject_str)
        tmp = ''
        # print detail
        for i in detail:
            if None != i[1]:
                tmp = tmp + i[0].decode(i[1]).encode('utf-8')
            else:
                tmp = tmp + i[0]
        # print tmp
        return tmp

# 获取 news head 的字典形式，
# 如果参数id为一个元组或list 则会获取两个元素之间的所有news 的 head,返回list 的字典···[{}]

    def getDictHead(self, id, filePath=None):
        result = []
        if list == type(id) or tuple == type(id):
            if 2 == len(id):
                for i in range(int(id[0]), int(id[1]) + 1):
                    head = self.__getDictHead(i)
                    if None != head:
                        result.append(head)
            else:
                print 'id must be [int,int] or (int,int) or 123 or \'123\'!'
        elif int == type(id):
            result = self.__getDictHead(id)
        else:
            print 'id must be [int,int] or (int,int) or 123 or \'123\'!'
        if None != filePath:
            self.__write(result, filePath)
        else:
            pass
        return result

# 写入文件，字符串，列表， 字典 元组。

    def __write(self, content, filePath):
        f = open(filePath, "w")
        if str == type(content) or int == type(content):
            f.write(content)
        elif list == type(content) or tuple == type(content):
            for i in content:
                f.write(str(i) + "\n")
        elif dict == type(content):
            for k, v in content.items():
                f.write(str(k) + ":" + str(v) + '\n')
        else:
            f.write(content)
        f.close()

# how to use
if __name__ == "__main__":
    # m = SimpEmail("yanglin@aaaaaa.com", "111111Aa", "mail.aaaaaa.com", "25", "yanglin")
    # a = '\tlkjhlkjlkjljljljl\njljlljkjhkjhkj\nhkhkhkkhkhkhkkjhkjkjh'
    # m.sendEmail(["421168852@qq.com","lin_yang@cccc.com"],"hahahah",a,"./getNews.py", ["ccc@aaaaaa.com","ddd@aaaaaa.com"])

    n = GetNews("70.191.90.19", 119)
    resp, count, first, last, name = n.setGroup("aaaa.aaaaa.aaaaaa")

    h = n.getHead(735)
    print h
    print h['Subject']
    # print n.getMainBody(first)
    # n.getSubject(first,last, "./milestone_subject")
    # n.getDate(first, last, './milestone_date')

    n.quitService()
