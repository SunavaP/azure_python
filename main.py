from flask import Flask, render_template, request
import sqlite3 as sql
app = Flask(__name__)

import sqlite3

conn = sqlite3.connect('database.db')
print("Opened database successfully")

cursor = conn.cursor()
# cursor.execute('DROP TABLE IF EXISTS people')
# # conn.execute('CREATE TABLE student (name TEXT, addr TEXT, city TEXT, pin TEXT)')
#
# conn.execute('CREATE TABLE people (name TEXT, vehicle TEXT, grade TEXT, room TEXT, telnum TEXT , picture TEXT , keywords TEXT )')
print("Table created successfully")

import csv
csvfile = open('D:/study/UTA/Summer18/CSE-6331/Quiz 0/people.csv', 'rb')
creader = csv.reader(csvfile, delimiter=',', quotechar='|')

# Iterate through the CSV reader, inserting values into the database
for t in creader:
    cursor.execute("INSERT INTO people VALUES (?,?,?,?,?,?,?)",t)

# Close the csv file, commit changes, and close the connection
csvfile.close()
# filename = 'D:/study/UTA/Summer18/CSE-6331/Quiz 0/people.csv'
# with open(filename, 'rb') as f:
#    csv_data = csv.reader(f)
# # csv_data = csv.reader(file('students.csv'))
#    for row in csv_data:
#
#       cursor.execute('INSERT INTO people(name, vehicle, grade, room, telnum,\
#            picture, keywords )' \
#           'VALUES("%s", "%s", "%s","%s", "%s", "%s","%s")',
#           row)
#close the connection to the database.
conn.commit()
cursor.close()
conn.close()


import csv, sys
filename = 'D:/study/UTA/Summer18/CSE-6331/Quiz 0/people.csv'
with open(filename, 'rb') as f:
    reader = csv.reader(f)
    try:
        for row in reader:
            print row
    except csv.Error as e:
        sys.exit('file %s, line %d: %s' % (filename, reader.line_num, e))

@app.route('/')
def home():
   return render_template('home.html')

@app.route('/enternew')
def new_student():
   return render_template('student.html')

@app.route('/addrec',methods = ['POST', 'GET'])
def addrec():
   if request.method == 'POST':
      try:
         nm = request.form['nm']
         vehicle = request.form['vehicle']
         grade = request.form['grade']
         room = request.form['room']
         telnum= request.form['telnum']
         picture= request.form['picture']
         keywords= request.form['keywords']
         
         with sql.connect("database.db") as con:
            cur = con.cursor()
            
            cur.execute("INSERT INTO people (name, vehicle, grade, room, telnum,\
           picture, keywords) VALUES (?,?,?,?,?,?,?)",(nm, vehicle, grade, room, telnum, picture, keywords))
            
            con.commit()
            msg = "Record successfully added"
      except:
         con.rollback()
         msg = "error in insert operation"
      
      finally:
         return render_template("result.html",msg = msg)
         con.close()

@app.route('/list')
def list():
   con = sql.connect("database.db")
   con.row_factory = sql.Row
   
   cur = con.cursor()
   cur.execute("select * from people")
   
   rows = cur.fetchall();
   return render_template("list.html",rows = rows)

if __name__ == '__main__':
   app.run(debug = True)