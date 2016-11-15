#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Script per aggiungere  users
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

def insertUser(cursor, user):
    print user
    sql = "INSERT INTO users (user_id, career_level, discipline_id, industry_id, country, region, experience_n_entries_class, experience_years_experience, experience_years_in_current, edu_degree) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    cursor.execute(sql, 
        (user['user_id'],
        user['career_level'],
        user['discipline_id'],
        user['industry_id'],
        user['country'],
        user['region'],
        user['experience_n_entries_class'],
        user['experience_years_experience'],
        user['experience_years_in_current'],
        user['edu_degree']))

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
raw_user_profile = pd.read_csv(data_path + filename_user_profile, sep='\t')

raw_user_profile = raw_user_profile.where(pd.notnull(raw_user_profile), None)

try:
    with connection.cursor() as cursor:

        for index, raw_user in raw_user_profile.iterrows():
            insertUser(cursor, raw_user)

    connection.commit()
finally:
    connection.close()
