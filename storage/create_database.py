import sqlite3

conn = sqlite3.connect('readings.sqlite')

c = conn.cursor()
c.execute('''
          CREATE TABLE food_delivery_request
          (id INTEGER PRIMARY KEY ASC, 
          customer_id INTEGER NOT NULL,
           driver_id VARCHAR(250) NOT NULL,
           customer_address VARCHAR(250) NOT NULL,
           order_id VARCHAR(250) NOT NULL,
           date_created VARCHAR(100) NOT NULL)
          ''')

c.execute('''
          CREATE TABLE order_request
          (id INTEGER PRIMARY KEY ASC, 
           customer_id INTEGER NOT NULL,
           order_id VARCHAR(250) NOT NULL,
           date VARCHAR(100) NOT NULL,
           date_created VARCHAR(100) NOT NULL)
          ''')

conn.commit()
conn.close()
