#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import pymysql
import pandas as pd
import matplotlib as mpl
from SqlControl import SqlControl
#初始化数据库连接，设置matplotlib中文字体（不设置中文会乱码）
mpl.rcParams['font.sans-serif'] = ['SimHei']
mpl.rcParams['font.serif'] = ['SimHei']


class ThisSqlcontrol(SqlControl):

    def process_item(self, *item):
        sqlCommand='select '+item[0]+' from lagou_copy'
        self.cur.execute(sqlCommand)
        urls_list=self.cur.fetchall()
        return urls_list
    # def insert(self,url_number,txt):
    #     sqlCommand='insert into txt VALUES ("%s","%s")'%(url_number,txt)
    #     self.cur.execute(sqlCommand)
    #     self.conn.commit()


sql = ThisSqlcontrol()
job_list_with_tunple = sql.process_item('job_require')
sql.kill_sql()
job_list=[]
for x in job_list_with_tunple:
    job_list.append(x[0])
#long的作用是为了后面能够利用groupby，groupby必须2个轴以上才能统计出结果，而long是什么值不重要，后面count会覆盖掉
long=list(range(len(job_list)))
df=pd.DataFrame({"word":job_list,"key":long})
df=df.groupby(df['word']).count().reset_index()
df1=df[df['key']>3].reset_index()
del df1['index']
#df1w为处理后，df为处理前。 df处理后会丢失一定的数据（而这一部分的数据分类太费劲所以丢掉）
df1.plot(kind="bar",x=df1['word'])
df.plot(kind="bar",x=df['word'])
print("stop")

