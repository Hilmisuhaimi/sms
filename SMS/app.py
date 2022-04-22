from unicodedata import category
from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors

app = Flask(__name__)

app.secret_key = 'secret key' # for session

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_DB'] = 'sms'

mysql = MySQL(app)


@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = 'Please login'

    check = 'username' in request.form and 'password' in request.form

    if request.method == 'POST' and check:
        username = request.form['username']
        password = request.form['password']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        sql = f"SELECT * from accounts WHERE username = '{username}' and password='{password}' and category = 'admin' "
        cursor.execute(sql)
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['username'] = account['username']
            msg = 'You are currently logged in as: ' + session['username']
            return render_template('admin.html', msg=msg)
        else:
            msg = 'Incorrect username or password'

        sql = f"SELECT * from accounts WHERE username = '{username}' and password='{password}' and category = 'student' "
        cursor.execute(sql)
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['username'] = account['username']
            msg = 'You are currently logged in as: ' + session['username']
            return render_template('student.html', msg=msg)
        else:
            msg = 'Incorrect username or password'

    return render_template('login.html', msg=msg)

@app.route('/admin')
def admin():
    if 'loggedin' in session:
        # msg = 'You are currently logged in as: ' + session['username'] 
        return render_template('admin.html')

    return redirect(url_for('login'))

@app.route('/createaccount', methods=['GET', 'POST'])
def createaccount():
    msg = ''

    check = 'username' in request.form and 'password' in request.form and 'category' in request.form 

    if request.method == 'POST' and not check:
        msg = 'Please fill the form'
        return render_template('createaccount.html', msg=msg)

    if request.method == 'POST' and check:
        username = request.form['username']
        password = request.form['password']
        category = request.form['category']
        

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        sql = f"SELECT * from accounts WHERE username = '{username}'"
        cursor.execute(sql)
        account = cursor.fetchone()

        if account:
            msg = 'Account already exists'
        else:
            sql = f"INSERT INTO accounts VALUES ('{username}', '{password}', '{category}', NULL )"
            cursor.execute(sql)
            mysql.connection.commit()

            msg = 'Account successfully registered'

    return render_template('createaccount.html', msg=msg)


@app.route('/stureg', methods=['GET', 'POST'])
def stureg():
    msg = ''

    check = 'regno' in request.form and 'name' in request.form and 'ic' in request.form and 'dob' in request.form and 'address' in request.form and 'email' in request.form and 'email' in request.form 
    if request.method == 'POST' and not check:
        msg = 'Please fill the form'
        return render_template('stureg.html', msg=msg)

    if request.method == 'POST' and check:
        regno = request.form['regno']
        name = request.form['name']
        ic = request.form['ic']
        dob = request.form['dob']
        address = request.form['address']
        email = request.form['email']
        
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        sql = f"SELECT * FROM stperinfo WHERE regno = '{regno}' " 
        cursor.execute(sql)
        stpersonal = cursor.fetchone()

        if stpersonal:
            msg = 'Account already exists'
        else:
            sql = f"INSERT INTO stperinfo VALUES (NULL, '{regno}' , '{name}' ,'{ic}', '{dob}' , '{address}', '{email}' )"
            cursor.execute(sql)
            mysql.connection.commit()
            msg = 'Account successfully registered'

    return render_template('stureg.html', msg=msg)
    

@app.route('/lecturer')
def lecturer():
    if 'loggedin' in session:
        # msg = 'You are currently logged in as: ' + session['username'] 
        return render_template('lecturer.html')

    return redirect(url_for('login'))

@app.route('/regmodule')
def regmodule():
    if 'loggedin' in session:
        page = render_template('regmodule.html')
        return page
    return redirect(url_for('student'))

@app.route('/student')
def student():
    if 'loggedin' in session:
        msg = 'You are currently logged in as: ' + session['username']
        return render_template('student.html', msg=msg)

    return redirect(url_for('login'))
       
@app.route('/stpersonal')
def stpersonal():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        sql = f"SELECT *  FROM stperinfo WHERE regno = '{session['username']}'"
        cursor.execute(sql)
        stperinfo = cursor.fetchall()

        for row in stperinfo:
            name = row['name']
            ic = row['ic']
            
            print("Name; " , name)
            print("IC no: " , ic)
        return render_template('stpersonal.html', stperinfo=stperinfo)

    return redirect(url_for('student'))

@app.route('/ststuinfo')
def ststuinfo():

    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        sql = f"SELECT *  FROM ststuinfo WHERE regno = '{session['username']}'"
        cursor.execute(sql)
        ststuinfo = cursor.fetchall()

        for row in ststuinfo:
            degcate = row['dgcate']
            fac = row['faculty']
            degin = row['dgin']
            enroll = row['enrolldate']
            year = row['year']
            semester = row['sem']
            status = row['status']
            print("Degree Category; " , degcate)
            print("Faculty: " ,fac)
            print("Major; " , degin)
            print("Enrollment: " ,enroll)
            print("Year of study; " , year)
            print("Semester: " ,semester)
            print("Status; " , status)
        
        return render_template('ststuinfo.html', ststuinfo=ststuinfo)

    return redirect(url_for('student'))



@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))



if __name__ == '__main__':
    app.run(debug=True)