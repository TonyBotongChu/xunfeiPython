#!/usr/bin/python3
# -*- coding=utf-8 -*-
import re

def punctuationDelete(rawString):
    '''去除字符串中的中英文标点'''
    newstring = re.sub("[\s+\.\!\/_,$%^*(+\"\']+|[+——！，。？、~@#￥%……&*（）]+", "", rawString)
    return newstring

def getLoginParams():
    filename = "login_params"
    file_open = open(filename, 'r')
    file_content_byte = ""
    try:
        file_content = file_open.read()
        file_content_byte = bytes(file_content, encoding = "utf8")
    except Exception as e:
        print(e)
    finally:
        file_open.close()
        return file_content_byte

if __name__ == "__main__":
    line = "测试。。去除标点。。"
    print(punctuationDelete(line))
