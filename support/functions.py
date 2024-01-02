from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from datetime import date
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
import mysql.connector
import time
import pandas as pd
import configparser
import pysftp

def getConnection(config):
    Conn = mysql.connector.connect(
        host=config['host'],
        user=config['user'],
        password=config['password'],
        )
    return Conn
def getEngine(config):
    try:
        connectionString = "mysql+pymysql://" + config['user'] + ":" + config['password']+"@"+ config['host']
        engine = create_engine(connectionString)
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        print(error)
        return error
    return engine

def loadConfig(configFile):
    config = configparser.ConfigParser()
    config.read(configFile)
    return config

def loadQuery(sqlFileName):
    try:
        with open(sqlFileName) as f:
            sql = f.read()
        if sql == '':
            issue = 'SQL File empty or data not laoded.'
            print(issue)
            log(issue)
            exit()
        return sql
    except:
        error = 'Could not load SQL file.\n\tNOTE: File name should be query.sql'
        print(error)
        log(error)
        exit()

def Upload(CSVfile,config):
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None      
    with pysftp.Connection(config['host'], username=config['uname'], password=config['key'],cnopts=cnopts) as sftp:
        dir = config['dir']
        with sftp.cd(dir):           # temporarily chdir to allcode
            sftp.put(CSVfile)  	# upload file to allcode/pycode on remote
            # sftp.get('remote_file')         # get a remote file
    logMsg = CSVfile + ' was uploaded to '+ config['host'] + "@" + dir
    log(logMsg)
    return logMsg

def SQL2CSV(conn,query,dbname,csvfile):
    pd.read_sql(query, con=conn).to_csv(csvfile,index=False)
    logMsg = "data from `" + dbname + "` was written to " + csvfile
    log(logMsg)
    return logMsg
    

    
    
def getDate():
    return date.today().strftime('%Y-%m-%d')

def log(log):
    log = time.strftime("%H:%M:%S") + '\t' + log + '\n'
    print(log)
    fileName = "logs\\furner_" + getDate() + '.log'
    f = open(fileName, "a")
    f.write(log)

