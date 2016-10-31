#!/usr/bin/python
# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd

pd.options.mode.chained_assignment = None  # default='warn'

"""
Variabili costanti (path dei file, ...)
"""
data_path = '../data/'
filename_interactions = 'interactions.csv'
filename_item_profile = 'item_profile.csv'
filename_target_users = 'target_users.csv'
filename_user_profile = 'user_profile.csv'

interactions_user_id = 'user_id'
interactions_item_id = 'item_id'

"""
Lettura dei file csv
"""
raw_item_profile = pd.read_csv(data_path + filename_item_profile, sep='\t')
raw_interactions = pd.read_csv(data_path + filename_interactions, sep='\t')
raw_target_users = pd.read_csv(data_path + filename_target_users, sep='\t')
raw_user_profile = pd.read_csv(data_path + filename_user_profile, sep='\t')

unique_items_ids = np.unique(raw_interactions[interactions_item_id])

active_items = raw_item_profile[raw_item_profile['active_during_test'] == 1]
filtered_items_ids = active_items['id']
filtered_interactions = raw_interactions[raw_interactions['item_id'].isin(filtered_items_ids)]

maxTimestamp = filtered_interactions['created_at'].max()
minTimestamp = filtered_interactions['created_at'].min()

filtered_interactions['created_at'] = filtered_interactions['created_at'].apply(lambda x: np.interp(x, [minTimestamp, maxTimestamp], [0, 1]))
filtered_interactions['scored_interaction'] = filtered_interactions['interaction_type'] * filtered_interactions['created_at']


def getScore(item_id):
    interactions_for_item = filtered_interactions[filtered_interactions['item_id'] == item_id]
    return interactions_for_item['scored_interaction'].sum()


active_items['score'] = active_items['id'].apply(lambda x: getScore(item_id=x))

to_recommend = active_items.sort(['score'], ascending=0).head()['id'].tolist()
data = np.empty([len(raw_target_users[0:]['user_id']), 2], dtype="string")

for uid in raw_target_users[0:]['user_id']:
    recommended_items = str(to_recommend[0]) + " " + str(to_recommend[1]) + " " + str(to_recommend[2]) + " " + str(to_recommend[3]) + " " + str(to_recommend[4])
    row = [str(uid), recommended_items]
    data = np.vstack([data, row])

np.savetxt(data_path + 'submission_02.csv', data, delimiter=',', fmt="%s")
