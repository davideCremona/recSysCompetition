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
raw_norms = pd.read_csv(norms_file, sep=',', index_col='user_id')
norms = dict()
for user_id, norm_implicit in raw_norms.iterrows():
    norms[int(user_id)] = float(norm_implicit)


raw_urm = pd.read_csv(urm_file, sep=',')
