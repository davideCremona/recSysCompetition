#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Collaborative filtering recommender system
"""
import pandas as pd
import numpy as np
import math

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
raw_item_profile = pd.read_csv(data_path + filename_item_profile, sep='\t', index_col='id')
raw_interactions = pd.read_csv(data_path + filename_interactions, sep='\t')
raw_target_users = pd.read_csv(data_path + filename_target_users, sep='\t', index_col='user_id')
raw_user_profile = pd.read_csv(data_path + filename_user_profile, sep='\t')

"""
filtro item attivi
"""
is_active = raw_item_profile['active_during_test'] == 1
active_items = raw_item_profile[is_active]


"""
data preprocessing
"""
maxTimestamp = raw_interactions['created_at'].max()
minTimestamp = raw_interactions['created_at'].min()

raw_interactions['created_at'] = raw_interactions['created_at'].apply(lambda x: np.interp(x, [minTimestamp, maxTimestamp], [0, 1]))


grupped_interaction = raw_interactions[['user_id', 'item_id', 'interaction_type','created_at']]
grupped_interaction_user = grupped_interaction.groupby(['user_id'])
grupped_interaction_item = grupped_interaction.groupby(['item_id'])
grouped_interaction_user_item = grupped_interaction.groupby(['user_id','item_id'])

def getInteractionsForItems(item):
    try:
        interactions = grupped_interaction_item.get_group((item))
        return interactions
    except KeyError:
        #print "No interactions with item: "+str(item)
        return None

def getInteractionsForUser(user):
    try:
        interactions = grupped_interaction_user.get_group((user))
        return interactions
    except KeyError:
        #print "No interactions for: "+str(target_user)
        return None

def raw_frequency(rating, interactions):
    return float(float(len(interactions[interactions['interaction_type']==rating]))/float(len(interactions)))

def tf(rating, interactions, mode="boolean"):
    if mode == "boolean":
        return rating in interactions['interaction_type'].unique()
    if mode == "frequency":
        return raw_frequency(rating, interactions)
    else:
        print "Not implemented"

def averageRatingOfUser(interactions):
    if interactions is not None:
        # average weighted by td-idf for each possible rating:
        # avg = 
        pass
    else:
        return np.NaN

new_interactions = dict()

def getItemsRatings(items):
    items_dict = dict()
    grouped_items = items.groupby('item_id').aggregate(np.average)
    grouped_items = grouped_items.drop('user_id',axis=1)
    grouped_items= grouped_items.drop('created_at', axis=1)
    return grouped_items

for user, row in grupped_interaction_user:
   new_interactions[user] = getItemsRatings(row) 

print new_interactions





"""

raw_user_profile['average_rating'] = raw_user_profile.apply(lambda row: averageRatingOfUser(getInteractionsForUser(row['user_id'])), axis=1)

print raw_user_profile['average_rating'].head(5)

pd.to_csv(data_path + "user_profile_avg_rating.csv", sep='\t', encoding='utf-8')

"""

"""
def idf(rating, ensemble):
    number_of_groups = len(ensemble)
    number_of_groups_contains = 0
    for index, row in ensemble:
        if rating in row['interaction_type'].unique():
            number_of_groups_contains += 1
    return float(number_of_groups)/float(number_of_groups_contains)

# pre-computed
idfs_users = {1:math.log(1.00085401959), 2:math.log(6.01917479884), 3:math.log(4.21053892216)}

for i in idfs_users:
    print idfs_users[i]
"""
