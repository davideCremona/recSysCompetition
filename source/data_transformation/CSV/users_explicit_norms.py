#!/usr/bin/python
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import math

import sys 
import os
sys.path.append(os.path.relpath("../../IMPORTS/files_paths"))
import files_paths
sys.path.append(os.path.relpath("../../IMPORTS/time_statistics"))
from time_stats import *
offset = "../"


"""
Script per calcolare la colonna explicit_norm in user_meta.csv
"""

startTask("reading user meta")

user_meta = pd.read_csv(offset+files_paths.P_USER_META, sep=",", index_col='user_id')
user_meta['explicit_norm'] = 0.0

finishTask("reading user meta")


startTask("reading  user rating matrix")

user_rating_matrix = pd.read_csv(offset+files_paths.P_USER_RATING_MATRIX, sep=",")
user_rating_matrix['avg_rating'] = user_rating_matrix['avg_rating'].apply(lambda x: float(math.pow(float(x),2)))
user_grouped = user_rating_matrix.groupby('user_id')

finishTask("reading user rating matrix")


startTask("computing norms")

for user_id, group in user_grouped:
    user_meta.set_value(user_id, 'explicit_norm', math.sqrt(float(sum(group['avg_rating']))))

finishTask("computing norms")

startTask("saving user meta")
user_meta.to_csv(offset+files_paths.P_USER_META, sep=",")
finishTask("saving user meta")