#!/usr/bin/python
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import math
import time
from datetime import datetime

norms_file = "../../../data/fromSQL/user_meta.csv"
urm_file = "../../../data/fromSQL/user_rating_matrix.csv"


"""
leggo norme, le metto in un dizionario
"""
print "-------------------------"
print "Start Computing Norms"
now = datetime.now()
time_start = time.mktime(now.timetuple())

raw_norms = pd.read_csv(norms_file, sep=',', index_col='user_id')
norms = dict()
for user_id, norm_implicit in raw_norms.iterrows():
    norms[int(user_id)] = float(norm_implicit)

now = datetime.now()
time_finish = time.mktime(now.timetuple())
print "Finish Computing Norms in "+str(time_finish-time_start)


"""
Calcolo dizionario di items per ogni utente
"""

print "-------------------------"
print "Start Computing Interactions"
now = datetime.now()
time_start = time.mktime(now.timetuple())

raw_urm = pd.read_csv(urm_file, sep=',')
raw_urm['user_id'] = raw_urm['user_id'].apply(int)
raw_urm['item_id'] = raw_urm['item_id'].apply(int)
user_grouped = raw_urm.groupby('user_id')
interactios_for_user = dict()
for user_id, interactions in user_grouped:
    interactios_for_user[user_id] = set(interactions['item_id'])


now = datetime.now()
time_finish = time.mktime(now.timetuple())
print "Finish Computing Interactions in "+str(time_finish-time_start)

"""
calcolo similarità
"""

def user_similarity(user1, user2):
    try:
        nominator = len(interactios_for_user[user1].intersection(interactios_for_user[user2]))
        denominator = norms[user1]*norms[user2]
        return nominator / denominator
    except KeyError:
        # (l'utente non ha avuto interazione --> no implicit ratings)
        return 0.0



target_users = pd.read_csv("../../../data/target_users.csv", sep="\t", index_col = "user_id")
similarities_raw = list()
print "-------------------------"
print "Start Computing Similarities"
now = datetime.now()
time_start = time.mktime(now.timetuple())
i = 0
for target_user in target_users.index:
    if i%100 == 0:
        print "Rimangono: "+str(10000-i)
    for other_user in interactios_for_user.keys():
        if target_user.item() != other_user.item():
            sim = user_similarity(target_user, other_user)
            if sim > 0.0:
                similarity_record = str(target_user)+","+str(other_user)+","+str(sim)
                similarities_raw.append(similarity_record)
    i += 1

now = datetime.now()
time_finish = time.mktime(now.timetuple())
print "Finish Computing Similarities in "+str(time_finish-time_start)


"""
salvo similarity matrix
"""
print "-------------------------"
print "Start Saving Similarities"
now = datetime.now()
time_start = time.mktime(now.timetuple())

with open("../../../data/similarity_matrix_user_user.csv", "a") as matrix:

    for record in similarities_raw:
        matrix.write(record+"\n")

    matrix.close()

now = datetime.now()
time_finish = time.mktime(now.timetuple())
print "Finish Writing Similarities in "+str(time_finish-time_start)

