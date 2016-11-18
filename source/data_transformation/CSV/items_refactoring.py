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
Script per:
- creare file items_titles
- creare file items_tags
- postprocess file items_profile
"""

item_profile = pd.read_csv(offset+files_paths.P_ITEM_PROFILE, sep="\t")
item_profile = item_profile.set_index('id')
item_profile['title'] = item_profile['title'].apply(lambda x: str(x).split(','))
item_profile['tags'] = item_profile['tags'].apply(lambda x: str(x).split(','))

"""
items_titles.csv
"""
startTask("Items Items file creation")

items_titles = []
for item_id, row in item_profile.iterrows():
    for title in row['title']:
        entry = {'item_id': item_id, 'title': title}
        items_titles.append(entry)

items_titles_df = pd.DataFrame(items_titles)
items_titles_df = items_titles_df.set_index('item_id')
items_titles_df.to_csv(offset+files_paths.PROCESSED_DATA_DIRECTORY+"/items_titles.csv")
finishTask("Items Items file creation")

"""
items_tags.csv
"""
startTask("Items Tags file creation")
items_tags = []
for item_id, row in item_profile.iterrows():
    for tag in row['tags']:
        entry = {'item_id': item_id, 'tag': tag}
        items_tags.append(entry)

items_tags_df = pd.DataFrame(items_tags)
items_tags_df = items_tags_df.set_index('item_id')
items_titles_df.to_csv(offset+files_paths.PROCESSED_DATA_DIRECTORY+"/items_tags.csv")
finishTask("Items Tags file creation")

"""
processed items.csv (old item_profile.csv without column title and tags)
"""
startTask("Saving new items.csv")
item_profile.drop('title', axis=1, inplace=True)
item_profile.drop('tags', axis=1, inplace=True)
item_profile.to_csv(offset+files_paths.PROCESSED_DATA_DIRECTORY+"/items.csv")
finishTask("Saving new items.csv")

