# -*- coding:utf-8 -*-
import urllib2
import re
import os
import sys

'''
    淘宝爬虫
    create:2018-01-31
    auther:zengln
'''


class TBSpider:

    def __init__(self):
        self.siteURL = 'http://mm.taobao.com/json/request_top_list.htm'

    def getPage(self, pageIndex):
        url = self.siteURL + "?page=" + str(pageIndex)
        request = urllib2.Request(url)
        response = urllib2.urlopen(request)
        return response.read().decode('gbk')

    def getContents(self, pageIndex):
        Contents = self.getPage(pageIndex)
        # print Contents
        pattern_str = (
            # 头像地址
            '<div class="pic s60">.*?<img src="(.*?)"'
            # 姓名,个人主页地址
            '.*?<p class="top">.*?<a class="lady-name".*?href="(.*?)".*?>(.*?)</a>'
            # 年龄
            '.*?<em><strong>(.*?)</strong>.*?</em>'
            # 居住地
            '.*?<span>(.*?)</span>'
        )
        pattern = re.compile(pattern_str, re.S)
        items = re.findall(pattern, Contents)
        return items

        # 传入图片地址,文件名,保存单张图片
    def saveImg(self, imagURL, fileName):
        img = urllib2.urlopen(imagURL).read()
        imgFile = open(fileName, "wb")
        imgFile.write(img)
        imgFile.close()

    # 写入文本
    def saveBrief(self, content, name):
        fileName = name + ".txt"
        file = open(fileName, "w+")
        print u"正在保存个人信息,文件名为", fileName
        file.write(content)
        file.close()

    # 创建新目录
    def mkdir(self, path):
        path = path.strip()
        isExists = os.path.exists(path)
        if not isExists:
            os.makedirs(path)
            return True
        else:
            return False

    def start(self, pageIndex):
        items = self.getContents(pageIndex)
        path = "D://test"
        self.mkdir(path)
        for item in items:
            imgURL = "https:" + item[0]
            fileName = item[2] + ".jpg"
            self.saveImg(imgURL, path + "/" + fileName)
            content = (
                    '个人主页地址:' + item[1] +
                    '姓名:' + item[2] +
                    '年龄:' + item[3] +
                    '居住地:' + item[4]
            )
            self.saveBrief(content, path + "/" + item[2])

reload(sys)
sys.setdefaultencoding('utf-8')
tbSpider = TBSpider()
tbSpider.start(1)
