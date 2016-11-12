#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Script per aggiungere relazioni molti a molti users jobroles
""" 

import pandas as pd
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

def insertUserJobrole(cursor, userId, jobrole):
    sql = "INSERT INTO users_jobroles (user_id, jobrole) VALUES (%s, %s)"
    cursor.execute(sql, (userId, jobrole))


"""
Variabili costanti (path dei file, ...)
"""
data_path = '../../../data/'
filename_interactions = 'interactions.csv'
filename_active_item = 'active_item_profile.csv'
filename_item_profile = 'item_profile.csv'
filename_target_users = 'target_users.csv'
filename_user_profile = 'user_profile.csv'

interactions_user_id = 'user_id'
interactions_item_id = 'item_id'

"""
lettura csv
"""
raw_user_profile = pd.read_csv(data_path + filename_user_profile, sep='\t', index_col='user_id')
raw_user_profile = raw_user_profile.where(pd.notnull(raw_user_profile), None)
raw_user_profile['jobroles'] = raw_user_profile['jobroles'].apply(lambda x: x.split(','))

try:

    with connection.cursor() as cursor:

        for user_id, user in raw_user_profile.iterrows():
            for jobrole in user['jobroles']:
                if jobrole != "0":
                    insertUserJobrole(cursor, str(user_id), jobrole)

        connection.commit()

finally:
    connection.close()

