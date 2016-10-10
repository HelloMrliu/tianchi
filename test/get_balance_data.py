# coding=utf-8
from __future__ import unicode_literals
import pandas as pd
import codecs
import os


train_data_path = '../train_data/pre_train_data.csv'
data = pd.read_csv(train_data_path)

label_list = data['label']

pos_index_list = list()
neg_index_list = list()

index = 0
for index in range(len(label_list)):
    if str(label_list[index]) == '1':
        pos_index_list.append(index)
    else:
        if index % 7 == 0:
            neg_index_list.append(index)
        index += 0

pos_list = list()
neg_list = list()

pos_list = data.ix[pos_index_list]
neg_list = data.ix[neg_index_list]

print len(pos_list)
print len(neg_list)

new_list = pos_list.append(neg_list)
print len(new_list)

new_list.to_csv('../train_data/train_data.csv', index=False)
