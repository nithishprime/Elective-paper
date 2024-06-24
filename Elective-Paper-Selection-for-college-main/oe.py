from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
  
  
app = Flask(__name__)
  
  
app.secret_key = 'xyzsdfg'
  
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'nithish'
  
mysql = MySQL(app)
  
@app.route('/')

@app.route('/adminlogin', methods =['GET', 'POST'])
def adminlogin():
    mesage = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM admin WHERE username = % s AND password = % s', (username, password))
        admin = cursor.fetchone()
        if admin:
            session['loggedin'] = True
            session['username'] = admin['username']
            session['password'] = admin['password']
            mesage = 'Logged in successfully !'
            return render_template('admin.html', mesage = mesage)
        else:
            mesage = 'Please enter correct username / password !'
    return render_template('adminlogin.html', mesage = mesage)


@app.route('/logup', methods =['GET', 'POST'])
def logup():
    mesage = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM signup WHERE email = % s AND password = % s', (email, password, ))
        user = cursor.fetchone()
        if user:
            session['loggedin'] = True
            session['name'] = user['name']
            session['email'] = user['email']
            session['password'] = user['password']
            mesage = 'Logged in successfully !'
            return render_template('student.html', mesage = mesage)
        else:
            mesage = 'Please enter correct email / password !'
    return render_template('logup.html', mesage = mesage)

  
@app.route('/signup', methods =['GET', 'POST'])
def signup():
    mesage = ''
    if request.method == 'POST' and 'name' in request.form and 'email' in request.form and 'password' in request.form :
        userName = request.form['name']
        email = request.form['email']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM signup WHERE email = % s', (email, ))
        account = cursor.fetchone()
        if account:
            mesage = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            mesage = 'Invalid email address !'
        elif not userName or not password or not email:
            mesage = 'Please fill out the form properly !'
        else:
            cursor.execute('INSERT INTO signup VALUES ( % s, % s, % s)', (userName, email, password, ))
            mysql.connection.commit()
            mesage = 'You have successfully signed up !'
    elif request.method == 'POST':
        mesage = 'Please fill out the form properly !'
        return render_template('logup.html', mesage = mesage)
    return render_template('signup.html', mesage = mesage)

@app.route('/student', methods =['GET', 'POST'])
def student():
    
    mesage = ''
    if request.method == 'POST' and 'name' in request.form and 'email' in request.form and 'roll' in request.form and 'year' in request.form and 'department' in request.form and 'course' in request.form :
        Name = request.form['name']
        Email = request.form['email']
        Roll = request.form['roll']
        Year = request.form['year']
        Department = request.form['department']
        Course = request.form['course']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM student WHERE Name = % s', (Name, ))
        order = cursor.fetchone()
        if not re.match(r'[^@]+@[^@]+\.[^@]+', Email):
            mesage = 'Invalid email address !'
        elif not Name or not Email or not Roll or not Year or not Department or not Course :
            mesage = 'Please fill out the form !'
        else:
            cursor.execute('INSERT INTO student VALUES (% s, % s, % s, % s, % s, % s)', (Name, Roll, Email,Year,Department,Course))
            mysql.connection.commit()
            mesage = 'You have successfully registered !'
    elif request.method == 'POST':
        mesage = 'Please fill out the form !'
    return render_template("student.html")  

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('email', None)
    session.pop('paswword', None)
    return redirect(url_for('logup'))

@app.route('/admin/export_csv')
def export_csv():
    if 'loggedin' in session and session['loggedin']:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM student')
        data = cursor.fetchall()
        if data:
            # Get the column names dynamically
            columns = [col[0] for col in cursor.description]
            
            csv_data = ",".join(columns) + "\n"

            for row in data:
                csv_data += ",".join([str(row[col]) for col in columns]) + "\n"

            with open('student_data.csv', 'w') as csv_file:
                csv_file.write(csv_data)

            return send_file('student_data.csv', as_attachment=True)
        else:
            return render_template('admin.html', message='No data to export.')
    else:
        return redirect(url_for('logup'))

@app.route("/staff")
def staff():
    return render_template("staff.html")
@app.route("/thank")      
def thank():
    return render_template("thank.html") 



if __name__ == "__main__":
    app.run()