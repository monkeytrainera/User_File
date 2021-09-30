# -*- coding: utf-8 -*-
"""
Created on Thu Sep 30 19:33:06 2021

@author: k
"""
import pandas as pd
import os
import re
import jieba

###############设置路径########
path = os.getcwd()
raw_data_path = path + r'\data'
processed_data_path = path + r'\processed_data'

folder = os.path.exists(processed_data_path)
if not folder:
    os.makedirs(processed_data_path)
    print('creat new folder:processed_data')
    print('folder processed_data prepared!')
else:
    print('folder processed_data prepared!')

    
###############导入停用词########
with open(raw_data_path + '\\' + 'stopwords.txt', 'r', encoding='utf-8') as f:
  stopwords = f.readlines()

###############定义数据处理器，作用是清洗数据#####
def processor(x_lst):
  new_lst = []
  noise_pattern = re.compile("|".join(["http\S+", '\d+'])) #去除链接和数字

  for x in x_lst:    
    clean_x = re.sub(noise_pattern, "", x)
    word_lst = []
    for word in jieba.cut(clean_x):
      if len(word) > 1 and word not in stopwords:  #分词，去除停用词和长度小于2的词
        word_lst.append(word)
    s = ' '.join(word_lst)
    new_lst.append(s)
  return new_lst 

###############定义数据处理函数，作用是读取、处理、保存数据########
def DataProcess(file_name, train = True):
    with open(raw_data_path + '\\' + file_name, 'r', encoding='utf-8') as f:
        raw_data = f.readlines() 
        
    x = []
    
    if train == True:   
        y1 = []
        y2 = []
        y3 = [] 
        for data in raw_data:
            data_lst = data.split('###')
            y1.append(data_lst[2])
            y2.append(data_lst[4])
            y3.append(data_lst[6])
            x.append(data_lst[8])
        x = processor(x)
        df = pd.DataFrame({ 'QueryList' : x, 'Age' : y1, 'Gender' : y2, 'Education' : y3})
        df.to_csv(processed_data_path + '\\' + file_name, index=False)
    else:
        for data in raw_data:
            data_lst = data.split('###')
            x.append(data_lst[-1])
        x = processor(x)
        df = pd.DataFrame({ 'QueryList' : x})
        df.to_csv(processed_data_path + '\\' + file_name, index=False)       

###########处理数据############
DataProcess('train.csv', train = True)
DataProcess('test.csv', train = False)






