# coding=utf-8
from __future__ import unicode_literals
import pandas as pd
import codecs
import os


def make_new_feaature_list(file_path, std_id_list):
    id_value_dict = dict()
    result_list = list()
    with codecs.open(file_path, 'r', 'utf-8') as feature_data_file:
        count = 0
        for feature_data in feature_data_file:
            if count == 0:
                count += 1
                continue
            feature_data_list = feature_data.strip('\n').split(',')
            std_id = str(feature_data_list[0])
            value = str(feature_data_list[1])
            id_value_dict[std_id] = value

    for index in range(len(std_id_list)):
        std_id = str(std_id_list[index])
        if std_id not in id_value_dict:
            value = '0.00'
        else:
            value = id_value_dict[std_id]
        result_list.append(value)
    return result_list

feature_data_dir_path = '../feature_data/'
like_train_file_path = '../train_data/like_train_data.csv'
save_file_path = '../train_data/pre_train_data.csv'

like_train_data = source_data = pd.read_csv(like_train_file_path)

uid_list = like_train_data['uid']
mid_list = like_train_data['mid']
cid_list = like_train_data['cid']
discount_list = like_train_data['discount']
distance_list = like_train_data['distance']
label_list = like_train_data['label']

result_list = list()
title_list = list()
for file_name in os.listdir(feature_data_dir_path):
    file_path = feature_data_dir_path + file_name

    if 'mid' in file_name:
        temp_result_list = make_new_feaature_list(file_path, mid_list)
    elif 'uid' in file_name:
        temp_result_list = make_new_feaature_list(file_path, uid_list)
    else:
        continue

    title_list.append(file_name.split('.')[0])
    result_list.append(temp_result_list)

feature_list = list()
for index in range(len(cid_list)):
    uid = uid_list[index]
    mid = mid_list[index]
    cid = cid_list[index]
    discount = discount_list[index]
    distance = distance_list[index]

    temp_list = list()
    temp_list.append(str(uid))
    temp_list.append(str(mid))
    temp_list.append(str(cid))
    temp_list.append(str(discount))
    temp_list.append(str(distance))

    feature_list.append(temp_list)

for temp_val_list in result_list:
    for index in range(len(temp_val_list)):
        temp_feature_list = feature_list[index]
        temp_feature_list.append(temp_val_list[index])


for index in range(len(feature_list)):
    temp_list = feature_list[index]
    label = label_list[index]
    temp_list.append(str(label))


with codecs.open(save_file_path, 'w', 'utf-8') as save_file:
    save_file.write('uid,mid,cid,discount,distance,' + ','.join(title_list) + ',label' + '\n')
    for val_list in feature_list:
        save_file.write(','.join(val_list) + '\n')

