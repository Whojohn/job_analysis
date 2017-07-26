#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
from SqlControl import SqlControl
import pandas as pd
import jieba
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import HashingVectorizer
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans, MiniBatchKMeans

def loadDataset():
    '''导入文本数据集'''
    sql = SqlControl()
    job_list_with_tunple = sql.process_item('job_require')
    sql.kill_sql()
    job_list = []
    for x in job_list_with_tunple:
        job_list.append(x[0])
    after_tf = []
    for x in job_list:
        #temp = [x]
        #temp.append(jieba.analyse.extract_tags(x, topK=3, allowPOS=("n", "v")))
        temp=jieba.cut(x)
        f_temp=[]
        bad_dict=["专家","视频","初级","项目","实习生","国际","阿里","广州","经理","总监","主管","工程师","高级","大","资深","专员","方向","(",")","/","java","hadoop","spark","mysql"]
        for x in temp:
            if x not in bad_dict:
                f_temp.append(x)
                f_temp.append(" ")
        after_tf.append("".join(f_temp))
        #after_tf.append(",")
    #dataset="".join(after_tf)
    dataset=after_tf
    return dataset


def transform(dataset, n_features=1000):
    vectorizer = TfidfVectorizer(max_df=0.5, max_features=n_features, min_df=3, use_idf=True)
    X = vectorizer.fit_transform(dataset)
    return X, vectorizer


def train(X, vectorizer, true_k=1, minibatch=False, showLable=False):
    # 使用采样数据还是原始数据训练k-means，
    if minibatch:
        km = MiniBatchKMeans(n_clusters=true_k, init='k-means++', n_init=1,
                             init_size=1000, batch_size=1000, verbose=False)
    else:
        km = KMeans(n_clusters=true_k, init='k-means++', max_iter=300, n_init=1,
                    verbose=False)
    km.fit(X)
    job=[]
    if showLable:
        print("Top terms per cluster:")
        order_centroids = km.cluster_centers_.argsort()[:, ::-1]
        terms = vectorizer.get_feature_names()
        print(vectorizer.get_stop_words())
        for i in range(true_k):
            print("Cluster %d:" % i, end='')
            for ind in order_centroids[i, :3]:
                print(' %s' % terms[ind], end='')
                job.append(terms[ind])
            print()
    result = list(km.predict(X))
    print('Cluster distribution:')
    print(dict([(i, result.count(i)) for i in result]))
    #return  -km.score(X)
    return result,-km.score(X)


def test():
    '''测试选择最优参数'''
    dataset = loadDataset()
    print("%d documents" % len(dataset))
    X, vectorizer = transform(dataset, n_features=500)
    true_ks = []
    scores = []
    for i in range(3, 15, 1):
        score = train(X, vectorizer, true_k=i) / len(dataset)
        print(i, score)
        true_ks.append(i)
        scores.append(score)
    plt.figure(figsize=(8, 4))
    plt.plot(true_ks, scores, label="error", color="red", linewidth=1)
    plt.xlabel("n_features")
    plt.ylabel("error")
    plt.legend()
    plt.show()


def out():
    '''在最优参数下输出聚类结果'''
    dataset = loadDataset()
    X, vectorizer = transform(dataset, n_features=500)
    # result,score = train(X, vectorizer, true_k=8, showLable=True) / len(dataset)
    # print(score)
    result=train(X,vectorizer,true_k=16,showLable=True,minibatch=False)
    print(result)


#test()
out()