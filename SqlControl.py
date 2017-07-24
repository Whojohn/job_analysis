#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pymysql
MYSQL_HOSTS = "127.0.0.1"
MYSQL_USER = "root"
MYSQL_PASSWORD = "123456"
MYSQL_PORT = 3306
MYSQL_DB = "job"


class SqlControl(object):
    def __init__(self):
        self.conn= pymysql.connect(user = MYSQL_USER,password= MYSQL_PASSWORD,host =MYSQL_HOSTS,database=MYSQL_DB,use_unicode=True, charset="utf8")#创建链接
        self.cur=self.conn.cursor()

    def process_item(self, *item):
        sqlCommand='select '+item[0]+' from lagou'
        self.cur.execute(sqlCommand)
        urls_list=self.cur.fetchall()
        return urls_list

    def kill_sql(self):
        self.cur.close()
        self.conn.close()
