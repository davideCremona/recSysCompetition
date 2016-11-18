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
Script per dividere le interactions in test set e training set
"""

"""
reading interactions
"""