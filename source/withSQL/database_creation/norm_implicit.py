#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Script per calcolare i rating medi di ogni utente
""" 

from datetime import datetime
import time
import pymysql.cursors
import math


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
def insertNorm(cursor, user, norm):
    sql = "INSERT INTO user_meta (user_id, norm_implicit) VALUES (%s, %s) ON DUPLICATE KEY UPDATE norm_implicit=%s"
    cursor.execute(sql, (user, norm, norm))

def usersNoInteraction(cursor):
    sql = "SELECT DISTINCT user_id FROM target_users WHERE user_id NOT IN (SELECT DISTINCT user_id FROM user_rating_matrix)"
    cursor.execute(sql)
    return cursor.fetchall()

def usersInteractions(cursor):
    sql = "SELECT DISTINCT user_id FROM user_rating_matrix"
    cursor.execute(sql)
    return cursor.fetchall()

def lenInteractionsUser(cursor, user):
    sql = "SELECT COUNT(*) AS len FROM user_rating_matrix WHERE user_id=%s"
    cursor.execute(sql, (user))
    return float(cursor.fetchone()['len'])

try:
    with connection.cursor() as cursor:
        for user_row in usersInteractions(cursor):
            user_id = user_row['user_id']
            l = lenInteractionsUser(cursor, user_id)
            insertNorm(cursor, user_id, l)

        for user_row in usersNoInteraction(cursor):
            user_id = user_row['user_id']
            insertNorm(cursor, user_id, None)

    connection.commit()
finally:
    connection.close()