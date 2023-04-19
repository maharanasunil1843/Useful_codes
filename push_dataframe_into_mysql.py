#Pushing dataframe into MySQL Work Bench.
#Thumb Rule: Column name of dataframe and MySQL table should be identical.

import pandas as pd
import mysql.connector as connect

mydb = connect.connect(host="localhost", user='root', passwd="Sunil131096@", db='sunil')
#Establishing connection.
#create cursor

cursor = mydb.cursor()

data = {'Rollno': [1,2,3,4,5],
        'Name': ['Sunil', 'Anil', 'Ravi', 'Ankit', 'Akash'],
        'City': ['Surat', 'Satna', 'Patna', 'Jhunjhunu', 'Dongargarh']}

df = pd.DataFrame(data)

for index, row in df.iterrows():
    sql = "insert into sunil.test1(Rollno, Name, City) values (%s, %s, %s)"
    cursor.execute(sql,(row['Rollno'], row['Name'], row['City']))
    mydb.commit()

cursor.close()
mydb.close()