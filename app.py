
from flask import Flask, render_template, request, json, redirect, jsonify
from flaskext.mysql import MySQL
from flask import session, flash
from werkzeug.security import check_password_hash, generate_password_hash
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename
#UPLOAD_FOLDER = '/static/images'
#ALLOWED_EXTENSIONS = {'jpg'}
#app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
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

print("\n\n\n\n")





@app.route('/')
def index():
    return render_template('index.html')

@app.route('/admin/', methods=['POST', 'GET'])
def admin():
    if request.method == "GET":
        return render_template("admin.html")

@app.route('/admin/users', methods=['POST', 'GET'])
def admin_users():
    if request.method == "GET":
        connected_to_database = 0
        try:
            conn = mysql.connect()
            cursor = conn.cursor()
            connected_to_database == 1
            cursor.execute("SELECT id, username FROM user")
            data = cursor.fetchall()
            return render_template("admin_users.html", data=data)
        except Exception as e:
            print("exception:", str(e))
            return render_template('admin_users.html')
        finally:
            if connected_to_database == 1:
                cursor.close()
                conn.close()

@app.route('/admin/cars', methods=['POST', 'GET'])
def admin_cars():
    if request.method == "GET":
        connected_to_database = 0
        try:
            conn = mysql.connect()
            cursor = conn.cursor()
            connected_to_database == 1
            # join car table with images on VIN number
            cursor.execute("SELECT car.VIN, car.Make, car.Model, car.Color, car.Year, car.Seats, car.Price_Per_Day,"
             " image.image_number FROM car JOIN image ON image.CAR_VIN = car.VIN GROUP BY car.VIN")
            data = cursor.fetchall()
                    
            return render_template("admin_cars.html", data=data)
        except Exception as e:
            print("exception:", str(e))
            return render_template('admin_cars.html')
        finally:
            if connected_to_database == 1:
                cursor.close()
                conn.close()
@app.route('/edit/<vin>', methods=['POST', 'GET'])
def admin_edit_cars(vin):
    if request.method == "GET":
        connected_to_database = 0
        try:
            conn = mysql.connect()
            cursor = conn.cursor()
            connected_to_database = 1

            #selecting images 
            cursor.execute("SELECT image_number FROM image WHERE CAR_VIN = %s", (vin))
            images = cursor.fetchall()
            cursor.close()
            conn.close()
            connected_to_database = 0

            #selecting cars
            conn = mysql.connect()
            cursor = conn.cursor()
            connected_to_database = 1
            cursor.execute("SELECT Make, Model, Color, Year, Seats, Price_Per_Day FROM car WHERE VIN = %s", (vin))
            car = cursor.fetchone()
            return render_template("admin_edit.html", images=images, vin = vin, car = car)
        except Exception as e:
            print("exception:", str(e))
            return render_template('admin_edit.html')
        finally:
            if connected_to_database == 1:
                cursor.close()
                conn.close()
                connected_to_database = 0
    elif request.method == "POST":
        car_make = request.form['fmake']
        car_model = request.form['fmodel']
        car_color = request.form['fcolor']
        car_year = request.form['fyear']
        car_seats = request.form['fseats']
        car_price = request.form['fprice']
        try:
            conn = mysql.connect()
            cursor = conn.cursor()
            connected_to_database = 1
            cursor.execute("UPDATE car SET Make = %s, Model = %s, Color = %s, Year = %s, Seats = %s, Price_Per_Day = %s"
            "WHERE VIN = %s", (car_make, car_model, car_color, car_year, car_seats, car_price, vin))
            conn.commit()
            return redirect("/admin/cars")
        except Exception as e:
            print("exception:", str(e))
            return render_template('admin_edit.html')
        finally:
            if connected_to_database == 1:
                cursor.close()
                conn.close()
                connected_to_database = 0





@app.route('/delete/<vin>', methods=['POST', 'GET'])
def admin_delete_cars(vin):
    if request.method == "GET":
        connected_to_database = 0
        try:
            conn = mysql.connect()
            cursor = conn.cursor()
            connected_to_database = 1

            #selecting images 
            cursor.execute("SELECT image_number FROM image WHERE CAR_VIN = %s", (vin))
            images = cursor.fetchall()
            cursor.close()
            conn.close()
            connected_to_database = 0

            #selecting cars
            conn = mysql.connect()
            cursor = conn.cursor()
            connected_to_database = 1
            cursor.execute("SELECT Make, Model, Color, Year, Seats, Price_Per_Day FROM car WHERE VIN = %s", (vin))
            car = cursor.fetchone()
            return render_template("admin_delete.html", images=images, vin = vin, car = car)
        except Exception as e:
            print("exception:", str(e))
            return render_template('admin_delete.html')
        finally:
            if connected_to_database == 1:
                cursor.close()
                conn.close()
                connected_to_database = 0
    elif request.method == "POST":
        if request.form["toDelete"] == 'yesDelete':
               #_user = session.get('user')
                conn = mysql.connect()
                cursor = conn.cursor()

                #first delete the foreign key
                cursor.execute("DELETE FROM image WHERE CAR_VIN = %s", (vin))
                conn.commit()
                cursor.close()
                conn.close()


                conn = mysql.connect()
                cursor = conn.cursor()

                #now delete the actual car
                cursor.execute("DELETE FROM car WHERE VIN = %s", (vin))
                conn.commit()
                cursor.close()
                conn.close()


                return redirect('/admin/cars')
        #no delete
        else:
            return redirect('/admin/cars')

@app.route('/admin/add', methods=['POST', 'GET'])
def admin_add_cars():
    if request.method == "GET":
            return render_template("admin_add.html")
    elif request.method == "POST":
        car_make = request.form['fmake']
        car_model = request.form['fmodel']
        car_color = request.form['fcolor']
        car_year = request.form['fyear']
        car_seats = request.form['fseats']
        car_price = request.form['fprice']
        try:
            conn = mysql.connect()
            cursor = conn.cursor()
            connected_to_database = 1
            cursor.execute("UPDATE car SET Make = %s, Model = %s, Color = %s, Year = %s, Seats = %s, Price_Per_Day = %s"
            "WHERE VIN = %s", (car_make, car_model, car_color, car_year, car_seats, car_price, vin))
            conn.commit()
            return redirect("/admin/cars")
        except Exception as e:
            print("exception:", str(e))
            return render_template('admin_edit.html')
        finally:
            if connected_to_database == 1:
                cursor.close()
                conn.close()
                connected_to_database = 0
            
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
            "INSERT INTO rental (User_id, Car_VIN, Date, Days, Total_Price, Return_Date) "
            "VALUES "
            "(%s, %s, NOW(3), %s, (SELECT Price_Per_Day FROM car WHERE vin=%s)*%s, null);"
        )
        param = (session['user'], vin, days, vin, days)
        cursor.execute(query, param)
        data = cursor.fetchall()

        if len(data) == 0:
            conn.commit()
            return json.dumps({'message':'rental confirmed'})
        else:
            return json.dumps({'message':'rental failed, is the vin number valid?'})

    except Exception as e:
        return json.dumps({'exception':e})

    finally:
        if connected_to_database == 1:
            cursor.close()
            conn.close()


@app.route('/showSavedList',methods=['GET'])
def savedlist():
    if session.get('user'):
        return json.dumps({'message':'savedlist.html'})
    else:
        return render_template('error.html', error = 'Unauthorized Access')
    
    
@app.route('/savedList',methods=['POST', 'GET', 'PUT', 'DELETE'])
def savedList():
    #create
    if request.method == "POST":
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
                "INSERT INTO saved_list (User_id, Car_VIN, Days) "
                "VALUES "
                "(%s, %s, %s);"
            )
            param = (session['user'], vin, days)
            cursor.execute(query, param)
            data = cursor.fetchall()

            if len(data) == 0:
                conn.commit()
                return json.dumps({'message':'add to saved list confirmed'})
            else:
                return json.dumps({'message':'add to saved list failed'})

        except Exception as e:
            return json.dumps({'exception':e})

        finally:
            if connected_to_database == 1:
                cursor.close()
                conn.close()

    #read
    elif request.method == "GET":
        connected_to_database = 0
        try:
            conn = mysql.connect()
            cursor = conn.cursor()
            connected_to_database == 1
            query = (
                "SELECT vin, Make, Model, Color, Year, Seats, CAST(Price_Per_Day AS CHAR) AS Price_Per_Day, Image_number, Days "
                "FROM car, image, saved_list "
                "WHERE car.vin = image.car_vin AND car.vin = saved_list.car_vin AND saved_list.user_id = %s AND car.deleted = 0; "
            )
            param = (session['user'])
            cursor.execute(query, param)
            
            data = cursor.fetchall()

            if len(data) > 0:
                return json.dumps(data)
            else:
                return json.dumps({'message':'no cars available'})

        except Exception as e:
            return json.dumps({'exception':e})

        finally:
            if connected_to_database == 1:
                cursor.close()
                conn.close()

    #update
    elif request.method == "PUT":
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
                "UPDATE saved_list "
                "SET Days = %s "
                "WHERE user_id = %s AND car_vin = %s; "
            )
            param = (days, session['user'], vin,)
            cursor.execute(query, param)
            data = cursor.fetchall()

            if len(data) == 0:
                conn.commit()
                return json.dumps({'message':'update to saved list confirmed'})
            else:
                return json.dumps({'message':'update to saved list failed'})

        except Exception as e:
            return json.dumps({'exception':e})

        finally:
            if connected_to_database == 1:
                cursor.close()
                conn.close()

    #delete
    elif request.method == 'DELETE':
        connected_to_database = 0
        try:
            vin = request.form['vin']
            if not vin:
                return json.dumps({'message':'missing vin'})

            conn = mysql.connect()
            cursor = conn.cursor()
            connected_to_database == 1
            query = (
                "DELETE FROM saved_list WHERE car_vin = %s; "
            )
            param = (vin)
            cursor.execute(query, param)
            data = cursor.fetchall()

            if len(data) == 0:
                conn.commit()
                return json.dumps({'message':'delete from saved list confirmed'})
            else:
                return json.dumps({'message':'delete from saved list failed'})

        except Exception as e:
            return json.dumps({'exception':e})

        finally:
            if connected_to_database == 1:
                cursor.close()
                conn.close()


if __name__ == "__main__":
    app.run(debug=True)   
