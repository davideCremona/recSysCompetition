#!/usr/bin/python
# -*- coding: utf-8 -*-

import pandas as pd

import sys 
import os
sys.path.append(os.path.relpath("../../IMPORTS/files_paths"))
import files_paths
sys.path.append(os.path.relpath("../../IMPORTS/time_statistics"))
from time_stats import *
offset = "../"

"""
leggo norme, le metto in un dizionario user->norm
"""
startTask("Reading Norms")

user_meta = pd.read_csv(offset+files_paths.P_USER_META, sep=',', index_col='user_id')
norms = dict()
for user_id, user_norms in user_meta.iterrows():
    norms[int(user_id)] = float(user_norms['explicit_norm'])

finishTask("Reading Norms")



"""
dizionario con rating medi per ogni utente
"""
startTask("Reading users average ratings")

users = pd.read_csv(offset+files_paths.P_USERS, sep=',', index_col='user_id')
avg_ratings = dict()
for user_id, user_row in users.iterrows():
    avg_ratings[int(user_id)] = float(user_row['average_rating'])

finishTask("Reading users average ratings")



"""
dizionario con, per ogni utente:
    - un    "set": set di item
    - serie "item": rating
    {
        user_id: 
        {
            item_set: set(items)
            <item>: <rating>
            ...
        },
        ...
    }
"""
startTask("Reading URM")

urm = pd.read_csv(offset+files_paths.P_USER_RATING_MATRIX, sep=',')
urm['user_id'] = urm['user_id'].apply(int)
urm['item_id'] = urm['item_id'].apply(int)
urm['avg_rating'] = urm['avg_rating'].apply(float)
grouped_urm = urm.groupby('user_id')
user_ratings = dict()
for user_id, ratings_group in grouped_urm:
    user_ratings[user_id] = dict()
    items_set = set(ratings_group['item_id'])
    user_ratings[user_id]['item_set'] = items_set
    for item, rating in ratings_group.groupby('item_id'):
        user_ratings[user_id][item] = rating['avg_rating']

finishTask("Reading URM")



"""
calcolo delle similarità
"""
startTask("Computing explicit similarity matrix")



finishTask("Computing explicit similarity matrix")

