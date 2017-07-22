#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pandas as pd
from pandas import Series as sr, DataFrame as df
import jieba.posseg  as pseg
from SqlControl import SqlControl
import re


def seperate(dic):
    document_path = r"C:\Users\John\Desktop\job\each_url_paper" + '\\'
    sql = SqlControl()
    urls_list = sql.process_item('job_urls')
    sql.kill_sql()
    for x in urls_list:
        txt_number=re.findall(r"[0-9]+", x[0])[0]+".txt"
        file_path="".join([r"C:\Users\John\Desktop\job\each_url_paper","\\",txt_number])
        with open(file_path, encoding='utf8') as f:
            data1 = f.read()
        l = len(data1)
        df1 = df(columns=['word', 'type'])
        words = pseg.cut(data1)  #分词
        a = 0
        for t in words:
            df2 = pd.DataFrame([[t.word, t.flag]], columns=['word', 'type'])
            a=a+1
            df1 = df1.append(df2, ignore_index=True)
            # df3=df1.groupby(['word']).count().reset_index()
            # print(df3)
        no_duplicate_set=set(df1[df1['type'] == "eng"]['word'].tolist())
        for x in no_duplicate_set:
            if x not in dic:
                dic[x] = 1
            else:
                dic[x] = dic[x]+ 1
    return dic

def job_need(d):
    df = pd.DataFrame(columns=["key", "value"])
    a = 0
    for x in d:
        temp_df = pd.DataFrame({"key": x, "value": int(d[x])}, index=[a])
        df = df.append(temp_df, ignore_index=True)
        a = a + 1
        print(a)
    df = df[df['value'] > 5].reset_index()
    del df['index']
    df.plot(kind='barh', x=df['key'])

#结果  df1[df1['type']=='eng'].drop_duplicates() df1[df1['type']=='eng'].drop_duplicates().count()[0]
#统计eng关键字df1[df1['type']=="eng"]['word'].tolist()
if __name__ == '__main__':
    dic={}
    dic=seperate(dic)
    job_need(dic)
    print(dic)

