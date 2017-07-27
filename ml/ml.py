#!/usr/bin/env python
# -*- coding: utf-8 -*-
from SqlControl import SqlControl
import re
import random
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
import jieba
# from sklearn import metrics
# from sklearn.naive_bayes import BernoulliNB
# from sklearn.linear_model import SGDClassifier


class MySqlControl(SqlControl):
    def process_item(self, *item):
        sqlCommand = 'select ' + item[0] + ' from lagou'+ ' where job_require like '+item[1]
        self.cur.execute(sqlCommand)
        urls_list = self.cur.fetchall()
        return urls_list


def load_data_train(sql,job_list,word_detail):
    # '''导入文本数据集'''
    job_list_with_tunple = sql.process_item('job_require',word_detail)
    word_title="".join(re.findall(r"[^r\"'%s].+?",word_detail))
    leng=len(job_list_with_tunple)

    if leng/467<=0.08:
        for x in job_list_with_tunple:
            # 没有分词
            # job_list.append((x[0],word_title))
            word_cut=" ".join(list(jieba.cut(x[0])))
            job_list.append((word_cut,word_title))
    else:
        x=int((leng/467)*0.8*467)
        num=random.sample(range(leng),x)
        for x in num:
            # job_list.append((job_list_with_tunple[x][0],word_title))
            word_cut=" ".join(list(jieba.cut(job_list_with_tunple[x][0])))
            job_list.append((word_cut, word_title))


# load_data_train参数传入的为取数据具体函数


def load_all_train(load_data_train=load_data_train,chain=None):
    job_list=[]
    sql = MySqlControl()
    for x in chain:
        load_data_train(sql,job_list,x)
    # 上面循环相当于下面代码
    # load_data_train(sql,job_list,r'"%数据%分析%"')
    # load_data_train(sql,job_list,r"'%数据%挖掘%'")
    # load_data_train(sql,job_list,r"'%数据库%'")
    # load_data_train(sql,job_list,r"'%项目%经理%'")
    # load_data_train(sql,job_list,r"'%产品%经理%'")
    # load_data_train(sql,job_list,r"'%运营%'")
    # load_data_train(sql,job_list,r"'%销售%'")
    # load_data_train(sql,job_list,r"'%数据库%开发%'")
    # load_data_train(sql,job_list,r"'%数据%开发%'and job_require NOT LIKE '%数据库%'")
    # load_data_train(sql,job_list,r"'%收集%'and job_require LIKE '%采集%'")
    # load_data_train(sql,job_list,r"'%大数据%'")
    sql.kill_sql()
    random.shuffle(job_list)
    return job_list


def load_data(sql,job_list,word_detail):
    '''导入文本数据集'''
    job_list_with_tunple = sql.process_item('job_require',word_detail)
    word_title="".join(re.findall(r"[^r\"'%s].+?",word_detail))
    a=0
    for x in job_list_with_tunple:
        word_cut = " ".join(list(jieba.cut(x[0])))
        job_list.append((word_cut,word_title))


def train_and_test_data(data_,chain):
    # 训练集和测试集的比例为7:3
    train_=load_all_train(chain=chain)
    train_data_ = [each[0] for each in train_]
    train_target_ = [each[1] for each in train_]

    test_data_ = [each[0] for each in data_]
    test_target_ = [each[1] for each in data_]

    return train_data_, train_target_, test_data_, test_target_

k=0.001
for x in range(30000):
    chain=[r'"%数据%分析%"',r"'%数据%挖掘%'",r"'%数据库%'",r"'%项目%经理%'",r"'%产品%经理%'",r"'%运营%'",r"'%销售%'",r"'%数据库%开发%'",r"'%数据%开发%'and job_require NOT LIKE '%数据库%'",
           r"'%收集%'and job_require LIKE '%采集%'",r"'%大数据%'"]
    data = load_all_train(load_data_train=load_data,chain=chain)
    train_data, train_target, test_data, test_target = train_and_test_data(data,chain)
    #sgd
    # nbc = Pipeline([
    #     ('vect', TfidfVectorizer()),
    #     ('clf', SGDClassifier( loss="hinge",
    # n_iter=50,
    # alpha=0.00001,
    # fit_intercept=True)),
    # ])
    #
    # MultinomialNB
    bad_dict = ["专家", "视频", "初级", "项目", "实习生", "国际", "阿里", "广州", "总监", "主管", "工程师", "高级",  "资深", "专员", "方向",
                "(", ")", "/", "java", "hadoop", "spark", "mysql"]
    # bad_dict=[]
    nbc = Pipeline([
        ('vect', TfidfVectorizer(stop_words=bad_dict)),
        ('clf', MultinomialNB(alpha=k)),
    ])
    nbc.fit(train_data, train_target)  # 训练我们的多项式模型贝叶斯分类器
    predict = nbc.predict(test_data)  # 在测试集上预测结果
    count = 0  # 统计预测正确的结果个数
    for left, right in zip(predict, test_target):
        if left == right:
            count += 1
    print(count / len(test_target))