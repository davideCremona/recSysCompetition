#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Script per aggiungere tutti gli user fieldofstudies alla tabella fieldofstudies
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

def insertField(cursor, field):
    sql = "INSERT INTO edu_fieldofstudy (fieldofstudy) VALUES (%s)"
    cursor.execute(sql, (field))


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


field_list = list()
field_column = raw_user_profile['edu_fieldofstudies'].apply(lambda x: str(x).split(','))

for fields in field_column:
    for field in fields:
        if field not in field_list:
            field_list.append(field)

field_list.remove("0")

# adding jobroles
try:

    with connection.cursor() as cursor:

        for field in field_list:

            insertField(cursor, field)

        connection.commit()

finally:
    connection.close()

