#!/usr/bin/python2
#-*- coding: utf-8 -*-

import os
import sys
import time
import logging
import email
from nntplib import NNTP
from smtplib import SMTP
from email.header import Header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEBase
from email.mime.multipart import MIMEMultipart

#定义输出日志
logging.basicConfig(level=logging.INFO,
                    format='--%(levelname)s - \n%(message)s')
logging.disable(logging.INFO)


# Send 异常类
class SendError(Exception):
    '''发送异常类'''

    def __init__(self, discription):
        self.discription = discription
        super(SendError, self).__init__()

    def __str__(self):
        return self.discription


# 一个发送邮件和news的类
class SendMailNews(object):
    '''send mail and news!'''

    def __init__(self, fromAddr, subject, bodyContent):
        '''初始化类'''
        self.fromAddr = self.__checkFromAddr(fromAddr)
        self.subject = Header(self.__checkSubject(subject), 'utf-8')
        self.body = self.__checkBody(bodyContent)
        self.headKey = {
            'From': fromAddr,
            "Subject": self.subject,
            'body': self.body
        }

    def connectMail(self, password, mailServer, serverPort='25'):
        self.smtpObj = SMTP()
        self.smtpObj.connect(mailServer, serverPort)
        self.smtpObj.login(self.fromAddr.strip().split('@')[0], password)

    def connectNews(self, server, port=119):
        self.nntpObj = NNTP(server, port)

    def __checkFromAddr(self, fromAddr):
        if isinstance(fromAddr, str):
            fromAddr_ = fromAddr.strip().split('@')
            if 2 != len(fromAddr_) or '' == fromAddr_[0] or '' == fromAddr_[1]:
                raise SendError('from Address: %s is not standardized!' %
                                fromAddr)
            else:
                return fromAddr

    def __checkToAddr(self, toAddrList):
        addr_str = ''
        if toAddrList or isinstance(toAddrList, list):
            for i in toAddrList:
                i_ = i.strip().split('@')
                if 2 != len(i_) or '' == i_[0] or '' == i[1]:
                    raise SendError('accept Address: %s is not standardized!' %
                                    i)
                else:
                    addr_str = addr_str + '%s<%s>,' % (i_[0], i)
        else:
            raise SendError(
                '\n****accept Address can\'t null!***\n***def setMail(self, toAddrList, CcAddrList = []), toAddrList is not a list!***\n--please check!--'
            )
        return addr_str.strip(',')

    def __checkSubject(self, subject):
        if isinstance(subject, str):
            return subject
        else:
            raise SendError(
                '\n***subject must be a string!***\n--please ceck--')

    def __checkCCAddr(self, CcAddrList):
        addr_str = ''
        if isinstance(CcAddrList, list):
            for i in CcAddrList:
                i_ = i.strip().split('@')
                if 2 != len(i_) or '' == i_[0] or '' == i[1]:
                    raise SendError('accept Address: %s is not standardized!' %
                                    i_)
                else:
                    addr_str = addr_str + '%s<%s>,' % (i_[0], i)
        else:
            raise SendError(
                '\n***def setMail(self, toAddrList, CcAddrList = []), CcAddrList is not a list!***\n--please check!--'
            )
        return addr_str.strip(',')

    def __checkBody(self, bodyContent):
        if isinstance(bodyContent, str):
            # return "%s\n________________________\n%s" %( bodyContent, self.fromAddr)
            return bodyContent
        else:
            raise SendError(
                '\n***body content must be a strint!***\n--please check!--')

    def __checkNewsGroups(self, groupList):
        if isinstance(groupList, list):
            return ','.join(groupList)
        else:
            raise SendError(
                '\n***def setNews(self, server, newsGroup_list),newsGroup_list must be list!***\n--please check!--'
            )

    def __setAttachContent(self, attachment_path, contype):
        data = open(attachment_path, 'rb')
        maintype, subtype = contype.split('/', 1)
        file_msg = MIMEBase(maintype, subtype)
        file_msg.set_payload(data.read())
        data.close()
        return file_msg

    def __setAttachHeader(self, file_msg, attachment_path):
        basename = os.path.basename(attachment_path)
        file_msg.add_header('Content-Disposition',
                            'attachment',
                            filename=basename)
        # file_msg.add_header('Content-Disposition', 'attachment', filename = ('utf-8','Chinese', basename))
        email.encoders.encode_base64(file_msg)
        self.main_msg.attach(file_msg)

    def setAttachment(self,
                      attachment_path=None,
                      contype='application/octet-stream'):
        if None != attachment_path:
            attachment_path = os.path.normpath(attachment_path)
            file_msg = self.__setAttachContent(attachment_path, contype)
            if not hasattr(self, 'main_msg'):
                self.main_msg = MIMEMultipart()
            else:
                pass
            self.__setAttachHeader(file_msg, attachment_path)
        else:
            pass

    def setMail(self, toAddrList, CcAddrList=[]):
        toAddr = self.__checkToAddr(toAddrList)
        CcAddr = self.__checkCCAddr(CcAddrList)
        self.toAddrsList = toAddrList + CcAddrList
        self.mail = {'To': toAddr, 'Cc': CcAddr}
        self.headKey.update(self.mail)

    def setNews(self, newsGroup_list, **kwag):
        group = self.__checkNewsGroups(newsGroup_list)
        kwag['Newsgroups'] = group
        self.groups = newsGroup_list
        self.news = kwag
        self.headKey.update(self.news)

    def formatMIME(self):
        text_msg = MIMEText(self.headKey.pop('body', ''), 'plain', 'utf-8')
        # email.encoders.encode_7or8bit(text_msg)
        if hasattr(self, 'main_msg'):
            self.main_msg.attach(text_msg)
            for i in self.headKey:
                self.main_msg[i] = self.headKey[i]
            text_msg['date'] = email.utils.formatdate()
            # print(self.main_msg)
            return self.main_msg
        else:
            for i in self.headKey:
                text_msg[i] = self.headKey[i]
            text_msg['date'] = email.utils.formatdate()
            return text_msg

    def __checkSendMail(self):
        if hasattr(self, 'mail') and hasattr(self, 'smtpObj'):
            return True
        elif not hasattr(self, 'mail') and not hasattr(self, 'smtpObj'):
            return False
        else:
            raise SendError(
                '\n***two must be called:\nconnectMail(self, password, mailServer, serverPort = \'25\')\nsetMail(self, toAddrList, CcAddrList = [])'
            )

    def __checkSendNews(self):
        if hasattr(self, 'news') and hasattr(self, 'nntpObj'):
            return True
        elif not hasattr(self, 'news') and not hasattr(self, 'nntpObj'):
            return False
        else:
            raise SendError(
                '\n***two must be called:\nconnectNews(self, server, port = 119)\nsetNews(self, server, newsGroup_list)'
            )

    def __returnOpenObj(self, MIMEObj):
        fw = open('./NEWS_Source', 'w')
        fw.write(MIMEObj.as_string())
        fw.close()
        fr = open('./NEWS_Source', 'r')
        return fr

    def doSend(self):
        MIMEObj = self.formatMIME()
        if self.__checkSendMail():
            logging.info('>>>>>>>>>>>> SEND MAIL......\n')
            logging.info('From:\n%s\n' % self.fromAddr)
            logging.info('To:\n%s\n' % '\n'.join(self.toAddrsList))
            logging.info('As_string:\n%s\n' % MIMEObj.as_string())
            self.smtpObj.sendmail(self.fromAddr, self.toAddrsList,
                                  MIMEObj.as_string())
            self.smtpObj.quit()
            logging.info('SEND MAIL SUCCESS<<<<<<<<<<<')
        if self.__checkSendNews():
            logging.info('>>>>>>>>>>>> SEND NEWS......')
            logging.info('From:\n%s\n' % self.fromAddr)
            logging.info('Newsgroups:\n%s\n' % '\n'.join(self.groups))
            logging.info('As_string:\n%s\n' % MIMEObj.as_string())
            fr = self.__returnOpenObj(MIMEObj)
            self.nntpObj.post(fr)
            self.nntpObj.quit()
            fr.close()
            logging.info('SEND NEWS SUCCESS<<<<<<<<<<<')


# 以下是使用方法
if __name__ == '__main__':
    # 创建发送邮件 新闻类的对象
    # 传入参数---发件人地址，标题，正文
    s = SendMailNews('yanglin@aaaaa.com', '不服来战！', '我就发你能咋地。。。。。。。。。。。。。!')

    # 接收人地址，是一个list类型，抄送人地址一样
    toAddr = ['yanglin@aaaaa.com', 'shanzhifeng@aaaaa.com']
    # cc = ['shanzhifeng@aaaaa.com']

    # 接收的新闻组，是一个list类型
    grou = ['ccccc.aaaaa.jjjjj', 'aaaaa.kkkkk.ddddd']

    # 设置邮件
    # 传入参数： 接收人list，抄送人list_可有可无
    s.setMail(toAddr)

    # 设置附件
    # 传入参数：附件地址，附件类型（contype = 'application/octet-stream'）
    s.setAttachment('./invalid_unknown.xlsx')
    s.setAttachment('./Build-服务器统计表.xls')

    # 连接邮件服务器
    # 传入参数：密码，邮件服务器地址，端口号
    s.connectMail('111111Aa', 'mail.aaaaa.com', '25')

    # 连接新闻组服务器
    # 传入参数：服务器地址，端口号
    s.connectNews('192.28.29.28')

    # 设置新闻组
    # 传入参数：新闻组名list，和其他的头。
    # 例：（grou，{'References': <762c8e9f-91c0-0591-bb1a-6c88d395d15d@aaaaa.com>， 'In-Reply-To': <762c8e9f-91c0-0591-bb1a-6c88d395d15d@aaaaa.com>}）
    # 后面的可以不用，新闻要挂在某条的下面就需要各键的值是被挂news的  message-ID
    # References 是挂着
    # In-Reply-To：是回复
    s.setNews(grou)

    # 发送
    s.doSend()
