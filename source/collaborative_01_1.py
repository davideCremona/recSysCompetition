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
filename_target_users_1_chunk = 'target_users_2.csv'
filename_target_users_2_chunk = 'target_users_1.csv'
filename_user_profile = 'user_profile.csv'

interactions_user_id = 'user_id'
interactions_item_id = 'item_id'


"""
Lettura dei file csv
""" 
raw_item_profile = pd.read_csv(data_path + filename_item_profile, encoding='utf-8', sep='\t')
raw_interactions = pd.read_csv(data_path + filename_interactions, encoding='utf-8', sep='\t')
raw_target_users = pd.read_csv(data_path + filename_target_users, encoding='utf-8', sep='\t', index_col="user_id")
raw_user_profile = pd.read_csv(data_path + filename_user_profile, encoding='utf-8', sep='\t')

"""
user-profile preprocessing

def nanReplace(value):
    if math.isnan(value):
        return -1
    else:
        return value

def intPreproc(data, column):
    data[column] = data[column].apply(nanReplace)
    data[column] = data[column].apply(int)

raw_user_profile = raw_user_profile.set_index(['user_id'])
raw_user_profile['jobroles'] = raw_user_profile['jobroles'].apply(lambda x: str(x).split(','))
intPreproc(raw_user_profile,'career_level')
intPreproc(raw_user_profile,'region')
intPreproc(raw_user_profile,'experience_n_entries_class')
intPreproc(raw_user_profile,'experience_years_experience')
intPreproc(raw_user_profile,'experience_years_in_current')
intPreproc(raw_user_profile,'edu_degree')
#raw_user_profile['edu_fieldofstudies'] = raw_user_profile['edu_fieldofstudies'].apply(lambda x: nanReplace(x))
#raw_user_profile['edu_fieldofstudies'] = raw_user_profile['edu_fieldofstudies'].apply(lambda x: str(x).split(','))

print raw_user_profile.head()

"""

"""
filtro item attivi
"""
is_active = raw_item_profile['active_during_test'] == 1
active_items = raw_item_profile[is_active]

"""
interactions preprocessing
"""
maxTimestamp = raw_interactions['created_at'].max()
minTimestamp = raw_interactions['created_at'].min()

# normalizzazione del timestamp da 0 a 1
raw_interactions['created_at'] = raw_interactions['created_at'].apply(lambda x: np.interp(x, [minTimestamp, maxTimestamp], [0, 1]))

# id unici degli utenti
users = np.unique(raw_interactions.index)
# id unici degli items
items = np.unique(raw_interactions['item_id'])

int_gro = raw_interactions.groupby(by=['user_id'])

print int_gro
