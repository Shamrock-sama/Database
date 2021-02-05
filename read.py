# -*- coding: utf-8 -*-
"""
Created on Thu Jan  7 10:58:59 2021

@author: Jin Zhu
"""

import json
import matplotlib.pyplot as plt
import re
import math

def getfloat(text):
    if text:
        if isinstance(text, str):
            if text == '/' or text == '-':
                return 0
            else:
                if re.findall(r'\d+', text):
                    return float(re.search(r'\d+', text).group())
                else:
                    return text
        elif math.isnan(text):
            return 0
        else:
            return float(text)
    else:
        return 0

def Getinfo(Dict, proname=None, key1=None, key2=None):
    if key2:
        return Dict[proname][key1][key2]
    elif key1:
        return Dict[proname][key1]
    elif proname:
        return Dict[proname]
    else:
        return Dict

def Dictfilter(Dict, key1=None, key2=None):
    info = []
    if key2:
        for project in Dict.values():
            info.append(project.get(key1, {}).get(key2))    
    elif key1:
        for project in Dict.values():
            info.append(project.get(key1, {}))
    else:
        for project in Dict.values():
            info.append(project)
    return info


def superfilter(data, key):
    if key == '金风':
        return [i for i in data.keys() if re.findall(r'\AGW', i)]
    elif key == '远景':
        return [i for i in data.keys() if re.findall(r'\AEN', i)]
    elif key == '中车':
        return [i for i in data.keys() if re.findall(r'\AWT', i)]
    elif key == '明阳':
        return [i for i in data.keys() if re.findall(r'\AM', i)]
    elif key == '三一':
        return [i for i in data.keys() if re.findall(r'\ASE', i)]


def find_key(val, dic):
    for k,v in dic.items():
        if isinstance(v, dict):
            p = find_key(val, v)
            if p:
                return [k] 
        elif getfloat(v) == val:
            return [k]

  

#print(superfilter(data, '明阳')) 

with open('data_history.json', 'r') as f:
    data = json.load(f)
    
data1 = Dictfilter(data, "基本信息", 'Rated Power(kW)')
data1 = [getfloat(i) for i in data1] 
data2 = Dictfilter(data, "基本信息", 'Rated Power(kW)')
data2 = [getfloat(i) for i in data2]

print(find_key(3000, data['EN-141-3.0']))  
