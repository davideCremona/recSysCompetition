#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Collaborative filtering recommender system
"""

import pandas as pd
import numpy as np
from scipy.spatial.distance import cosine

"""
package settings
"""
pd.options.mode.chained_assignment = None  # default='warn'


"""
Variabili costanti (path dei file, ...)
"""
data_path = '../data/'
filename_interactions = 'interactions_reduced.csv'
filename_active_item  = 'active_item_profile.csv'
filename_item_profile = 'item_profile.csv'
filename_target_users = 'target_users.csv'
filename_user_profile = 'user_profile.csv'

interactions_user_id = 'user_id'
interactions_item_id = 'item_id'


"""
Lettura dei file csv
""" 
raw_item_profile = pd.read_csv(data_path+filename_item_profile, sep='\t' )
raw_interactions = pd.read_csv(data_path+filename_interactions, sep='\t')
#raw_target_users = pd.read_csv(data_path+filename_target_users, sep='\t', index_col='user_id')
#raw_user_profile = pd.read_csv(data_path+filename_user_profile, sep='\t', index_col='id')

"""
filtro item attivi
"""
is_active = raw_item_profile['active_during_test']==1
active_items = raw_item_profile[is_active]

"""
per ogni utente, prendo la lista di item con cui ha interagito
"""
interactions_user_item = raw_interactions[['user_id','item_id']]

grouped_interactions = interactions_user_item.groupby('user_id').aggregate(lambda x: list(x))


lista_appoggio = grouped_interactions;

lista_appoggio['match'] = lista_appoggio['item_id'].apply(
    lambda x: len(set(x).intersection(set(raw_interactions[raw_interactions['user_id']==219]['item_id']))))



recommended_items = active_items
recommended_items['score'] = recommended_items['id'].apply(lambda x: 0)
recommended_items = recommended_items.drop('active_during_test', axis=1)
recommended_items = recommended_items.drop('created_at', axis=1)
recommended_items = recommended_items.drop('tags', axis=1)
recommended_items = recommended_items.drop('employment', axis=1)
recommended_items = recommended_items.drop('region', axis=1)
recommended_items = recommended_items.drop('country', axis=1)
recommended_items = recommended_items.drop('latitude', axis=1)
recommended_items = recommended_items.drop('longitude', axis=1)
recommended_items = recommended_items.drop('industry_id', axis=1)
recommended_items = recommended_items.drop('discipline_id', axis=1)
recommended_items = recommended_items.drop('career_level', axis=1)
recommended_items = recommended_items.drop('title', axis=1)
recommended_items =recommended_items.set_index(['id'])

print recommended_items.head()

for user_index , user_row in grouped_interactions.iterrows():

	similarity_taste_taste = lista_appoggio[lista_appoggio.index==user_index]['match']


	if(similarity_taste_taste.item() != 0):

		for item_index in user_row['item_id']:

			if item_index in recommended_items.index :
				if item_index not in grouped_interactions.get_value(219 ,'item_id', takeable=False) :
					print "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
					print	recommended_items.loc[[item_index]]
					recommended_items.set_value(item_index, 'score', recommended_items.get_value(item_index, 'score', takeable=False) +  similarity_taste_taste.item())					
					print	recommended_items.loc[[item_index]]
					print 

			


recommended_items=recommended_items.sort_values(by='score', ascending=False)

print recommended_items.head()


"""
- lista di item per utente
- per ogni utente u, ordino gli altri utenti (se hanno avuto interazioni con item con cui u ha avuto interazioni, allora valgono di più)
- raccomando un item i che non è nella lista dell'utente u ma è nella lista dell'altro utente.x
"""