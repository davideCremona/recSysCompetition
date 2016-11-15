#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Script per calcolare i rating medi di ogni utente
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

def dropExistingRatings(cursor):
    sql = "UPDATE users SET average_rating = 0"
    cursor.execute(sql)

# seleziona i rating medi dell'utente 'u'
def getAverageRating(cursor, user, mode="simple_average"):
    if mode == "simple_average":
        sql = "SELECT AVG(rating) AS average_rating FROM user_rating_matrix WHERE user_id=%s"
    if mode == "timestamp_corrected":
        sql = "SELECT AVG(rating * timestamp_weight) AS average_rating FROM user_rating_matrix WHERE user_id=%s"
    cursor.execute(sql, (user))
    return cursor.fetchone()

def getUserIds(cursor):
    sql = "SELECT DISTINCT user_id FROM user_rating_matrix"
    cursor.execute(sql)
    return cursor.fetchall()


def updateRating(cursor, user, rating):
    print "Inserting average rating for user: ", user
    sql = "UPDATE users SET average_rating=%s WHERE user_id=%s"
    cursor.execute(sql, (rating, user))


"""
database pop
"""
try:
    with connection.cursor() as cursor:
        dropExistingRatings(cursor)
        users = getUserIds(cursor)
        for user in users:
            average_rating = getAverageRating(cursor, user['user_id'])['average_rating']
            updateRating(cursor, user['user_id'], average_rating)

    connection.commit()

finally:
    connection.close()



