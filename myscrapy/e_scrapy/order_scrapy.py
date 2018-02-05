# -*- coding:utf-8 -*-
import urllib
import urllib2
import cookielib
import re

'''
    获取淘宝订单爬虫
    create:2018-02-02
    auther:zengln
'''

class OrderScrapy:

    def __init__(self):
        self.loginURL = 'https://login.taobao.com/member/login.jhtml'
        # 代理 IP 地址,防止自己的 IP 被封禁
        self.proxyURL = 'http://120.193.146.97:843'
        # 登录 post 数据时发送的头部信息
        self.loginHeaders = {
            'content-type': 'application/x-www-form-urlencoded',
            'origin': 'https://login.taobao.com',
            'referer': 'https://login.taobao.com/member/login.jhtml',
            'user-agent': ('ozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                           'Chrome/64.0.3282.140 Safari/537.36')
        }
        # 用户名
        self.username = 'your username'
        # ua 字符串
        self.ua = ('you ua')

        self.password2 = ('your password2')

        self.um_token = 'your um_token'
        self.ncoToken = 'your ncoToken'

        self.post = {
            'ua': self.ua,
            'um_token': self.um_token,
            'TPL_password_2': self.password2,
            'TPL_username': self.username,
            'TPL_password': '',
            'ncoSig': '',
            'ncoSessionid': '',
            'ncoToken': self.ncoToken,
            'slideCodeShow': 'false',
            'useMobile': 'false',
            'lang': 'zh_CN',
            'loginsite': '0',
            'newlogin': '0',
            'TPL_redirect_url': '',
            'from': 'tb',
            'fc': 'default',
            'style': 'default',
            'css_style': '',
            'keyLogin': 'false',
            'qrLogin': 'true',
            'newMini': 'false',
            'newMini2': 'false',
            'tid': '',
            'loginType': '3',
            'minititle': '',
            'minipara': '',
            'pstrong': '',
            'sign': '',
            'need_sign': '',
            'islgnore': '',
            'full_redirect': '',
            'sub_jump': '',
            'popid': '',
            'callback': '',
            'guf': '',
            'not_duplite_str': '',
            'need_user_id': '',
            'poy': '',
            'gvfdcname': '10',
            'gvfdcre': '',
            'from_encoding': '',
            'sub': '',
            'loginASR': '1',
            'loginASRSuc': '1',
            'allp': '',
            'oslanguage': 'zh-CN',
            'sr': '1366*768',
            'osVer': '',
            'naviVer': 'chrome|64.0328214',
            'osACN': 'Mozilla',
            'osAV': ('5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari'
                     '/537.36'),
            'osPF': 'Win32',
            'miserHardInfo': '',
            'appkey': '00000000',
            'nickLoginLink': '',
            'mobileLoginLink': 'https://login.taobao.com/member/login.jhtml?useMobile=true',
            'showAssistantLink': ''
        }
        # 将 POST 的数据进行编码转换
        self.postData = urllib.urlencode(self.post)
        # 设置代理
        self.proxy = urllib2.ProxyHandler({'http': self.proxyURL})
        # 设置 cookie
        self.cookie = cookielib.LWPCookieJar()
        # 设置 cookie 处理器
        self.cookieHandler = urllib2.HTTPCookieProcessor(self.cookie)
        # 设置登录时用到的 opener
        self.opener = urllib2.build_opener(self.cookieHandler, self.proxy, urllib2.HTTPHandler)


    def login(self):
        request = urllib2.Request(self.loginURL, self.postData, self.loginHeaders)
        response = self.opener.open(request)
        content = response.read().decode('gbk')
        print content
        # pattern_str = '&&trid=(.*?)&asid=(.*?)"'
        # pattern = re.compile(pattern_str, re.S)
        # items = re.findall(pattern, content)
        # for item in items:
        #     self.trid = item[0]
        #     self.asid = item[1]
        #
        # self.get = {
        # "logtype": '1',
        # "title": '%u9875%u9762%u8DF3%u8F6C%u4E2D',
        # "pre": 'https://login.taobao.com/member/login.jhtml?',
        # "cache": 'cache',
        # "scr": '1366x768',
        # "cna": 'cna',
        # "nick": 'nickname',
        # "spm-cnt": 'spm-cnt',
        # "category": '',
        # "uidaplus": '',
        # "aplus": '',
        # "yunid": '',
        # "fe1ef81eeeaeb": '',
        # "trid": self.trid,
        # "asid": self.asid,
        # "p": '1',
        # "o": 'win10',
        # "b": 'chrome64',
        # "s": '1366x768',
        # "w": 'webkit',
        # "ism": 'pc',
        # 'lver': "8.1.1",
        # "jsver":'aplus_std',
        # "thw": 'cn',
        # "tag": '1',
        # "stag": '-1',
        # "lstag": '-1'
        # }
        #
        # test_url = 'https://log.mmstat.com/v.gif?' + urllib.urlencode(self.get)
        # print test_url
        # test_request = urllib2.Request(test_url)
        # self.opener.open(test_request)
        pattern_str2 = 'top.location.href = "(.*?)";'
        pattern2 = re.compile(pattern_str2, re.S)
        result = re.search(pattern2, content)
        myURL = result.group(1)
        myRequest = urllib2.Request(myURL, headers=self.loginHeaders)
        myResponse = self.opener.open(myRequest)
        myContent = myResponse.read().decode('gbk')
        print myContent

        # pattern_str = '<script src="(.*?)"></script>'
        # pattern = re.compile(pattern_str, re.S)
        # items = re.findall(pattern, content)
        # print items.__len__()
        # i = 0
        # for item in items:
        #     jumpRequest = urllib2.Request(item, headers=self.loginHeaders)
        #     response = self.opener.open(jumpRequest)
        #     jumpContent = response.read().decode('gbk')
        #     file = open("D://test/file"+str(i), "w+")
        #     file.write(jumpContent)
        #     file.close()
        #     i += 1




orderScrapy = OrderScrapy()
orderScrapy.login()

