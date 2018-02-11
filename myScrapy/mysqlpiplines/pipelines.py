# -*- coding: utf-8 -*-

# create:2018-02-11
# author:zengln

from .mysql import mySql
from myScrapy.items import MyscrapyItem

class MySpiderPipleLine(object):

    def process_item(self, item, spider):

        if isinstance(item, MyscrapyItem):
            name_id = item['name_id']
            result = mySql.isexists(name_id)
            if result[0] == 1:
                print('该小说记录已存在')
                pass
            else:
                mySql.insert(item['name'], item['author'], item['novelurl'], item['serialstatus'], item['serialnumber'],
                             item['category'], item['name_id'], item['collect_num'], item['click_num'],
                             item['push_num'], item['last_update_time'])
