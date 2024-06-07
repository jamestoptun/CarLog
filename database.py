import sqlite3
import os
os.system('clear')
connection = sqlite3.connect("customer.db")
cursor = connection.cursor()

command1 = """CREATE TABLE IF NOT EXISTS
    customer (first-name text, last_name text, email text)"""

cursor.execute(command1)

cursor.execute("INSERT INTO CUSTOMERS VALUES ('James', 'Toptun', 'james007@gmail.com')")
cursor.execute("INSERT INTO CUSTOMERS VALUES ('fredick', 'Toptun', 'fredick007@gmail.com')")
cursor.execute("INSERT INTO CUSTOMERS VALUES ('ben', 'Toptun', 'ben007@gmail.com')")
print("Records added to the table")

print ("----------------------------\n Customer Table")
cursor.execute("SELECT * FROM customer")
connection.commit()
results = cursor.fetchall()
print(results)

print (" FName" + " " + "Surname" + " " + "Email")
for item in results:
    print(item[0] + " " + item [1] + " " + item[2])
    print("\n")

    cursor.close()