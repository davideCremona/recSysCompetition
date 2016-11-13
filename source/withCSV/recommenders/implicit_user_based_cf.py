#!/usr/bin/python
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import math
import time
from datetime import datetime

K = 25

"""
leggo sim matrix
"""
print "-------------------------"
print "Start Processing Similarity Matrix"
now = datetime.now()
time_start = time.mktime(now.timetuple())


sim_matrix = pd.read_csv("../../../data/similarity_matrix_user_user.csv", sep=',')
sim_matrix['user_1'] = sim_matrix['user_1'].apply(int)
sim_matrix['user_2'] = sim_matrix['user_2'].apply(int)
indexed_matrix = sim_matrix.set_index(['user_1','user_2'])

def sim(u1, u2):
    try:
        return indexed_matrix.get_value((u1,u2), 'similarity', takeable=False)
    except KeyError:
        return 0.0

now = datetime.now()
time_finish = time.mktime(now.timetuple())
print "Finish Processing Similarity Matrix in "+str(time_finish-time_start)


"""
calcolo somma similarity
"""
sim_sum = dict()
knn_user = dict()
user_sim_groups = sim_matrix.groupby('user_1')
for user, group in user_sim_groups:
    sorted_group = group.sort_values(by='similarity', ascending=False)
    knn_user[user] = sorted_group[['user_2','similarity']].head(K)
    sim_sum[user] = sum(sorted_group['similarity'].head(K))


"""
Calcolo dizionario di items per ogni utente
"""
urm_file = "../../../data/fromSQL/user_rating_matrix.csv"
print "-------------------------"
print "Start Processing URM"
now = datetime.now()
time_start = time.mktime(now.timetuple())

raw_urm = pd.read_csv(urm_file, sep=',')
raw_urm['user_id'] = raw_urm['user_id'].apply(int)
raw_urm['item_id'] = raw_urm['item_id'].apply(int)
indexed_urm = raw_urm.set_index(['user_id', 'item_id'])

def rating_user_item(user, item):
    try:
        indexed_urm.get_value((user,item), 'rating', takeable=False)
        return 1
    except KeyError:
        return 0

# calcolo dizionario di item per ogni utente (items con cui ha intergito l'utente)
user_grouped = raw_urm.groupby('user_id')
interactios_for_user = dict()
for user_id, interactions in user_grouped:
    interactios_for_user[user_id] = set(interactions['item_id'])


now = datetime.now()
time_finish = time.mktime(now.timetuple())
print "Finish Processing URM in "+str(time_finish-time_start)


"""
calcolo active items
"""
raw_item_profile = pd.read_csv("../../../data/item_profile.csv", sep='\t')
active_items = raw_item_profile[raw_item_profile['active_during_test']==1]
active_items = active_items.set_index('id')

active_items_id_set = set(active_items.index)


"""
raccomandazioni
"""
target_users = pd.read_csv("../../../data/target_users.csv", sep="\t", index_col = "user_id")
submission = pd.read_csv("../../../data/target_users.csv", sep='\t', index_col="user_id")
top_popular = ["2778525","1244196","1386412","278589","657183"]
submission['recommended_items'] = ' '.join(top_popular) # standard top popular

print "-------------------------"
print "Start Recommendations"
now = datetime.now()
time_start = time.mktime(now.timetuple())
recommendations_list = list()
j=0
for target_user in target_users.index:
    
    if j%100 == 0:
        print "Mancano: "+str(2500-j)

    if target_user in knn_user.keys():

        items_leaderboard = dict()

        # devo prendere tutti gli item con cui hanno interagito i primi k utenti
        knn_users = knn_user[target_user]['user_2']
        items = set()
        for other_user in knn_users:
            items = items.union(interactios_for_user[other_user])

        items = active_items_id_set.intersection(items)
        items = items - interactios_for_user[target_user]

        for item in items:
            nominator = 0
            for index, sim_row in knn_user[target_user].iterrows():
                nominator += rating_user_item(sim_row['user_2'], item) * sim_row['similarity']
                items_leaderboard[item] = nominator/sim_sum[target_user]

        sorted_leaderboard = sorted(items_leaderboard, key=items_leaderboard.get)
        to_recommend = sorted_leaderboard[:5]
        to_recommend = [str(i) for i in to_recommend]

        to_recommend_set = set(to_recommend)
        top_pop_set = set(top_popular)

        if len(to_recommend) < 5:
            diff = top_pop_set - to_recommend_set.intersection(top_pop_set)
            to_recommend.extend(list(diff))

        to_recommend = to_recommend[:5]
        submission.set_value(target_user, 'recommended_items', ' '.join(to_recommend))

    j += 1

now = datetime.now()
time_finish = time.mktime(now.timetuple())
print "Finish Recommendations in "+str(time_finish-time_start)

submission.to_csv("../../../data/submission_03_02_02.csv", sep=",")

