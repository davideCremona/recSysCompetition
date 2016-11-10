#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Collaborative filtering recommender system
"""
import pandas as pd
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
raw_item_profile = pd.read_csv(data_path + filename_item_profile, sep='\t')
raw_interactions = pd.read_csv(data_path + filename_interactions, sep='\t')
"""
raw_target_users = pd.read_csv(data_path+filename_target_users, sep='\t', index_col='user_id')
raw_user_profile = pd.read_csv(data_path+filename_user_profile, sep='\t', index_col='id')
"""

"""
filtro item attivi
"""
is_active = raw_item_profile['active_during_test'] == 1
active_items = raw_item_profile[is_active]


"""
data preprocessing
"""


def nanReplace(career):
    if math.isnan(career):
        return int(0)
    else:
        return career




active_items['tags'] = active_items['tags'].apply(lambda x: str(x).split(','))
active_items = active_items.drop('latitude', axis=1)
active_items = active_items.drop('longitude', axis=1)
active_items = active_items.drop('created_at', axis=1)
active_items = active_items.drop('active_during_test', axis=1)
active_items = active_items.drop('title', axis=1)
active_items['career_level'] = active_items['career_level'].apply(lambda x: nanReplace(x)).astype(int)
active_items['discipline_id'] = active_items['discipline_id'].apply(lambda x: nanReplace(x)).astype(int)
active_items['industry_id'] = active_items['industry_id'].apply(lambda x: nanReplace(x)).astype(int)
active_items['region'] = active_items['region'].apply(lambda x: nanReplace(x)).astype(int)
active_items['employment'] = active_items['employment'].apply(lambda x: nanReplace(x)).astype(int)




"""
items similarity
"""


def titleSim(title1, title2):
    return "not implemented yet"


def careerSim(career1, career2):
    return career1 == career2


def disciplineSim(discipline1, discipline2):
    return discipline1 == discipline2


def industrySim(industry1, industry2):
    return industry1 == industry2


def countrySim(country1, country2):
    return country1 == country2


# to use only with items that have country as "de"
def regionSim(region1, region2):
    return region1 == region2


# it's really important?
def positionSim(latitude1, longitude1, latitude2, longitude2):
    return "not implemented yet"


def employmentSim(employment1, employment2):
    return employment1 == employment2


# this is important, implementation of jaccard distance.
def tagsSim(tags1, tags2):
    setTags1 = set(tags1.item())
    setTags2 = set(tags2.item())
    intersection_cardinality = len(setTags1.intersection(setTags2))
    cardinality_tags1 = len(setTags1)
    cardinality_tags2 = len(setTags2)
    den = cardinality_tags1 + cardinality_tags2 - intersection_cardinality
    return intersection_cardinality / den


def isActive(item):
    return item['active_during_test'] == 1


def itemSim(item1, item2):
    nominator = [careerSim(item1['career_level'], item2['career_level']),
                 disciplineSim(item1['discipline_id'], item2['discipline_id']),
                 industrySim(item1['industry_id'], item2['industry_id']),
                 countrySim(item1['country'], item2['country']),
                 regionSim(item1['region'], item2['region']),
                 employmentSim(item1['employment'], item2['employment']),
                 tagsSim(item1['tags'], item2['tags'])]
    return sum(nominator)


active_items['score']=0

grupped_interaction= raw_interactions[['user_id', 'item_id', 'interaction_type']]

grupped_interaction = grupped_interaction.groupby('user_id')


print grupped_interaction.head()

