# -*- coding:utf-8 -*-
import urllib2
import re

'''
    百度贴吧爬虫
    create:2018-01-30
    auther:zengln
'''


class TextTool:
    # 去除 img 标签,7位长空格
    removeImg = re.compile('<img.*?>| {7}|')
    # 删除超链接标签
    removeAddr = re.compile('<a.*?>|</a>')
    # 把换行的标签换位\n
    replaceLine = re.compile('<tr>|<div>|</div>|</p>')
    # 将表格制表<td>替换为\t
    replaceTD = re.compile('<td>')
    # 把段落开头换位\n加空两格
    replacePara = re.compile('<p.*?>')
    # 将换行符或双换行符替换为\n
    replaceBR = re.compile('<br><br>|<br>')
    # 将其余标签剔除
    removeExtraTag = re.compile('<.*?>')

    def replace(self, x):
        x = re.sub(self.removeImg, "", x)
        x = re.sub(self.removeAddr, "", x)
        x = re.sub(self.replaceLine, "\n", x)
        x = re.sub(self.replaceTD, "\t", x)
        x = re.sub(self.replacePara, "\n", x)
        x = re.sub(self.replaceBR, "\n", x)
        x = re.sub(self.removeExtraTag, "", x)
        return x.strip()


class BDTB:

    # 初始化，传入地址,与是否只看楼主参数
    def __init__(self, baseUrl, seeLZ, floorTag):
        self.baseURL = baseUrl
        self.seeLZ = '?see_lz=' + str(seeLZ)
        self.tool = TextTool()
        self.file = None
        self.floor = 1
        self.defaultTitle = u"百度贴吧"
        # 是否写入楼分隔符的标记
        self.floorTag = floorTag

    # 传入页码,获取该页帖子代码
    def getPage(self, pageNum):
        try:
            url = self.baseURL + self.seeLZ + '&pn=' + str(pageNum)
            request = urllib2.Request(url)
            response = urllib2.urlopen(request)
            return response.read()
        except urllib2.URLError, e:
            if hasattr(e, "reason"):
                print u"链接百度贴吧失败, 错误原因", e.reason
                return None

    # 获取帖子标题
    def getTitle(self):
        page = self.getPage(1)
        pattern = re.compile('<h3 class="core_title_txt.*?">(.*?)</h3>', re.S)
        result = re.search(pattern, page)
        if result:
            return result.group(1)
        else:
            return None

    # 获取帖子总页数
    def getPageNum(self):
        page = self.getPage(1)
        pattern = re.compile('<li class="l_reply_num".*?<span class="red">(.*?)</span>', re.S)
        result = re.search(pattern, page)
        if result:
            return result.group(1)
        else:
            return None

    # 获取每一层楼的内容,传入页面内容
    def getContent(self, page):
        pattern = re.compile('<div id="post_content_.*?>(.*?)</div>', re.S)
        items = re.findall(pattern, page)
        contents = []
        for item in items:
            content = "\n" + self.tool.replace(item) + "\n"
            contents.append(content)
        return contents

    def setFileTitle(self, title):
        if title is not None:
            self.file = open(title.decode('utf-8') + ".txt", "w+")
        else:
            self.file = open(self.defaultTitle + ".txt", "w+")

    def writeData(self, contents):
        # 向文件中写入每一楼的信息
        for item in contents:
            if self.floorTag == '1':
                floorLine = "\n" + str(self.floor) + u"----------------------------------------------------------------"
                self.file.write(floorLine)
            self.file.write(item)
            self.floor += 1

    def start(self):
        indexPage = self.getPage(1)
        pageNum = self.getPageNum()
        title = self.getTitle()
        self.setFileTitle(title)
        if pageNum == None:
            print "URL已失效,请换一个地址"
            return
        try:
            print "该帖子共有" + str(pageNum) + "页"
            for i in range(1, int(pageNum) + 1):
                print "正在写入第" + str(i) + "页数据"
                page = self.getPage(i)
                contents = self.getContent(page)
                self.writeData(contents)
        except IOError, e:
            print "写入异常,原因:" + e.message
        finally:
            print "写入任务完成"


code = raw_input("请输入帖子代号\n")
baseURL = 'http://tieba.baidu.com/p/' + str(code)
seeLZ = raw_input("是否只获取楼主发言,是输入1,否输入2\n")
floorTag = raw_input("是否写入楼层信息,是输入1,否输入2\n")
bdtb = BDTB(baseURL, seeLZ, floorTag)
bdtb.start()
