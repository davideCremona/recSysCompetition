#!/usr/bin/python
# -*- coding: utf-8 -*-

import numpy as np

def jaccard(first, second):
    card_a = float(len(first))
    card_b = float(len(second))
    set_a = set()
    set_b = set()
    for item in first:
        set_a.add(item[0])
    for item in second:
        set_b.add(item[0])
    card_a_int_b = float(len(set_a.intersection(set_b)))
    return card_a_int_b / (card_a + card_b - card_a_int_b)

def inverseDifference(first, second):
    return 1.0 / float(abs(int(first) - int(second) + 1))

def equality(first, second):
    return first == second

def userJobrolesSim(jobroles1, jobroles2):
    return jaccard(jobroles1, jobroles2)

def userCareerSim(career1, career2):
    return inverseDifference(career1, career2)

def userDisciplineSim(discipline1, discipline2):
    return equality(discipline1, discipline2)

def userIndustrySim(industry1, industry2):
    return equality(industry1, industry2)

def userCountrySim(country1, country2):
    return equality(country1, country2)

def userRegionSim(region1, region2):
    return equality(region1, region2)

def userExperienceEntriesClassSim(exp1, exp2):
    return inverseDifference(exp1, exp2)

def userExperienceYearsSim(years1, years2):
    return inverseDifference(years1, years2)

def userEduDegreeSim(deg1, deg2):
    return inverseDifference(deg1, deg2)

def userFieldStudiesSim(fields1, fields2):
    return jaccard(fields1, fields2)

def userSim(user1, user2):
    userSimilarities = [userJobrolesSim(user1['jobroles'], user2['jobroles']),
    userCareerSim(user1['career_level'], user2['career_level']),
    userDisciplineSim(user1['discipline_id'], user2['discipline_id']),
    userIndustrySim(user1['industry_id'], user2['industry_id']),
    userCountrySim(user1['country'], user2['country']),
    userExperienceEntriesClassSim(user1['experience_n_entries_class'], user2['experience_n_entries_class']),
    userExperienceYearsSim(user1['experience_years_experience'], user2['experience_years_experience']),
    userEduDegreeSim(user1['edu_degree'], user2['edu_degree']),
    userFieldStudiesSim(user1['edu_fieldofstudies'], user2['edu_fieldofstudies'])]
    return np.interp(sum(userSimilarities).item(), [0,9], [0,1])

    