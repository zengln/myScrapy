# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# create:2018-02-08
# auther:zengln

import scrapy

class MyscrapyItem(scrapy.Item):
    # 小说的名字
    name = scrapy.Field()
    # 作者
    author = scrapy.Field()
    # 小说地址
    novelurl = scrapy.Field()
    # 状态
    serialstatus = scrapy.Field()
    # 连载字数
    serialnumber = scrapy.Field()
    # 文章类别
    category = scrapy.Field()
    # 小说编号
    name_id = scrapy.Field()
    # 收藏数
    collect_num = scrapy.Field()
    # 总点击数
    click_num = scrapy.Field()
    # 总推荐数
    push_num = scrapy.Field()
    # 最新更新日期
    last_update_time = scrapy.Field()
    pass
