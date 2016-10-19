import numpy as np
import pandas as pd


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
raw_item_profile = pd.read_csv(data_path+filename_item_profile, sep='\t')
raw_interactions = pd.read_csv(data_path+filename_interactions, sep='\t')
raw_target_users = pd.read_csv(data_path+filename_target_users, sep='\t')
raw_user_profile = pd.read_csv(data_path+filename_user_profile, sep='\t')

unique_users = np.unique(raw_interactions[interactions_user_id])
unique_items = np.unique(raw_interactions[interactions_item_id])

n_users = len(unique_users)
n_items = len(unique_items)

