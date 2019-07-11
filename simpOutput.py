#!/usr/bin/python
#coding: utf-8

import sys
import os
import time


# 自定义输出类。
class simpleOutput():
    def __init__(self, sleepTime=0.2):
        self.chooseOut = 0
        self.sleepTime = sleepTime
        self.outCharLen = 0
        self.signDict = {"0": " / ", "1": " - ", "2": " \\ "}

# 调用此函数必须给出四个参数：在标记（／）前的输出，在标记后的输出，结束控制和结束的标记
# 在循环中调用此方法，会在同一行动态输出：
#   str_frontsign此处标记str_aftersign
#   str_overcontrol == str_overSign 时会独立输出一行，不会被替换的一行。

    def customOut(self, str_frontSign, str_afterSign, str_overControl,
                  str_overSign):
        if "0" == self.chooseOut:
            self.__customOut(str_frontSign,
                             str_afterSign,
                             str_overControl,
                             str_overSign,
                             index_="1")
        elif "1" == self.chooseOut:
            self.__customOut(str_frontSign,
                             str_afterSign,
                             str_overControl,
                             str_overSign,
                             index_="2")
        else:
            self.__customOut(str_frontSign,
                             str_afterSign,
                             str_overControl,
                             str_overSign,
                             index_="0")
        time.sleep(self.sleepTime)
        if str_overControl == str_overSign:
            self.__customOut(str_frontSign, str_afterSign, str_overControl,
                             str_overSign)
        else:
            return

    def __customOut(self,
                    str_frontSign,
                    str_afterSign,
                    str_overControl,
                    str_overSign,
                    index_=None):
        if index_ is not None:
            sys.stdout.write(" " * self.outCharLen + "\r")
            sys.stdout.write(str_frontSign + self.signDict[index_] +
                             str_afterSign + "\r")
            self.outCharLen = len(str_frontSign + " / " + str_afterSign)
            self.chooseOut = index_
        else:
            sys.stdout.write(" " * self.outCharLen + "\r")
            sys.stdout.write(str_frontSign + " : " + str_afterSign + "\n")
            self.outCharLen = len(str_frontSign + " / " + str_afterSign)
        sys.stdout.flush()

# 此方法动态输出百分比，接受三个参数：字符串说明，浮点当前分子，字符串百分比样式

    def percentOut(self, str_explainOut, float_currentOut, str_style):
        str_currentOut = str(float_currentOut)
        if 0 == self.chooseOut:
            sys.stdout.write(" " * self.outCharLen + "\r")
            sys.stdout.write(str_explainOut + " / " + str_currentOut +
                             str_style + "\r")
            self.outCharLen = len(str_explainOut + " / " + str_currentOut +
                                  str_style)
            self.chooseOut = 1
            sys.stdout.flush()
        elif 1 == self.chooseOut:
            sys.stdout.write(" " * self.outCharLen + "\r")
            sys.stdout.write(str_explainOut + " - " + str_currentOut +
                             str_style + "\r")
            self.outCharLen = len(str_explainOut + " - " + str_currentOut +
                                  str_style)
            self.chooseOut = 2
            sys.stdout.flush()
        else:
            sys.stdout.write(" " * self.outCharLen + "\r")
            sys.stdout.write(str_explainOut + " \\ " + str_currentOut +
                             str_style + "\r")
            self.outCharLen = len(str_explainOut + " \\ " + str_currentOut +
                                  str_style)
            self.chooseOut = 0
            sys.stdout.flush()
        time.sleep(self.sleepTime)
        if 100 == float_currentOut:
            sys.stdout.write(" " * self.outCharLen + "\r")
            sys.stdout.write(str_explainOut + " : " + str(float_currentOut) +
                             str_style + "\n")
            sys.stdout.flush()
            return
        elif 100 < float_currentOut:
            sys.stdout.write(" " * self.outCharLen + "\r")
            sys.stdout.write(str_explainOut + " : " + str(float_currentOut) +
                             str_style + "\n")
            sys.stdout.write("BIG ERROR : current persent greater than 100%\n")
            sys.exit(1)
        else:
            return


# how to use
if __name__ == "__main__":
    a = simpleOutput()
    i = 0
    while i <= 100:
        a.customOut("Now ", str(i), "%", "hggg")
        i += 1
