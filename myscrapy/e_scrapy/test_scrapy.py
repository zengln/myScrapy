# -*- coding:utf-8 -*-
import urllib2
import re

'''
    糗事百科爬虫
    created:2018-01-20
'''


class QSBK:

    def __init__(self):

        self.pageIndex = 1
        self.user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64)'
        # 初始化headers
        self.headers = {'User-Agent': self.user_agent}
        # 存放段子的变量,每一个元素是每一页的段子
        self.stories = []
        # 程序是否继续运行的标识
        self.enable = False

    # 传入某一个的索引获取页面代码
    def getPage(self, pageIndex):
        try:
            url = 'http://www.qiushibaike.com/hot/page/' + str(pageIndex)
            # 构建请求的 request
            request = urllib2.Request(url, headers=self.headers)
            response = urllib2.urlopen(request)
            pageCode = response.read().decode('utf-8')
            return pageCode

        except urllib2.URLError, e:
            if hasattr(e, "reason"):
                print u"链接糗事百科失败,错误原因", e.reason
                return None

    # 传入某一个代码,返回本页不带图片的段子列表
    def getPageItems(self, pageIndex):

        pageCode = self.getPage(pageIndex)
        if not pageCode:
            print "页面加载失败...."
            return None

        #  匹配纯文本段子的正则
        pattern_str = (
            # 匹配用户名
            '<div.*?author.*?<h2>(.*?)</h2>'
            # 匹配内容
            '.*?<div class="content.*?<span>(.*?)</span>'
            # 匹配图片
            '.*?<!--.*?-->(.*?)'
            # 匹配点赞数
            '<div class="stats">.*?<i class="number">(.*?)</i>'
        )
        pattern = re.compile(pattern_str, re.S)
        items = re.findall(pattern, pageCode)
        pageStories = []
        print items.__len__()
        for item in items:
            hasImg = re.search("img", item[2])
            if not hasImg:
                replaceBR = re.compile('<br/>')
                text = re.sub(replaceBR, "\n", item[1])
                pageStories.append([item[0].strip(), text.strip(), item[3].strip()])

        return pageStories

    # 加载并提取页面内容, 加入到列表中
    def loadPage(self):
        # 如果当前未看的页数少于 2 页,则加载新一页
        if self.enable == True:
            if len(self.stories) < 2:
                pageStories = self.getPageItems(self.pageIndex)
                if pageStories:
                    self.stories.append(pageStories)
                    self.pageIndex += 1

    # 调用该方法,每次敲回车打印输出一个段子
    def getOneStory(self, pageStories, page):
        for story in pageStories:
            input = raw_input()
            self.loadPage()
            if input == "Q":
                self.enable = False
                return
            print u"第 %d 页\t发布人:%s\t赞:%s\n%s" % (page, story[0], story[2], story[1])

    # 开始方法
    def start(self):
        print u"正在读取糗事百科,按回车查看新段子,Q退出"
        self.enable = True
        self.loadPage()
        nowPage = 0
        while self.enable:
            if len(self.stories) > 0:
                pageStories = self.stories[0]
                nowPage += 1
                del self.stories[0]
                self.getOneStory(pageStories, nowPage)


spider = QSBK()
spider.start()
