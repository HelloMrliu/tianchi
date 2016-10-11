# coding=utf-8
from __future__ import unicode_literals
import pandas as pd
import os
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.cross_validation import train_test_split
import codecs


train_data_path = '../train_data/train_data.csv'
val_data_path = '../train_data/val_data.csv'
test_data_path = '../train_data/test_data.csv'
save_file_path = '../result_data/result_'

data = pd.read_csv(train_data_path)
val_data = pd.read_csv(val_data_path)
test_data = pd.read_csv(test_data_path)

train_data, temp_data = train_test_split(data, test_size=0.1)

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

weight_dict = {
    0: 0.3,
    1: 0.7
}

print 'start'
#model = RandomForestClassifier(n_estimators=500, max_depth=None, min_samples_split=2, class_weight=weight_dict).fit(train_x, train_y)
model = GradientBoostingClassifier(n_estimators=300, learning_rate=0.5, max_depth=3, random_state=0).fit(train_x, train_y)
print model.score(val_x, val_y)
predict_y = model.predict(val_x)

right_val = 0
for index in range(len(predict_y)):
    if str(val_y[index]) == '1':
        if str(predict_y[index]) == str(val_y[index]):
            right_val += 1
        print str(predict_y[index]) + ', ' + str(val_y[index])
print right_val

prob = model.predict_proba(test_x)
index = 0
for val in prob:
    print val[1]
    if index > 1000:
        break
    index += 1
