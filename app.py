
from flask import Flask, render_template, request, json, redirect, jsonify
from flaskext.mysql import MySQL
from flask import session, flash
from werkzeug.security import check_password_hash, generate_password_hash
from flask_cors import CORS


app = Flask(__name__)


mysql = MySQL()

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_DB'] = 'car_rental'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_PORT'] = 3306 
mysql.init_app(app)

app.secret_key = 'secret key can be anything!'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/logout')
def logout():
    session.pop('user',None)
    return redirect('/')


@app.route('/register', methods=['POST', 'GET'])
def signUp():
    if request.method == "GET":
        return render_template("register.html")
    # read the posted values from the UI
    username = request.form['username']
    password = request.form['password']
    password_confirmation = request.form['confirmation']
    # validate the received values
    if not username:
        print('must provide username')
        return render_template("register.html")
    elif not password:
        print('must provide password')
        return render_template("register.html")
    elif not password == password_confirmation:
        print('confirmation password must be the same')
        return render_template("register.html")
    
    #hash the password
    hash = generate_password_hash(password)
    #connect to sql
    conn = mysql.connect()
    cursor = conn.cursor()
    if username:
        username_exists = cursor.execute("SELECT username FROM user WHERE username = %s", (username))
        if username_exists:
            print('Username already exists')
            return render_template("register.html")
    cursor.execute("INSERT INTO user(username, hashed_password) VALUES (%s, %s)", (username, hash))

    data = cursor.fetchall()

    if len(data) == 0:
        conn.commit()
        #return json.dumps({'message':'User created successfully !'})
        print("User created successfully")
        return render_template("index.html")
    else:
        print("User not created")
        return render_template("register.html")
    print("didnt")
    return render_template("register.html")

@app.route('/login',methods=['POST', 'GET'])
def login():
    if request.method == "GET":
        return render_template("login.html")
    connected_to_database = 0
    try:
        username = request.form['username']
        password = request.form['password']
        if not username:
            print('Must Provide Username')
            return render_template("login.html")
        elif not request.form.get("password"):
            print('Must Provide Password')
            return render_template("login.html")
        conn = mysql.connect()
        cursor = conn.cursor()
        connected_to_database == 1
        cursor.execute("SELECT * FROM user WHERE username = %s", (username))
        data = cursor.fetchall()
        if len(data) > 0 and check_password_hash(data[0][2], password):
            session['user'] = data[0][0]
            print("User signed in! ")
            return render_template('index.html')
        else:
            print("Username or password are wrong")
            return render_template('login.html')
    except Exception as e:
        print("exception:", str(e))
        return render_template('login.html')
    finally:
        if connected_to_database == 1:
            cursor.close()
            conn.close()

@app.route('/checkout',methods=['POST', 'GET'])
def checkout():
    if request.method == "GET":
        return json.dumps({'message':'checkout.html'})
        #return render_template("checkout.html")
    connected_to_database = 0
    try:
        vin = request.form['vin']
        days = request.form['days']
        if not vin:
            return json.dumps({'message':'missing vin'})
        elif not days:
            return json.dumps({'message':'missing days'})

        conn = mysql.connect()
        cursor = conn.cursor()
        connected_to_database == 1
        query = (
            "INSERT INTO rental (User_id, Car_VIN, Date, Rental_Days, Price, Return_Date) "
            "VALUES "
            "(%s, %s, NOW(3), %s, (SELECT price FROM car WHERE vin=%s)*%s, null);"
        )
        param = (session['user'], vin, days, vin, days)
        cursor.execute(query, param)
        conn.commit()
        data = cursor.fetchall()

        if len(data) == 0:
            #conn.commit()
            return json.dumps({'message':'rental confirmed'})
        else:
            return json.dumps({'message':'rental failed, is the vin number valid?'})

    except Exception as e:
        return json.dumps({'exception':e})

    finally:
        if connected_to_database == 1:
            cursor.close()
            conn.close()

if __name__ == "__main__":
    app.run()   