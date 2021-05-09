
from flask import Flask, render_template, request, json, redirect, jsonify, send_from_directory, Blueprint
from flask_paginate import Pagination, get_page_parameter

from flaskext.mysql import MySQL
from flask import session, flash
from werkzeug.security import check_password_hash, generate_password_hash
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename
import re
UPLOAD_FOLDER = 'static/images/'
ALLOWED_EXTENSIONS = {'jpg'}


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
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
print("\n\n\n\n")


list_cars = []
def list_cars():  
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT Make FROM car")
    list_tuple = cursor.fetchall()
    #returns list of lists
    initial_list = [list(i) for i in list_tuple]
    # flat list out of lists
    list_cars = [item for sublist in initial_list for item in sublist]
    
    #capitalize all words for easy matching
    for word in range (len(list_cars)):
        list_cars[word] = list_cars[word].capitalize()
    return list_cars

    
@app.route('/', methods=['POST', 'GET'])
def index():
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
            cursor.close()
            conn.close()
            connected_to_database == 0


            #getting colors for catagories
            conn = mysql.connect()
            cursor = conn.cursor()
            connected_to_database == 1
            # join car table with images on VIN number
            cursor.execute("SELECT Color FROM car")
            colors = cursor.fetchall()

            return render_template("index.html", data=data, colors=colors)
        except Exception as e:
            print("exception:", str(e))
            return render_template('index.html')
        finally:
            if connected_to_database == 1:
                cursor.close()
                conn.close()
    
    else:
        connected_to_database = 0
        inquiry = request.form.get("search")
        cars_color = request.form.get("cars_colors")
        isInquiry = False
        #look for substrings in string
        substring = re.compile(f'.*{inquiry}', re.IGNORECASE)
        substring_matches = list(filter(substring.match, list_cars()))
        print(cars_color)
        #if user searches for something 
        if inquiry:
            #if word is exactly the same as given in the searchbox
            if inquiry.capitalize() in list_cars():
                print
                try:

                    #getting colors for catagories
                    conn = mysql.connect()
                    cursor = conn.cursor()
                    connected_to_database == 1
                    # join car table with images on VIN number
                    cursor.execute("SELECT Color FROM car")
                    colors = cursor.fetchall()
                    cursor.close()
                    conn.close()
                    connected_to_database == 0

                    conn = mysql.connect()
                    cursor = conn.cursor()
                    connected_to_database == 1
                    if cars_color is None:
                        cursor.execute("SELECT car.VIN, car.Make, car.Model, car.Color, car.Year, car.Seats, car.Price_Per_Day, image.image_number FROM car \
                        JOIN image ON image.CAR_VIN = car.VIN GROUP BY car.VIN HAVING car.Make = %s", ( inquiry))
                    else:
                        cursor.execute("SELECT car.VIN, car.Make, car.Model, car.Color, car.Year, car.Seats, car.Price_Per_Day, image.image_number FROM car \
                        JOIN image ON image.CAR_VIN = car.VIN WHERE car.Color = %s GROUP BY car.VIN HAVING car.Make = %s", (cars_color, inquiry))
                    print(substring)
                    data = cursor.fetchall()
                    return render_template("index.html", data=data, colors=colors)
                except Exception as e:
                    print("exception:", str(e))
                    return render_template('index.html')
                finally:
                    if connected_to_database == 1:
                        cursor.close()
                        conn.close()

            #else there is a substring of that word
            elif substring_matches:
                try:

                    #getting colors for catagories
                    conn = mysql.connect()
                    cursor = conn.cursor()
                    connected_to_database == 1
                    # join car table with images on VIN number
                    cursor.execute("SELECT Color FROM car")
                    colors = cursor.fetchall()
                    cursor.close()
                    conn.close()
                    connected_to_database == 0



                    conn = mysql.connect()
                    cursor = conn.cursor()
                    connected_to_database == 1

                    if cars_color is None:
                        cursor.execute("SELECT car.VIN, car.Make, car.Model, car.Color, car.Year, car.Seats, car.Price_Per_Day, image.image_number FROM car \
                        JOIN image ON image.CAR_VIN = car.VIN GROUP BY car.VIN HAVING car.Make LIKE %s", ('%{}%'.format(inquiry)))
                    else:
                        cursor.execute("SELECT car.VIN, car.Make, car.Model, car.Color, car.Year, car.Seats, car.Price_Per_Day, image.image_number FROM car \
                        JOIN image ON image.CAR_VIN = car.VIN WHERE car.Color = %s GROUP BY car.VIN HAVING car.Make LIKE %s", (cars_color, '%{}%'.format(inquiry)))
                    print(substring_matches)
                    data = cursor.fetchall()
                    return render_template("index.html", data=data, colors=colors)
                except Exception as e:
                    print("exception:", str(e))
                    return render_template('index.html')
                finally:
                    if connected_to_database == 1:
                        cursor.close()
                        conn.close()
        else:
            isFound = False
            print("Item not found")
            redirect('/')
    return render_template('index.html')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

'''
@app.route('/', methods=['GET', 'POST'])
def upload_image():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            print('No file part')
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return render_template('admin_add.html')
        else:
            print('not allowed')
            return redirect('/admin/cars')
'''


@app.route('/admin/', methods=['POST', 'GET'])
def admin():
    return render_template("admin.html")

@app.route('/admin/users', methods=['POST', 'GET'])
def admin_users():
    if request.method == "GET":
        connected_to_database = 0
        if session.get('user'):
            _user = session.get('user')
            #make sure user logged in is admin
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM admin WHERE id = %s", _user)
            data = cursor.fetchall()
            if len(data) > 0:
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
            else:
                flash("User not admin", "error")
                return redirect('/')
        else:
            flash("Must login", "error")
            return redirect('/')
                



@app.route('/admin/cars', methods=['POST', 'GET'])
def admin_cars():
    if request.method == "GET":
        if session.get('user'):
            _user = session.get('user')
            #make sure user logged in is admin
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM admin WHERE id = %s", _user)
            data = cursor.fetchall()
            cursor.close()
            conn.close()
            if len(data) > 0:
                connected_to_database = 0
                print("cars", list_cars())
                try:
                    conn = mysql.connect()
                    cursor = conn.cursor()
                    
                    # Setting page, limit and offset variables
                    per_page = 4
                    page = request.args.get(get_page_parameter(), type=int, default=1)
                    offset = (page - 1) * per_page

                    connected_to_database == 1
                    # join car table with images on VIN number, get all
                    cursor.execute("SELECT car.VIN, car.Make, car.Model, car.Color, car.Year, car.Seats, car.Price_Per_Day,"
                    " image.image_number FROM car JOIN image ON image.CAR_VIN = car.VIN GROUP BY car.VIN")
                    total = cursor.fetchall()

                    
                    #the pagination limited one

                    cursor.execute("SELECT car.VIN, car.Make, car.Model, car.Color, car.Year, car.Seats, car.Price_Per_Day,"
                    " image.image_number FROM car JOIN image ON image.CAR_VIN = car.VIN GROUP BY car.VIN DESC LIMIT %s OFFSET %s" , (per_page, offset))
                    data  = cursor.fetchall()

                    cursor.close()
                    conn.close()
                    connected_to_database == 0

                    pagination = Pagination(page=page, per_page=per_page, offset=offset, total=len(total), record_name='data', css_framework='bulma')

                    #getting colors for catagories
                    conn = mysql.connect()
                    cursor = conn.cursor()
                    connected_to_database == 1
                    # join car table with images on VIN number
                    cursor.execute("SELECT Color FROM car")
                    colors = cursor.fetchall()

                    return render_template("admin_cars.html", data=data, colors=colors, pagination=pagination)
                except Exception as e:
                    print("exception:", str(e))
                    return render_template('admin_cars.html')
                finally:
                    if connected_to_database == 1:
                        cursor.close()
                        conn.close()
        print("must login")
        return redirect('/')
    
    else:
        connected_to_database = 0
        inquiry = request.form.get("search")
        cars_color = request.form.get("cars_colors")
        isInquiry = False
        #look for substrings in string
        substring = re.compile(f'.*{inquiry}', re.IGNORECASE)
        substring_matches = list(filter(substring.match, list_cars()))
        print(cars_color)
        #if user searches for something 
        if inquiry:
            #if word is exactly the same as given in the searchbox
            if inquiry.capitalize() in list_cars():
                print
                try:

                    #getting colors for catagories
                    conn = mysql.connect()
                    cursor = conn.cursor()
                    connected_to_database == 1
                    # join car table with images on VIN number
                    cursor.execute("SELECT Color FROM car")
                    colors = cursor.fetchall()
                    cursor.close()
                    conn.close()
                    connected_to_database == 0

                    conn = mysql.connect()
                    cursor = conn.cursor()
                    connected_to_database == 1
                    if cars_color is None:
                        cursor.execute("SELECT car.VIN, car.Make, car.Model, car.Color, car.Year, car.Seats, car.Price_Per_Day, image.image_number FROM car \
                        JOIN image ON image.CAR_VIN = car.VIN GROUP BY car.VIN HAVING car.Make = %s", ( inquiry))
                    else:
                        cursor.execute("SELECT car.VIN, car.Make, car.Model, car.Color, car.Year, car.Seats, car.Price_Per_Day, image.image_number FROM car \
                        JOIN image ON image.CAR_VIN = car.VIN WHERE car.Color = %s GROUP BY car.VIN HAVING car.Make = %s", (cars_color, inquiry))
                    print(substring)
                    data = cursor.fetchall()
                    return render_template("admin_cars.html", data=data, colors=colors)
                except Exception as e:
                    print("exception:", str(e))
                    return render_template('admin_cars.html')
                finally:
                    if connected_to_database == 1:
                        cursor.close()
                        conn.close()

            #else there is a substring of that word
            elif substring_matches:
                try:

                    #getting colors for catagories
                    conn = mysql.connect()
                    cursor = conn.cursor()
                    connected_to_database == 1
                    # join car table with images on VIN number
                    cursor.execute("SELECT Color FROM car")
                    colors = cursor.fetchall()
                    cursor.close()
                    conn.close()
                    connected_to_database == 0



                    conn = mysql.connect()
                    cursor = conn.cursor()
                    connected_to_database == 1

                    if cars_color is None:
                        cursor.execute("SELECT car.VIN, car.Make, car.Model, car.Color, car.Year, car.Seats, car.Price_Per_Day, image.image_number FROM car \
                        JOIN image ON image.CAR_VIN = car.VIN GROUP BY car.VIN HAVING car.Make LIKE %s", ('%{}%'.format(inquiry)))
                    else:
                        cursor.execute("SELECT car.VIN, car.Make, car.Model, car.Color, car.Year, car.Seats, car.Price_Per_Day, image.image_number FROM car \
                        JOIN image ON image.CAR_VIN = car.VIN WHERE car.Color = %s GROUP BY car.VIN HAVING car.Make LIKE %s", (cars_color, '%{}%'.format(inquiry)))
                    print(substring_matches)
                    data = cursor.fetchall()
                    return render_template("admin_cars.html", data=data, colors=colors)
                except Exception as e:
                    print("exception:", str(e))
                    return render_template('admin_cars.html')
                finally:
                    if connected_to_database == 1:
                        cursor.close()
                        conn.close()
        else:
            isFound = False
            print("Item not found")
            redirect('/admin/cars')




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

        if 'file' not in request.files:
            print('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            print('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        else:
            print('not allowed')
            return redirect('/admin/cars')
        image_variable = secure_filename(file.filename)
        #extracting numebr from file name
        image_number = [int(s) for s in re.findall(r'\b\d+\b',image_variable)]   

        try:
            conn = mysql.connect()
            cursor = conn.cursor()
            connected_to_database = 1
            cursor.execute("UPDATE car SET Make = %s, Model = %s, Color = %s, Year = %s, Seats = %s, Price_Per_Day = %s"
            "WHERE VIN = %s", (car_make, car_model, car_color, car_year, car_seats, car_price, vin))
            conn.commit()
            cursor.close()
            conn.close()
            connected_to_database = 0
            if image_number:
                conn = mysql.connect()
                cursor = conn.cursor()
                connected_to_database = 1
                cursor.execute("insert into image (car_VIN, image_number) values \
                ((select VIN from car WHERE VIN = %s), %s)", (vin, image_number[0]))
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



@app.route('/delete/image/<imageNumber>', methods=['POST', 'GET'])
def admin_delete_image(imageNumber):
    if request.method == "GET":
        connected_to_database = 0
        try:
            conn = mysql.connect()
            cursor = conn.cursor()
            connected_to_database = 1
            #selecting image 
            cursor.execute("SELECT image_number FROM image WHERE image_number = %s", (imageNumber))
            image = cursor.fetchone()
            cursor.close()
            conn.close()
            connected_to_database = 0
            return render_template("admin_image_delete.html", imageNumber= imageNumber)
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
                cursor.execute("DELETE FROM image WHERE image_number = %s", (imageNumber))
                conn.commit()
                return redirect('/admin/cars')
        #no delete
        else:
            return redirect('/admin/cars')








@app.route('/admin/add', methods=['POST', 'GET'])
def admin_add_cars():
    if request.method == "GET":
            return render_template("admin_add.html")
    elif request.method == "POST":
        car_VIN = request.form['fvin']
        car_make = request.form['fmake']
        car_model = request.form['fmodel']
        car_color = request.form['fcolor']
        car_year = request.form['fyear']
        car_seats = request.form['fseats']
        car_price = request.form['fprice']
        # check if the post request has the file part
        if 'file' not in request.files:
            print('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            print('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        else:
            print('not allowed')
            return redirect('/admin/cars')
        image_variable = secure_filename(file.filename)
        #extracting numebr from file name
        image_number = [int(s) for s in re.findall(r'\b\d+\b',image_variable)]        
        try:
            conn = mysql.connect()
            cursor = conn.cursor()
            connected_to_database = 1
            cursor.execute("INSERT INTO car (VIN, Make, Model, Color, Year, Seats, Price_Per_Day, DELETED)"
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (car_VIN, car_make, car_model, car_color, car_year, car_seats, car_price, 0))
            conn.commit()
            cursor.close()
            conn.close()
            connected_to_database = 0

            conn = mysql.connect()
            cursor = conn.cursor()
            connected_to_database = 1
            cursor.execute("insert into image (car_VIN, image_number) values \
            ((select VIN from car WHERE VIN = %s), %s)", (car_VIN, image_number[0]))
            conn.commit()
            return redirect("/admin/cars")
        except Exception as e:
            print("exception:", str(e))
            return render_template('admin.html')
        finally:
            if connected_to_database == 1:
                cursor.close()
                conn.close()
                connected_to_database = 0
        
        return redirect("/admin/cars")
            
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
            #return json.dumps({'message':'Username Unavilable!'})
            return jsonify({'htmlresponse': 'Username Unavilable!'})
            #return render_template("register.html")
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

@app.route('/admin/login',methods=['POST', 'GET'])
def admin_login():
    if request.method == "GET":
        connected_to_database = 0
        try:
            print("Creating admin")
            conn = mysql.connect()
            cursor = conn.cursor()
            connected_to_database == 1
            admin_pass = 'root'
            admin_username = 'root'
            cursor.execute("INSERT INTO admin(username, hashed_password) VALUES (%s, %s)", (admin_username, generate_password_hash(admin_pass)))
            conn.commit()
            cursor.close()
            conn.close()
            connected_to_database == 0
            print("admin created")
        except Exception as e:
            print("exception:", str(e))
            return render_template('admin_users.html')
        finally:
            if connected_to_database == 1:
                cursor.close()
                conn.close()
            return render_template("admin_login.html")
    else:
        connected_to_database = 0
        try:
            username = request.form['username']
            password = request.form['password']
            if not username:
                print('Must Provide Username')
                return render_template("admin_login.html")
            elif not request.form.get("password"):
                print('Must Provide Password')
                return render_template("admin_login.html")
            conn = mysql.connect()
            cursor = conn.cursor()
            connected_to_database == 1
            cursor.execute("SELECT * FROM admin WHERE username = %s", (username))
            data = cursor.fetchall()
            print("data is", data)
            if len(data) > 0 and check_password_hash(data[0][2], password):
                session['user'] = data[0][0]
                print("User signed in! ")
                return render_template('admin.html')
            else:
                print("Username or password are wrong")
                return render_template('admin_login.html')
        except Exception as e:
            print("exception:", str(e))
            return render_template('admin_login.html')
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
