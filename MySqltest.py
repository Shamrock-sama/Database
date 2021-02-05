# -*- coding: utf-8 -*-
"""
Created on Thu Jan 14 10:53:12 2021

@author: Administrator
"""

import mysql.connector
mydb = mysql.connector.connect(
  host="127.0.0.1",
  user="root",
  password="20200420",
  database="mydatabase"
)


mycursor = mydb.cursor()
##mycursor.execute('CREATE DATABASE mydatabase')
#mycursor.execute('SHOW DATABASES')
#for x in mycursor:
#    print(x)
#mycursor.execute("CREATE TABLE customers (name VARCHAR(255), address VARCHAR(255))")
#mycursor.execute("SHOW TABLES")
#for x in mycursor:
#    print(x)
#mycursor.execute("CREATE TABLE customers (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), address VARCHAR(255))")
mycursor.execute("ALTER TABLE customers ADD COLUMN id INT AUTO_INCREMENT PRIMARY KEY")