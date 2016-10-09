# coding=utf-8
from __future__ import unicode_literals
import pandas as pd
import codecs


online_train_file_path = '../../tianchi_data/source_data/online_train.csv'
offline_train_file_path = '../../tianchi_data/source_data/offline_train.csv'
offline_test_file_path = '../../tianchi_data/source_data/offline_test.csv'

feature_save_file_path = '../feature_data/mid_use_coupon_percentage.csv'

offline_train_data = pd.read_csv(offline_train_file_path)
online_train_data = pd.read_csv(online_train_file_path)
mall_use_coupon_dict = dict()
mall_all_dict = dict()


mid_list = offline_train_data['mid']
date_received_list = offline_train_data['data_received']
date_list = offline_train_data['date']

for index in range(len(mid_list)):
    if date_received_list[index] != 'null' and date_list[index] != 'null':
        if mid_list[index] in mall_use_coupon_dict:
            mall_use_coupon_dict[mid_list[index]] += 1
        else:
            mall_use_coupon_dict[mid_list[index]] = 1
    else:
        pass

    if date_list[index] != 'null':
        if mid_list[index] in mall_all_dict:
            mall_all_dict[mid_list[index]] += 1
        else:
            mall_all_dict[mid_list[index]] = 1
    else:
        pass

print len(mall_use_coupon_dict)

mid_list = online_train_data['mid']
action_list = online_train_data['action']
date_received_list = online_train_data['data_received']
date_list = online_train_data['date']

for index in range(len(mid_list)):
    if action_list[index] == 1:
        if date_received_list[index] != 'null' and date_list[index] != 'null':
            if mid_list[index] in mall_use_coupon_dict:
                mall_use_coupon_dict[mid_list[index]] += 1
            else:
                mall_use_coupon_dict[mid_list[index]] = 1
        else:
            pass

        if date_list[index] != 'null':
            if mid_list[index] in mall_all_dict:
                mall_all_dict[mid_list[index]] += 1
            else:
                mall_all_dict[mid_list[index]] = 1
        else:
            pass


with codecs.open(feature_save_file_path, 'w', 'utf-8') as feature_save_file:
    feature_save_file.write('mid,use_coupon_percentage')
    for mid in mall_use_coupon_dict:
        per = float(mall_use_coupon_dict[mid]) / mall_all_dict[mid]
        feature_save_file.write(str(mid) + ',' + str("%.2f"%per) + '\n')
    for mid in mall_all_dict:
        if mid not in mall_use_coupon_dict:
            per = 0.000
            feature_save_file.write(str(mid) + ',' + str("%.2f" % per) + '\n')


