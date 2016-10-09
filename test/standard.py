# coding=utf-8
from __future__ import unicode_literals
import pandas as pd
import codecs


online_train_file_path = '../../tianchi_data/source_data/online_train.csv'
offline_train_file_path = '../../tianchi_data/source_data/offline_train.csv'
offline_test_file_path = '../../tianchi_data/source_data/offline_test.csv'

small_count_dict = dict()
all_count_dict = dict()


def get_column_info(source_file_path, column_name, need_action):
    source_data = pd.read_csv(source_file_path)
    column_id_list = source_data[column_name]
    cid_list = source_data['cid']
    date_received_list = source_data['data_received']
    date_list = source_data['date']
    if need_action == 0:
        return column_id_list, cid_list, date_received_list, date_list
    else:
        action_list = source_data['action']
        return column_id_list, cid_list, date_received_list, date_list, action_list


def get_time_diff(less_time, big_time):
    month_diff = int(big_time[-4:-2]) - int(less_time[-4:-2])

    if month_diff == 0:
        return int(big_time[-2:]) - int(less_time[-2:])
    else:
        return int(big_time[-2:]) - int(less_time[-2:]) + 30 * month_diff


def count_bc_number_offline(column_id_list, cid_list, date_received_list, date_list, time_limit):
    for index in range(len(column_id_list)):
        column_id = column_id_list[index]
        cid = cid_list[index]
        date_received = date_received_list[index]
        date = date_list[index]
        if cid != 'null' and date != 'null':
            time_diff = get_time_diff(date_received, date)
            if time_diff <= time_limit:
                if column_id in small_count_dict:
                    small_count_dict[column_id] += 1
                else:
                    small_count_dict[column_id] = 1
            else:
                pass

        if date_list[index] != 'null':
            if column_id in all_count_dict:
                all_count_dict[column_id] += 1
            else:
                all_count_dict[column_id] = 1
        else:
            pass


def count_bc_number_online(column_id_list, cid_list, date_received_list, date_list, action_list, time_limit, action_number):
    for index in range(len(column_id_list)):
        column_id = column_id_list[index]
        cid = cid_list[index]
        date_received = date_received_list[index]
        date = date_list[index]
        action = action_list[index]
        if action == action_number:
            if cid != 'null' and date != 'null':
                time_diff = get_time_diff(date_received, date)
                if time_diff <= time_limit:
                    if column_id in small_count_dict:
                        small_count_dict[column_id] += 1
                    else:
                        small_count_dict[column_id] = 1
                else:
                    pass

            if date_list[index] != 'null':
                if column_id in all_count_dict:
                    all_count_dict[column_id] += 1
                else:
                    all_count_dict[column_id] = 1
            else:
                pass

        else:
            pass


def cal_percentage(divide_num, divider_num):
    per = float(divide_num) / divider_num

    if divider_num == 1:
        per *= 0.7
    elif divider_num == 2:
        per *= 0.8
    elif divider_num == 3:
        per *= 0.9

    if divide_num == 0 and divider_num == 1:
        per = 0.25
    if divide_num == 0 and divider_num == 2:
        per = 0.15
    if divide_num == 0 and divider_num == 3:
        per = 0.1

    return per


def save_result_into_file(feature_save_file_path):
    with codecs.open(feature_save_file_path, 'w', 'utf-8') as feature_save_file:
        feature_save_file.write('mid,use_coupon_percentage' + '\n')
        for mid in small_count_dict:
            per = cal_percentage(small_count_dict[mid], all_count_dict[mid])
            feature_save_file.write(str(mid) + ',' + str("%.2f" % per) + '\n')
        for mid in all_count_dict:
            if mid not in small_count_dict:
                per = 0.000
                feature_save_file.write(str(mid) + ',' + str("%.2f" % per) + '\n')


time_lim = 30
column_name = 'uid'

column_id_list, cid_list, date_received_list, date_list = get_column_info(offline_train_file_path, column_name, 0)
count_bc_number_offline(column_id_list, cid_list, date_received_list, date_list, time_lim)

column_id_list, cid_list, date_received_list, date_list, action_list = get_column_info(online_train_file_path, column_name, 1)
count_bc_number_online(column_id_list, cid_list, date_received_list, date_list, action_list, time_lim, 1)

feature_save_file_path = '../feature_data/uid_use_coupon_percentage_' + str(time_lim) + '.csv'
save_result_into_file(feature_save_file_path)
