import psycopg2
import pandas as pd

def getdblocation():
    #contains DB credentials
    db = psycopg2.connect(
        host = 'localhost',
        database = 'ezparkdb',
        user = 'postgres',
        port = 5432,
        password = '090310'
    )
    return db

def modifydatabase(sql,values):
    #function for modifying the DB
    db = getdblocation()
    cursor = db.cursor()

    #Execute the sql code with the cursor value
    cursor.execute(sql, values)

    #make the changes to the db persistent
    db.commit()

    #close the connection
    db.close()

def querydatafromdatabase(sql, values, dfcolumns):
    db = getdblocation()
    cur = db.cursor()
    cur.execute(sql,values)
    rows = pd.DataFrame(cur.fetchall(), columns=dfcolumns)
    db.close()
    return rows