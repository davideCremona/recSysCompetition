#!/usr/bin/python
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import math
import time
from datetime import datetime


top_popular = ["2778525","1244196","1386412","278589","657183"]

"""
dizionario user-items
"""
print "-------------------------"
print "Start User-Items Dict"
now = datetime.now()
time_start = time.mktime(now.timetuple())

user_items_dict = dict()
interactions = pd.read_csv("../../../data/interactions.csv", sep='\t')
g_interactions = interactions.groupby('user_id')
for user_id, group in g_interactions:
    user_items_dict[user_id] = set(group['item_id'])

now = datetime.now()
time_finish = time.mktime(now.timetuple())
print "Finish User-Items Dict in "+str(time_finish-time_start)

"""
dizionario items-users
"""
print "-------------------------"
print "Start Items-Users Dict"
now = datetime.now()
time_start = time.mktime(now.timetuple())


item_users_dict = dict()
g_interactions = interactions.groupby('item_id')
for item_id, group in g_interactions:
    item_users_dict[item_id] = set(group['user_id'])

now = datetime.now()
time_finish = time.mktime(now.timetuple())
print "Finish Items-Users Dict in "+str(time_finish-time_start)

target_users = pd.read_csv("../../../data/target_users.csv", sep="\t", index_col="user_id")



submission = pd.read_csv("../../../data/target_users.csv", sep="\t")

for target_user in target_users.index:

    print "-------------------------"
    print "Start User "+str(target_user)
    now = datetime.now()
    time_start = time.mktime(now.timetuple())

    leaderboard = dict()
    try:
        for item in user_items_dict[target_user]:

            for user in item_users_dict[item]:

                for item_user in user_items_dict[user]:

                    if item_user not in user_items_dict[target_user]:
                        try:
                            leaderboard[item_user] += 1
                        except KeyError:
                            leaderboard[item_user] = 1

        sorted_leaderboard = sorted(leaderboard, key=leaderboard.get)
        if len(sorted_leaderboard) == 0:
            sorted_leaderboard = sorted_leaderboard.extend(top_popular)
        print "Recommendation: "+str(sorted_leaderboard[:5])
    except KeyError:
        print "Recommendation: "+str(top_popular)

    now = datetime.now()
    time_finish = time.mktime(now.timetuple())
    print "Finish User "+str(target_user)+" in "+str(time_finish-time_start)


