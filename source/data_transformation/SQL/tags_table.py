#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Script per aggiungere tutti gli item titles alla tabella jobroles
""" 

import pandas as pd
import pymysql.cursors
import time
from datetime import datetime


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
raw_user_profile = pd.read_csv(data_path + filename_item_profile, sep='\t', index_col='id')


print "-------------------------"
print "Start Making list"
now = datetime.now()
time_start = time.mktime(now.timetuple())

jobroles_list = list()
jobroles_column = raw_user_profile['tags'].apply(lambda x: str(x).split(','))

for jobroles in jobroles_column:
    for jobrole in jobroles:
        if jobrole not in jobroles_list:
            jobroles_list.append(jobrole)

if "0" in jobroles_list:
    jobroles_list.remove("0")

now = datetime.now()
time_finish = time.mktime(now.timetuple())
print "Finish Making List in "+str(time_finish-time_start)

print "-------------------------"
print "Start Pushing in DB"
now = datetime.now()
time_start = time.mktime(now.timetuple())

# adding jobroles
try:

    with connection.cursor() as cursor:

        for jobrole in jobroles_list:

            insertRole(cursor, jobrole)

        connection.commit()

finally:
    connection.close()

now = datetime.now()
time_finish = time.mktime(now.timetuple())
print "Finish Pushing in DB in "+str(time_finish-time_start)
