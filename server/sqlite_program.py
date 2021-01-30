import sqlite3
conn = sqlite3.connect('smart_meter.db')

c=conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS consumption_data ( meter_id TEXT, current REAL, usage REAL, time_date TEXT''')

#to execute data

c.execute('''INSERT INTO consumption_data values ("sm01",4.68,2.37,"2021-01-30 13:41:35")''')


conn.commit()

conn.close()