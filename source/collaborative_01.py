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
filename_target_users = 'target_users_red.csv'
filename_user_profile = 'user_profile.csv'

interactions_user_id = 'user_id'
interactions_item_id = 'item_id'


"""
Lettura dei file csv
""" 
raw_item_profile = pd.read_csv(data_path + filename_item_profile, sep='\t')
raw_interactions = pd.read_csv(data_path + filename_interactions, sep='\t')
raw_target_users = pd.read_csv(data_path + filename_target_users, sep='\t', index_col="user_id")
# raw_user_profile = pd.read_csv(data_path+filename_user_profile, sep='\t', index_col='id')

"""
filtro item attivi
"""
is_active = raw_item_profile['active_during_test'] == 1
active_items = raw_item_profile[is_active]

"""
preprocessing
"""
maxTimestamp = raw_interactions['created_at'].max()
minTimestamp = raw_interactions['created_at'].min()

raw_interactions['created_at'] = raw_interactions['created_at'].apply(lambda x: np.interp(x, [minTimestamp, maxTimestamp], [0, 1]))

grouped_interactions = raw_interactions[['user_id', 'item_id', 'interaction_type', 'created_at']]
grouped_interactions['items'] = grouped_interactions.apply(lambda x : [ int(x['item_id']), int(x['interaction_type']), x['created_at']], axis=1)
#grouped_interactions = grouped_interactions.drop('item_id', axis=1)
grouped_interactions = grouped_interactions.drop('interaction_type', axis=1)
grouped_interactions = grouped_interactions.drop('created_at', axis=1)
grouped_interactions = grouped_interactions.groupby('user_id').aggregate(lambda x: list(x))

data = np.empty([len(raw_target_users.index), 2], dtype="string")

recommended_items = active_items
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
recommended_items = recommended_items.set_index(['id'])
recommended_items['score'] = 0

lista_appoggio = grouped_interactions

def points_interaction(p1, p2):
	if p1 == p2:
		return 1
	return 0

def match(x, target_user):
	match = 0
	for interaction in x:
		for interaction2 in lista_appoggio.get_value(target_user, 'items', takeable=False):
			if interaction[0] == interaction2[0]:
				match += 1+points_interaction(interaction[1], interaction2[1])
	return match


for current_target_user in raw_target_users.index:
	lista_appoggio = grouped_interactions
	try :
		lista_appoggio['match'] = lista_appoggio['items'].apply(
			lambda x: match(x, target_user=current_target_user))
		recommended_items['score'] = recommended_items['score'].apply(lambda x: 0)
		lista_appoggio = lista_appoggio[lista_appoggio['match'] != 0]
		for user_index , user_row in lista_appoggio.iterrows():

			similarity_taste_taste = lista_appoggio[lista_appoggio.index==user_index]['match']
			if(similarity_taste_taste.item() != 0):
				for item_index in user_row['item_id']:
					if item_index in recommended_items.index :
						if item_index not in grouped_interactions.get_value(current_target_user ,'item_id', takeable=False) :
							
							recommended_items.set_value(item_index, 'score', recommended_items.get_value(item_index, 'score', takeable=False) +  similarity_taste_taste.item())					
							

		recommended_items=recommended_items.sort_values(by='score', ascending=False)
		to_recommend = str(recommended_items.head().index[0])+" "+str(recommended_items.head().index[1])+" "+str(recommended_items.head().index[2])+" "+str(recommended_items.head().index[3])+" "+str(recommended_items.head().index[4])

	except KeyError :
		to_recommend = "2778525 1244196 1386412 278589 657183"



	print current_target_user, "RACOMMENDATION:"
	print '++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++'
	print to_recommend
	row = [str(current_target_user), to_recommend]
	data = np.vstack([data, row])


np.savetxt(data_path+'submission_03.csv', data, delimiter=',', fmt="%s")
