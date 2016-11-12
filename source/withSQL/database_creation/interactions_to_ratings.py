#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Script per calcolare i ratings (URM) dalle interazioni
""" 

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
    sql_delete = "DELETE FROM user_rating_matrix"
    cursor.execute(sql_delete)

# restituisce tutte le tuple di interactions_normalized
def getInteractionsAsURM(cursor):
    sql = "SELECT user_id, item_id, AVG(interaction_type) as rating, AVG(timestamp_weight) as timestamp_weight FROM interactions_normalized GROUP BY user_id, item_id"
    cursor.execute(sql)
    return cursor.fetchall()

def saveRating(cursor, rating):
    print "Saving Rating: ", "["+str(rating['user_id'])+",", str(rating['item_id'])+"]"
    sql = "INSERT INTO user_rating_matrix (user_id, item_id, rating, timestamp_weight) VALUES (%s, %s, %s, %s)"
    cursor.execute(sql, (rating['user_id'], rating['item_id'], rating['rating'], rating['timestamp_weight']))


"""
other functions
"""

"""
database population
"""
try:
    with connection.cursor() as cursor:
        dropExistingTable(cursor)
        processed_interactions = getInteractionsAsURM(cursor)
        for user_rating in processed_interactions:
            saveRating(cursor, user_rating)

    connection.commit()
except:
    connection.rollback()
finally:
    connection.close()