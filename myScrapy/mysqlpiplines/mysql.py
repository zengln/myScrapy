# coding: utf-8 -*-

# create:2018-02-11
# author:zengln

import pymysql
from myScrapy import settings

MYSQL_HOSTS = settings.MYSQL_HOSTS
MYSQL_USER = settings.MYSQL_USER
MYSQL_PASSWORD = settings.MYSQL_PASSWORD
MYSQL_PORT = settings.MYSQL_PORT
MYSQL_DB = settings.MYSQL_DB

# 打开数据库连接
mysql_db = pymysql.connect(host=MYSQL_HOSTS, port=MYSQL_PORT, user=MYSQL_USER, password=MYSQL_PASSWORD, db=MYSQL_DB, charset='utf8')

# 获取操作游标
cursor = mysql_db.cursor()

class mySql:

    @classmethod
    def insert(cls, name, author, novelurl, status, number, category, novelid, collect, click, push, lastupdate):
        insert_sql = ('INSERT INTO novel_test '
                        '(`name`,`author`,`novelurl`,`status`,`number`,`category`,`novelid`,`collect`,`click`,`push`,`lastupdate`)'
                        ' VALUES (%(name)s,%(author)s,%(novelurl)s,%(status)s,%(number)s,%(category)s,%(novelid)s,%(collect)s,%(click)s,%(push)s,%(lastupdate)s)'
                      )
        value = {
            'name': name,
            'author': author,
            'novelurl': novelurl,
            'status': status,
            'number': number,
            'category': category,
            'novelid': novelid,
            'collect': collect,
            'click': click,
            'push': push,
            'lastupdate': lastupdate
        }

        cursor.execute(insert_sql, value)
        mysql_db.commit()

    @classmethod
    def isexists(cls, novelid):
        exists_sql = 'SELECT EXISTS(SELECT 1 FROM novel_test WHERE novelid=%(novelid)s)'
        value = {
            'novelid': novelid
        }
        cursor.execute(exists_sql, value)
        return cursor.fetchall()[0]
