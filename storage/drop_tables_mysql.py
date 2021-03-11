import mysql.connector
db_conn = mysql.connector.connect(host="lab6-3855.westus2.cloudapp.azure.com", user="user", password="password", database="events")
db_cursor = db_conn.cursor()
db_cursor.execute('''
 DROP TABLE food_delivery_request, order_request
''')
db_conn.commit()
db_conn.close()
