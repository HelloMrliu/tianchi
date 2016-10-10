# coding=utf-8
from __future__ import unicode_literals
import xgboost as xgb
import pandas as pd
import codecs
import time
from sklearn.cross_validation import train_test_split

train_data_path = '../train_data/train_data.csv'
test_data_path = '../train_data/test_data.csv'
save_file_path = '../result_data/result_'


param = {
    'max_depth': 5,
    'eta': 0.1,
    'silent': 1,
    'objective': 'binary:logistic',
    'eval_metric': 'auc',
    'scale_pos_weight': 2,
    'subsample': 0.75,
    'colsample_bytree': 0.75,
    'alpha': 10,
    'lambda': 10,
    'nthread': 5
}

data = pd.read_csv(train_data_path)
test_data = pd.read_csv(test_data_path)

train_data, val_data = train_test_split(data, test_size=0.15)

train_uid = train_data['uid']
train_mid = train_data['mid']
train_cid = train_data['cid']

val_uid = val_data['uid']
val_mid = val_data['mid']
val_cid = val_data['cid']

test_uid = test_data['uid']
test_mid = test_data['mid']
test_cid = test_data['cid']
test_date_received = test_data['date_received']

train_x = train_data.drop(['uid', 'mid', 'cid', 'label'], axis=1)
train_y = train_data['label']

val_x = val_data.drop(['uid', 'mid', 'cid', 'label'], axis=1)
val_y = val_data['label']

test_x = test_data.drop(['uid', 'mid', 'cid', 'date_received'], axis=1)

train_matrix = xgb.DMatrix(train_x, label=train_y)
val_matrix = xgb.DMatrix(val_x, label=val_y)
test_matrix = xgb.DMatrix(test_x)

watchlist = [(train_matrix,'train'),(val_matrix,'val')]


model = xgb.train(param, train_matrix, num_boost_round=2000, evals=watchlist)

test_y = model.predict(test_matrix)

uid_list = list(test_uid)
mid_list = list(test_mid)
cid_list = list(test_cid)
date_received_list = list(test_date_received)
y_list = list(test_y)


current_time = time.strftime('%Y%m%d%H%M%S')
with codecs.open(save_file_path + str(current_time) + '.csv', 'w', 'utf-8') as save_file:
    #save_file.write('User_id,Coupon_id,Date_received,Probability\n')
    for index in range(len(y_list)):
        save_file.write(str(uid_list[index]) + ',' + str(cid_list[index]) + ',' + str(date_received_list[index]) + ',' + str("%.4f" % float(y_list[index])) + '\n')
