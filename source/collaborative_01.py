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
filename_interactions = 'interactions.csv'
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



recommended_items = active_items['id']
recommended_items['score'] = np.nan

for user in grouped_interactions:

	similarity_taste_taste = len(lista_appoggio[lista_appoggio['user_id']==user['user_id']]['item_id'])

	if(similarity_taste_taste != 0):

		appoggio_reccomended=list(set(grouped_interactions[grouped_interactions['user_id']==user['user_id']]['item_id']) - set(grouped_interactions[grouped_interactions['user_id']==219]['item_id']))

		for item in appoggio_reccomended:
			if(active_items[active_items['item_id']==item['item_id']] != nill):
				if recommended_items[recommended_items['item_id']==item['item_id']]['score'] == np.nan :
					recommended_items[recommended_items['item_id']==item['item_id']]['score']=0;

				recommended_items[recommended_items['item_id']==item['item_id']]['score']=recommended_items[recommended_items['item_id']==item['item_id']]['score']+similarity_taste_taste

			



recommended_items.sort('score', ascending=1)

print recommended_items


"""
- lista di item per utente
- per ogni utente u, ordino gli altri utenti (se hanno avuto interazioni con item con cui u ha avuto interazioni, allora valgono di più)
- raccomando un item i che non è nella lista dell'utente u ma è nella lista dell'altro utente.x
"""