import mysql.connector

mydb = mysql.connector.connect(host='localhost',user='corall',password='coralldr')

mycursor = mydb.cursor()

mycursor.execute("SHOW TABLES")

mydb.commit()
print(mycursor.rowcount,"record insert.")