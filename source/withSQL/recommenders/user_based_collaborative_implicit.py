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

def getTargetUsers(cursor):
    sql = "SELECT user_id FROM target_users"
    cursor.execute(sql)
    return cursor.fetchall()

def getOthersUsers(cursor):
    sql = "SELECT DISTINCT user_id FROM user_rating_matrix"
    cursor.execute(sql)
    return cursor.fetchall()

def lenIntersection(cursor, user1, user2):
    sql = "SELECT COUNT(*) AS len FROM user_rating_matrix AS URM1 JOIN user_rating_matrix AS URM2 ON URM1.item_id=URM2.item_id WHERE URM1.user_id=%s AND URM2.user_id=%s"
    cursor.execute(sql, (user1, user2))
    return cursor.fetchone()['len']

def lenInteractionsUser(cursor, user):
    sql = "SELECT COUNT(*) AS len FROM user_rating_matrix WHERE user_id=%s"
    cursor.execute(sql, (user))
    return cursor.fetchone()['len']

def insertSimilarity(cursor, target, other, sim):
    sql = "INSERT IGNORE INTO user_user_sim (target_user, other_user, similarity) VALUES (%s, %s, %s)"
    cursor.execute(sql, (target, other, sim))

def cosine_similarity(cursor, user1, user2):
    len_intersection = lenIntersection(cursor, user1, user2)
    len_1 = lenInteractionsUser(cursor, user1)
    len_2 = lenInteractionsUser(cursor, user2)
    return float(len_intersection)/float(math.sqrt(float(math.pow(len_1,2)))*math.sqrt(float(math.pow(len_2,2))))

try:
    with connection.cursor() as cursor:
        for record in getTargetUsers(cursor):
            target_user = record['user_id']
            now = datetime.now()
            time_start = time.mktime(now.timetuple())

            for other_user_record in getOthersUsers(cursor):
                other_user_id = other_user_record['user_id']
                sim = cosine_similarity(cursor, target_user, other_user_id)
                if sim != 0.0:
                    insertSimilarity(cursor, target_user, other_user_id, sim)

            now = datetime.now()
            time_finish = time.mktime(now.timetuple())
            print "Finished user "+str(target_user)+" in "+str(time_finish-time_start)
            connection.commit()

finally:
    connection.close()


