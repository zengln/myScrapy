# -*- coding:utf-8 -*-

# create:2018-02-08
# auther:zengln

import re
import scrapy
from scrapy.http import Request
from bs4 import BeautifulSoup
from myScrapy.items import MyscrapyItem


class MyScrapy(scrapy.Spider):

    name = 'myScrapy'
    base_url = 'http://www.23us.so'


    def start_requests(self):
        yield Request(self.base_url, self.parse)

    # 从主页提取每个分站的地址
    def parse(self, response):
        # print(response.text)
        # pattern_str = '<li class="m_ml">.*?<li><a href="(.*?)".*?</a></li>'
        # pattern = re.compile(pattern_str, re.S)
        # items = re.findall(pattern, response.text)
        # print(items.__len__())
        # for item in items:
        #     print(item)
        mainmenu = BeautifulSoup(response.text, 'lxml').find('div', class_='main m_menu').find_all('a')
        pattern_str = '<a href="(.*?)">(.*?)</a>'
        pattern = re.compile(pattern_str, re.S)
        items = re.findall(pattern, str(mainmenu))
        for index, item in enumerate(items):
            suburl = item[0]
            # self.url_name = item[1]
            if index != 0 and index != 10 and index != 11:
                newurl = self.base_url + suburl
                yield Request(newurl, self.subparse)
        # for index, urlstring in enumerate(mainmenu):
        #     suburl = re.findall(pattern, str(urlstring)).group[0]
        #     self.url_name = re.findall(pattern, str(urlstring))[1]
        #     if index != 0:
        #         newurl = self.base_url + suburl
        #         yield Request(newurl, self.subparse)

    # 爬取分站中的文章链接,与当前页数,总页数
    def subparse(self, response):
        # print(response.text)
        # title = BeautifulSoup(response.text, 'lxml').find('head').find_all('title')
        # pattern = re.compile(r'<title>(.*?)</title>', re.S)
        # file_name = re.search(pattern, str(title)).group(1)
        # print(self.url_name)
        # dir = "D://test/"
        # if os.path.exists(dir):
        #     print("mkdir is exist")
        # else:
        #     os.mkdir(dir)
        # file = open(dir + str(file_name) + ".txt", 'w+')
        # file.write(response.text)
        # file.close()

        # 获取当前页数与总页数
        page_pattern_str = ('<em id="pagestats">(.*?)/.*?</em>.*?'
                            '<a href="(.*?)_.*?html" class="first">.*?'
                            '<a.*?class="last">(.*?)</a>')
        page_pattern = re.compile(page_pattern_str, re.S)
        page_result = re.search(page_pattern, response.text)
        currentpage = page_result.group(1)
        currenturl = page_result.group(2)
        totalpage = page_result.group(3)
        # print(currentpage, currenturl, totalpage)

        # 获取当前页的小说链接,小说名,小说id
        pattern_str = '<td class="L"><a href="(.*?)">(.*?)</a></td>''[\n]<td class="L">.*?'
        pattern = re.compile(pattern_str, re.S)
        items = re.findall(pattern, response.text)

        for item in items:
            # 获取小说 id
            name_id = re.search(r'http.*?/xiaoshuo/(.*?).html', item[0]).group(1)
            yield Request(item[0], self.getvalue, meta={'name': item[1], 'name_id': name_id, 'novelurl': item[0]})

        nextpage = int(currentpage) + 1
        if nextpage <= int(totalpage):
            yield Request(currenturl + "_" + str(nextpage) + ".html", self.subparse)

    def getvalue(self, response):
        item = MyscrapyItem()
        # print(response.text)
        result = BeautifulSoup(response.text, 'lxml').find('table', id='at').find_all('td')
        # print(result)
        # print(result[4].get_text())
        item['category'] = result[0].get_text().replace('\xa0', '').encode('utf-8')
        item['author'] =result[1].get_text().replace('\xa0', '').encode('utf-8')
        item['serialstatus'] = result[2].get_text().replace('\xa0', '').encode('utf-8')
        item['collect_num'] = result[3].get_text().replace('\xa0', '')
        item['serialnumber'] = result[4].get_text()[:-1].replace('\xa0', '')
        item['last_update_time'] = result[5].get_text().replace('\xa0', '')
        item['click_num'] = result[6].get_text().replace('\xa0', '')
        item['push_num'] = result[9].get_text().replace('\xa0', '')
        item['name'] = response.meta['name'].encode('utf-8')
        item['name_id'] = response.meta['name_id']
        item['novelurl'] = response.meta['novelurl']
        return item
