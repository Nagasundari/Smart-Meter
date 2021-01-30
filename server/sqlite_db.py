import sqlite3
conn = sqlite3.connect('smart_meter.db')

def sql_insert(con,meter_id,entities):

    cursorObj = con.cursor()
    
    cursorObj.execute('INSERT INTO ' + meter_id + '(current, usage, time_date) VALUES(?, ?, ?);', entities)
    
    con.commit()

def sql_fetch(con):

    cursorObj = con.cursor()

    cursorObj.execute('SELECT * FROM consumption_data')

    rows = cursorObj.fetchall()

    for row in rows:

        print(row)




c=conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS ''' + meter_id + ''' (current REAL, usage REAL, time_date TEXT);''')

sql_fetch(conn)

#to execute data

#c.execute('''INSERT INTO consumption_data values ("sm01",4.68,2.37,"2021-01-30 13:41:35");''')


conn.commit()

conn.close()