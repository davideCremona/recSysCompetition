#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Script per normalizzare i timestamp delle interazioni
"""

import pandas as pd
import numpy as np
import pymysql.cursors

"""
connessione al database
"""
DB = "recsys"
HOST = "localhost"
USER = "root"
PSWD = "Ajfk36Tmk"

connection = pymysql.connect(host=HOST,
                             user=USER,
                             password=PSWD,
                             db=DB,
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

"""
Queries
"""

def dropExistingTable(cursor):
    sql_delete = "DELETE FROM interactions_normalized"
    sql_reset = "ALTER TABLE interactions_normalized AUTO_INCREMENT=1"
    cursor.execute(sql_delete)
    cursor.execute(sql_reset)

def insertInteraction(cursor, interaction):
    sql = "INSERT INTO interactions_normalized (user_id, item_id, interaction_type, timestamp_weight) VALUES (%s, %s, %s, %s)"
    cursor.execute(sql, 
        (str(int(interaction['user_id'])),
            str(int(interaction['item_id'])),
            int(interaction['interaction_type']),
            float(interaction['created_at'])))

"""
Variabili costanti (path dei file, ...)
"""
data_path = '../../../data/'
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
raw_interactions = pd.read_csv(data_path + filename_interactions, sep='\t')

"""
normalizzazione
"""
maxTimestamp = raw_interactions['created_at'].max()
minTimestamp = raw_interactions['created_at'].min()

raw_interactions['created_at'] = raw_interactions['created_at'].apply(
    lambda x: np.interp(x, [minTimestamp, maxTimestamp], [0, 1]))

"""
popolamento database
"""


try:
    with connection.cursor() as cursor:
        dropExistingTable(cursor)
        for index, interaction in raw_interactions.iterrows():
            print "Inserting interaction: ", index
            insertInteraction(cursor, interaction)

        connection.commit()
finally:
    connection.close()