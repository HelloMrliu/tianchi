# coding=utf-8
from __future__ import unicode_literals
import pandas as pd
import codecs


def get_time_diff(less_time, big_time):
    month_diff = int(big_time[-4:-2]) - int(less_time[-4:-2])

    if month_diff == 0:
        return int(big_time[-2:]) - int(less_time[-2:])
    else:
        return int(big_time[-2:]) - int(less_time[-2:]) + 30 * month_diff


online_train_file_path = '../../tianchi_data/source_data/online_train.csv'
offline_train_file_path = '../../tianchi_data/source_data/offline_train.csv'
offline_test_file_path = '../../tianchi_data/source_data/offline_test.csv'


def get_id_list(source_file_path):
    source_data = pd.read_csv(source_file_path)
    uid_list = source_data['cid']
    '''
    mid_list = source_data['mid']
    cid_list = source_data['cid']
    discount_list = source_data['discount']
    distance_list = source_data['distance']
    date_received_list = source_data['date_received']
    '''

    result_list = list()
    for result in uid_list:
        result_list.append(str(result))
    return result_list


online_train_set = set(get_id_list(online_train_file_path))
offline_train_set = set(get_id_list(offline_train_file_path))
offline_test_set = set(get_id_list(offline_test_file_path))

print len(offline_test_set)
print len(offline_train_set)
print len(offline_test_set & offline_train_set)


'''
print len(online_train_set | offline_train_set)
print len(online_train_set & offline_train_set)
print len(offline_test_set & offline_train_set)


all_data = pd.read_csv(offline_train_file_path)
id_list = all_data['cid']

train_index_list = list()
val_index_list = list()

for index in range(len(id_list)):
    if index % 10 == 0:
        val_index_list.append(index)
    else:
        train_index_list.append(index)

train_list = all_data.ix[train_index_list]
val_list = all_data.ix[val_index_list]

print len(train_list)
print len(val_list)


train_list.to_csv('../train_data.csv', index=False)
val_list.to_csv('../val_data.csv', index=False)
'''