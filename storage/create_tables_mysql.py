import sqlite3
import mysql.connector

conn = sqlite3.connect('readings.sqlite')

db_conn = mysql.connector.connect(host="lab6-3855.westus2.cloudapp.azure.com", user="user", password="password", database="events")

db_cursor = db_conn.cursor()

# c = conn.cursor()

db_cursor.execute('''
          CREATE TABLE food_delivery_request
          (id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
           customer_id INTEGER NOT NULL,
           driver_id VARCHAR(250) NOT NULL,
           customer_address VARCHAR(250) NOT NULL,
           order_id VARCHAR(250) NOT NULL,
           date_created VARCHAR(100) NOT NULL)
          ''')

db_cursor.execute('''
          CREATE TABLE order_request
          (id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
           customer_id INTEGER NOT NULL,
           order_id VARCHAR(250) NOT NULL,
           date VARCHAR(100) NOT NULL,
           date_created VARCHAR(100) NOT NULL)
          ''')

# conn.commit()
# conn.close()

db_conn.commit()
db_conn.close()

