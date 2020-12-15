# Created by elr
# Created on  12/14/2020

import os
import sqlite3 

def checkDatabaseExists():
    if os.path.exists("./jobs.db"):  #check if file exists or not
        conn = sqlite3.connect("./jobs.db")
        connObj = conn.cursor()
        dropTable(connObj)
        createTable(connObj)
        conn.commit()
        conn.close()
    else: 
        conn = sqlite3.connect("./jobs.db")
        connObj = conn.cursor()
        createTable(connObj)
        conn.commit()
        conn.close()


def createTable(c):
        c.execute('''CREATE TABLE Jobs
                    (company_name text, job_title text, date_posted text, location text, link text)''')


def dropTable(c):
        c.execute("DROP TABLE Jobs")


def connectToDB():
        conn = sqlite3.connect("./jobs.db")
        return conn
