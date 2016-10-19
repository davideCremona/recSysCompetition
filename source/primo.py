import numpy as np
import pandas as pd
import random

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

header_recommended = ['user_id', 'recommended_items']
data = np.empty([len(raw_target_users[0:]['user_id']) , 2], dtype="string")

def selectRandom():
    return raw_item_profile.sample(n=5)

print raw_target_users['user_id'].min()


print selectRandom()['id'].tolist()


for uid in raw_target_users[0:]['user_id']:
    selected = selectRandom()['id'].tolist()
    recommended_items = str(selected[0])+" "+str(selected[1])+" "+str(selected[2])+" "+str(selected[3])+" "+str(selected[4])
    row = [str(uid), recommended_items]
    data = np.vstack([data, row])

np.savetxt(data_path+'submission.csv', data, delimiter=',', fmt="%s")


