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
def login():
    return render_template('login.html')


@app.route('/',methods=['POST'])
def log():
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
        return render_template('index.html' , tot_user= rows)
    else:
        return redirect('/register')





@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/register' , methods=['POST'])
def reg():
    db=sqlite3.connect('test.sqlite3')
    cur=db.cursor()
    us=request.form['USER']
    pas=request.form['PASS']
    nm=request.form['NAM']
    phn=request.form['PHN']
    add=request.form['ADD']
    cur.execute('insert into User values(?,?,?,?,?)',(us,pas,nm,phn,add))
    db.commit()
    return redirect('/')




@app.route('/index',methods=['GET'])
def index():
    db=sqlite3.connect('test.sqlite3')
    cur=db.cursor()
    rows=cur.execute('select * from User')
    rows=rows.fetchall()
    rows=str(len(rows))
    return render_template('index.html' , tot_user= rows)

@app.route('/tracking')
def tracking():
    return render_template('tracking.html')


@app.route('/pred')
def pred():
    return render_template('Predict.html')



@app.route("/predict",methods=['GET','POST'])
def ans():
    if request.method =="POST":
        s = request.form['ml_model']
        if s=='OR':
            ans=0
        else:
            ans=1
        files=request.files['my_image']
        classes=['cardboard', 'glass', 'metal', 'paper', 'plastic', 'trash']
        img_path='static/'+ files.filename
        files.save(img_path)
        

        if ans==0:
            index=Predict(img_path)
            txt='The given image is '+index
        else:
            index=predict(img_path)
            txt='The given image is '+classes[index]
        
    return render_template('Predict.html' , img_p=img_path , t=txt)


@app.route('/error')
def error():
    return render_template('500.html')



@app.route('/qrcode')
def qr():
    return render_template('qrcode.html')

app.run(debug=True)