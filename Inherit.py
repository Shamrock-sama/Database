# -*- coding: utf-8 -*-
"""
Created on Wed Jan  6 15:12:49 2021

@author: Administrator
"""
import pandas as pd
import os
import re


class Weishengwu(object):
    def __init__(self, name):
        self.name = name
    
    def eat(self):
        print("Eat")
        
class Fish(Weishengwu):
    def move(self):
        print('Move')
        
class Monkey(Fish):
    def __init__(self, name, love):
        self.name = name 
        self.love = love
        
    def eat(self):
        print('Eat with teeth')
        
    def move(self):
        print('Move with feet')
        
    def climb(self):
        print('Climb the tree')
        
Weishengwu('Allen').eat()
Fish('Nible').eat()
print(Monkey('jane', 'banana').love)
