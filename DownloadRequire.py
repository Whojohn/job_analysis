#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pymysql
import os
import requests
from lxml import etree
import re
import time
from SqlControl import SqlControl
MYSQL_HOSTS = "127.0.0.1"
MYSQL_USER = "root"
MYSQL_PASSWORD = "123456"
MYSQL_PORT = 3306
MYSQL_DB = "job"

head= {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Cache-Control':'max-age=0',
        'Pragma':'no-cache',
        'Host': 'www.lagou.com',
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.110 Safari/537.36"}

mycook={}
#so里面填写seleium获取的cookcie
so=[]
for so in so:
    mycook[so['name']]=so['value']


class this_SqlControl(SqlControl):

    def process_item(self, *item):
        sqlCommand='select '+item[0]+' from lagou'
        self.cur.execute(sqlCommand)
        urls_list=self.cur.fetchall()
        return urls_list



class DownloadRequire(object):

    def download_paper(self):
        document_path=r"C:\Users\John\Desktop\job\each_url_paper"+'\\'
        sql=this_SqlControl()
        t=mycook['Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6']
        mycook['Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6']=str(int(t)+2)
        urls_list=sql.process_item('job_urls')
        if not os.path.isdir(document_path):
            os.makedirs(document_path)
        for x in  urls_list:
            time.sleep(0.5)
            html=requests.get(x[0],headers=head,cookies=mycook)
            selector = etree.HTML(html.text)
            paper=selector.xpath(r'id("job_detail")/dd[contains(@class,"job")]//p/text()')
            file_name="".join([document_path,re.findall(r"[0-9]+",x[0])[0],".txt"])
            with open(file_name,'w',encoding='utf8') as f:
                f.write("\n".join(paper))
        this_SqlControl.kill_sql()


if __name__ == '__main__':
    d=DownloadRequire()
    d.download_paper()