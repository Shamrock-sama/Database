# -*- coding: utf-8 -*-
"""
Created on Wed Jan  6 17:02:18 2021

@author: Jin Zhu
"""

import pandas as pd
import os
import json
import re


class Loadstruct:
    def __init__(self, KeyList, data=None):
        self.data = {}
        for i in KeyList:
            self.data[i] = {}
    
    def setInfo(self, catagory, item, value):
        self.data[catagory][item] = value
        
    def getInfo(self, catagory, item):
        return self.data[catagory][item]

def import_data(datapath, files):        
    DataBase = {}
    for n in range(len(files)):
        KeyList, Parameter = [], []
        f = pd.read_excel(os.path.join(datapath, files[n]), sheet_name="机组载荷信息表", header=None, usecols=[0, 1, 2], names=['KeyList', 'Parameter', 'Values'])
#        f["KeyList"][[i for i, n in enumerate(f["KeyList"]) if n == '塔架'][0]] = '塔架信息'
#        f["KeyList"][[i for i, n in enumerate(f["KeyList"]) if n == '塔架'][0]] = '塔架极限载荷'
#        f["KeyList"][[i for i, n in enumerate(f["KeyList"]) if n == '塔架'][0]] = '塔架疲劳载荷'
#        f["KeyList"][[i for i, n in enumerate(f["KeyList"]) if n == '叶根'][0]] = '叶根极限载荷'
#        f["KeyList"][[i for i, n in enumerate(f["KeyList"]) if n == '叶根'][0]] = '叶根疲劳载荷'
#        f["KeyList"][[i for i, n in enumerate(f["KeyList"]) if n == '轮毂'][0]] = '轮毂极限载荷'
#        f["KeyList"][[i for i, n in enumerate(f["KeyList"]) if n == '轮毂'][0]] = '轮毂疲劳载荷'   
        if not KeyList:
            for key in f["KeyList"]:
                if isinstance(key, str):
                    KeyList.append(key)
            for var in f["Parameter"]:
                Parameter.append(var)
        T = Loadstruct(KeyList)
        for i in range(len(KeyList)):
            index = f.index[f["KeyList"] == KeyList[i]].values.astype(int)[0]
            if i != (len(KeyList) - 1):
                trunc = f.index[f["KeyList"] == KeyList[i+1]].values.astype(int)[0]
            else:
                trunc = len(f["KeyList"])
            for j in range(index, trunc):
                T.setInfo(KeyList[i], f["Parameter"][j], f["Values"][j])
        Turbname = T.getInfo('基本信息', 'Wind Turbine Name')
        Height = str(T.getInfo('基本参数', 'Hub Height (m)'))
        if re.findall("\AWT", Turbname):
            Dictname = Turbname
        elif re.findall("\AH", Turbname):
            Dictname = Turbname.replace(' ', '-')
        else:
             Dictname = Turbname + '-' + Height
        DataBase[Dictname] = T.data  # use long filename 
        del T
    return DataBase

def savedata(outputpath, DataBase):   
    if os.path.exists(outputpath):
        with open(outputpath, 'r') as f:
            data = json.load(f)
            data.update(DataBase)
        with open(outputpath, 'w') as f:
            json.dump(data, f)
    else:
        with open(outputpath, 'w') as f:
            json.dump(DataBase, f)

def main():
    datapath = "D:\\spyder_run\\database\\Test"
    outputpath = 'D:\\spyder_run\\database\\data.json'
    files = []
    for file in os.listdir(datapath):
        if file.endswith(".xlsx"):
            files.append(file)       
    savedata(outputpath, import_data(datapath, files))
    
if __name__ == "__main__":
    main()