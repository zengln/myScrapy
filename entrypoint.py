# 由于Scrapy默认不能在IDE中调试,因此需要该文件
from scrapy.cmdline import execute
execute(['scrapy', 'crawl', 'myScrapy'])