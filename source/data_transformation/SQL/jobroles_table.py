#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Script per aggiungere tutti gli user jobroles alla tabella jobroles
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

def insertRole(cursor, role):
    sql = "INSERT IGNORE INTO jobroles (jobrole) VALUES (%s)"
    cursor.execute(sql, (role))

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


jobroles_list = list()
jobroles_column = raw_user_profile['jobroles'].apply(lambda x: x.split(','))

for jobroles in jobroles_column:
    for jobrole in jobroles:
        if jobrole not in jobroles_list:
            jobroles_list.append(jobrole)

jobroles_list.remove("0")

# adding jobroles
try:

    with connection.cursor() as cursor:

        for jobrole in jobroles_list:

            insertRole(cursor, jobrole)

        connection.commit()

finally:
    connection.close()

