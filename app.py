from flask import Flask , render_template , request , redirect , url_for
import sqlite3
import tensorflow as tf
from tensorflow import keras
import numpy as np
app=Flask(__name__)



model1  = keras.models.load_model('models/{3}')
model2 = keras.models.load_model('models/OR')






def predict(img):
    image = tf.keras.preprocessing.image.load_img(img)
    input_arr = tf.keras.preprocessing.image.img_to_array(image)
    input_arr = np.array([input_arr])
    predictions = model1.predict(input_arr)
    return np.argmax(predictions[0])

def Predict(img):
    image = tf.keras.preprocessing.image.load_img(img)
    input_arr = tf.keras.preprocessing.image.img_to_array(image)
    input_arr = np.array([input_arr])
    predictions = model2.predict(input_arr)
    if predictions[0]>0.5:
        return "Recyclable"
    else:
        return "Organic"







@app.route('/')
def start():
    return render_template('Main.html')
@app.route('/complain')
def comp():
    return render_template('complain.html')


@app.route('/login/admin')
def log_admin():
    return render_template('login.html')

@app.route('/login/admin',methods=['POST'])
def log_admin_post():
    db=sqlite3.connect('test.sqlite3')
    cur=db.cursor()
    us=request.form['USER']
    pas=request.form['PASS']
    rows=cur.execute('select username , password from User where username = ? and password = ?',(us,pas))
    rows=rows.fetchall()


    if len(rows)==1:
        rows=cur.execute('select * from User')
        rows=rows.fetchall()
        rows=str(len(rows))

        db1=sqlite3.connect('industry.sqlite3')
        cur1=db1.cursor()
        rows1=cur1.execute('select * from indus')
        rows1=rows1.fetchall()
        rows1=str(len(rows1))

        ## pending requests
        db2=sqlite3.connect('requests.db')
        cur2=db2.cursor()
        rows2=cur2.execute('select name , Phoneno , Address from pending')
        rows2=rows2.fetchall()
        total_requests=rows2
        rows2=str(len(rows2))




        return render_template('index.html' , tot_user = rows , tot_ind = rows1 , tot_req=rows2 , total=total_requests)
    else:
        return redirect('/register/admin')





@app.route('/register/admin')
def register_admin():
    return render_template('register.html')


@app.route('/register/admin' , methods=['POST'])
def reg_admin():
    db=sqlite3.connect('test.sqlite3')
    cur=db.cursor()
    us=request.form['USER']
    pas=request.form['PASS']
    nm=request.form['NAM']
    phn=request.form['PHN']
    add=request.form['ADD']
    cur.execute('insert into User values(?,?,?,?,?)',(us,pas,nm,phn,add))
    db.commit()
    return redirect('/login/admin')




@app.route('/index/admin',methods=['GET'])
def index():
    db=sqlite3.connect('test.sqlite3')
    cur=db.cursor()
    rows=cur.execute('select * from User')
    rows=rows.fetchall()
    rows=str(len(rows))

    db1=sqlite3.connect('industry.sqlite3')
    cur1=db1.cursor()
    rows1=cur1.execute('select * from indus')
    rows1=rows1.fetchall()
    rows1=str(len(rows1))

    return render_template('index.html' , tot_user= rows , tot_ind=rows1)

@app.route('/tracking/admin')
def tracking():
    return render_template('tracking.html')


@app.route('/pred/admin')
def pred():
    return render_template('Predict.html')



@app.route("/predict/admin",methods=['GET','POST'])
def ans():
    if request.method =="POST":
        s = request.form['ml_model']
        if s=='OR':
            ans=0
        else:
            ans=1
        files=request.files['my_image']
        classes=['cardboard', 'glass', 'metal', 'paper', 'plastic', 'trash']
        img_path='static/images/'+ files.filename
        files.save(img_path)

        if ans==0:
            index=Predict(img_path)
            txt='The given image is '+index
        else:
            index=predict(img_path)
            txt='The given image is '+classes[index]
        
        img_path="/"+img_path
        
        
    return render_template('Predict.html' , img_p=img_path , t=txt)


@app.route('/error/admin')
def error():
    return render_template('500.html')

@app.route('/qrcode/admin')
def qr():
    return render_template('qrcode.html')

@app.route('/industry/admin')
def ind():
    return render_template('add_industries.html')

@app.route('/industry/admin',methods=['POST'])
def ind_post():
    db1=sqlite3.connect('industry.sqlite3')
    cur=db1.cursor()
    ind=request.form['industry']
    add=request.form['address']
    cur.execute('insert into indus values(?,?)',(ind,add))
    db1.commit()
    return redirect('/index/admin')


@app.route('/pend/admin')
def pend():
    pass









###     User Page      ####





@app.route('/login/user')
def log_user():
    return render_template('login_user.html')

@app.route('/login/user',methods=['POST'])
def log_user_post():
    db=sqlite3.connect('test_user.sqlite3')
    cur=db.cursor()
    us=request.form['USER']
    pas=request.form['PASS']
    rows=cur.execute('select username , password from User where username = ? and password = ?',(us,pas))
    rows=rows.fetchall()


    if len(rows)==1:
        rows=cur.execute('select * from User')
        rows=rows.fetchall()
        rows=str(len(rows))
        return render_template('index_user.html')
    else:
        return redirect('/register/user')


@app.route('/register/user')
def register_user():
    return render_template('register_user.html')


@app.route('/register/user' , methods=['POST'])
def reg_user():
    db=sqlite3.connect('test_user.sqlite3')
    cur=db.cursor()
    us=request.form['USER']
    pas=request.form['PASS']
    nm=request.form['NAM']
    phn=request.form['PHN']
    add=request.form['ADD']
    cur.execute('insert into User values(?,?,?,?,?)',(us,pas,nm,phn,add))
    db.commit()
    return redirect('/login/user')



@app.route('/index/user')
def index_user():
    # db=sqlite3.connect('test.sqlite3')
    # cur=db.cursor()
    # rows=cur.execute('select * from User')
    # rows=rows.fetchall()
    # rows=str(len(rows))
    return render_template('index_user.html')


@app.route('/tracking/user')
def tracking_user():
    return render_template('map_tracking.html')



@app.route('/request/user')
def user_request():
    return render_template('request_form.html')


@app.route('/request/user', methods=['POST'])
def user_request_post():
    db=sqlite3.connect('requests.db')
    cur=db.cursor()
    us=request.form['TXT']
    pas=request.form['PHN']
    nm=request.form['ADD']
    cur.execute('insert into pending values(?,?,?)',(us,pas,nm))
    db.commit()
    return redirect('/index/user')
    


app.run(debug=True)