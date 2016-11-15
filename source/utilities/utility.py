#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Collaborative filtering recommender system
"""
import pandas as pd
import numpy as np
"""
package settings
"""
pd.options.mode.chained_assignment = None  # default='warn'


"""
Variabili costanti (path dei file, ...)
"""
data_path = '../data/'
filename_interactions = 'interactions.csv'
filename_active_item = 'active_item_profile.csv'
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
"""
raw_user_profile = pd.read_csv(data_path+filename_user_profile, sep='\t', index_col='id')
"""

print raw_target_users.shape

unique_items_ids = np.unique(raw_interactions[interactions_user_id])

print unique_items_ids.shape