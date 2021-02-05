# -*- coding: utf-8 -*-
"""
Created on Tue Jan 19 14:25:17 2021

@author: Administrator
"""

import json
import pandas as pd

def getKey(data):
    length_1 = 0
    for i in range(len(data)):
        if length_1 < len(list(data.values())[i].keys()):
            length_1 = len(list(data.values())[i].keys())
            KeyList = list(list(data.values())[0].keys())                   
    length_i = 0
    Parameter_i = []
    for i in range(len(data)):
        Parameter_2 = []
        length_2 = 0
        for item in list(list(data.values())[i].values()):
            if list(item.keys()):
                length_2 += len(list(item.keys()))
                Parameter_2.append(list(item.keys()))
        if length_i < length_2:
            length_i = length_2
            Parameter_i = Parameter_2
    Parameter = Parameter_i  
    return KeyList, Parameter

with open('data_history.json', 'r') as f:
    data = json.load(f)
    Parameter = getKey(data)[1]    

df = pd.DataFrame([1, 2, 3, 4], [1, 2, 3, 4])
for key, value in data.items():
    
    