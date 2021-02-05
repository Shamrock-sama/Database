# -*- coding: utf-8 -*-
"""
Created on Mon Jan 11 16:31:03 2021

Data is floating everywhere in the world. This is a small hub where a bundle of data strolling away.

@author: Administrator
"""

import pandas as pd 
import json

class Loadstruct:
    def __init__(self, KeyList, data=None):
        self.data = {}
        for i in KeyList:
            self.data[i] = {}
    
    def setInfo(self, catagory, item, value):
        self.data[catagory][item] = value
        
    def getInfo(self, catagory, item):
        return self.data[catagory][item]


f = pd.read_excel('history.xlsx', header=None)
f.loc[0][[i for i, n in enumerate(f.loc[0]) if n == '塔架'][0]] = '塔架信息'
f.loc[0][[i for i, n in enumerate(f.loc[0]) if n == '塔架'][0]] = '塔架极限载荷'
f.loc[0][[i for i, n in enumerate(f.loc[0]) if n == '塔架'][0]] = '塔架疲劳载荷'
f.loc[0][[i for i, n in enumerate(f.loc[0]) if n == '叶根'][0]] = '叶根极限载荷'
f.loc[0][[i for i, n in enumerate(f.loc[0]) if n == '叶根'][0]] = '叶根疲劳载荷'
f.loc[0][[i for i, n in enumerate(f.loc[0]) if n == '轮毂'][0]] = '轮毂极限载荷'
f.loc[0][[i for i, n in enumerate(f.loc[0]) if n == '轮毂'][0]] = '轮毂疲劳载荷'  
DataBase = {}
KeyList, Parameter = [], []
index = []
i = 0
for key in f.loc[0]:
    if isinstance(key, str):
        KeyList.append(key)
        index.append(i)
    i += 1
for var in f.loc[1]:
    Parameter.append(var)

for i in range(len(f[0])-2):
    T = Loadstruct(KeyList)
    for j in range(len(KeyList)):
        bef = index[j]
        if j != len(KeyList) - 1:
            aft = index[j+1]
        else:
            aft = len(f.loc[0])
        for k in range(bef, aft):
            T.setInfo(KeyList[j], Parameter[k], f[k][i+2])
    DataBase[f[1][i+2]] = T.data
    del T

filename = "data_history.json"
with open(filename, 'w') as f:
    json.dump(DataBase, f)


