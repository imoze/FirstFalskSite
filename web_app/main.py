import os

from flask import Flask, render_template, redirect, request, url_for

from db_handlers import db_login, db_register, getClientData, setClientData
from symmetric_crypto import simple_encrypt, simple_decrypt

app = Flask(__name__)

KEY = os.getenv("ENCR_KEY")

@app.route('/')
def index():
    return redirect('/mainpage')



@app.route('/mainpage', methods=['GET', 'POST'])
def mainpage():
    if request.method == 'POST':
        print('post')
        return redirect('models')
    else:
        return render_template('main.html')
    

@app.route('/models', methods=['GET', 'POST'])
def models():
    if request.method == 'POST':
        if request.form['model'] == 'SF90':
            return redirect('models/SF90')
        elif request.form['model'] == 'Roma':
            return redirect('models/Roma')
        elif request.form['model'] == '296':
            return redirect('models/296')
        elif request.form['model'] == 'Daytona SP3':
            return redirect('models/Daytona SP3')
        elif request.form['model'] == '12Cilindri':
            return redirect('models/12Cilindri')
    else:
        return render_template('models.html')


@app.route('/models/SF90',  methods=['GET', 'POST'])
def sf90():
    if request.method == 'POST':
        return redirect(url_for('buy', model='sf90'))
    else:
        return render_template('sf90.html')

@app.route('/models/Roma',  methods=['GET', 'POST'])
def roma():
    if request.method == 'POST':
        return redirect(url_for('buy', model='roma'))
    else:
        return render_template('roma.html')

@app.route('/models/296',  methods=['GET', 'POST'])
def f296():
    if request.method == 'POST':
        return redirect(url_for('buy', model='296'))
    else:
        return render_template('296.html')

@app.route('/models/Daytona SP3',  methods=['GET', 'POST'])
def daytona():
    if request.method == 'POST':
        return redirect(url_for('buy', model='daytonasp3'))
    else:
        return render_template('daytonasp3.html')

@app.route('/models/12Cilindri',  methods=['GET', 'POST'])
def cilindri():
    if request.method == 'POST':
        return redirect(url_for('buy', model='12cilindri'))
    else:
        return render_template('12cilindri.html')
    


@app.route('/buy',  methods=['GET', 'POST'])
def buy():
    if request.method == 'POST':
        return "Succesfull buy"
    else:
        return render_template('buy.html')



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login, password = request.form['login'], request.form['password']
        user = db_login(login, password)
        if user == 0:
            return render_template('login.html', error='Worng login or password')
        else:
            return redirect(url_for('profile', login=simple_encrypt(login, KEY), password=simple_encrypt(password, KEY)))
    else:
        return render_template('login.html')
    

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        login, password = request.form['login'], request.form['password']
        code = db_register(login, password)
        if code == 101:
            return render_template('signup.html', error='Login already taken')
        else:
            return redirect(url_for('profileEdit', login=simple_encrypt(login, KEY), password=simple_encrypt(password, KEY)))
    else:
        return render_template('signup.html')


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if request.method == 'POST':
        if request.form['action'] == 'edit':
            return redirect(url_for('profileEdit',
                                    login=request.args.get('login'),
                                    password=request.args.get('password')))
        else:
            return redirect(url_for('mainpage', login=request.args.get('login'), password=request.args.get('password')))
    else:
        cl_data = getClientData(db_login(simple_decrypt(request.args.get('login'), KEY),
                                         simple_decrypt(request.args.get('password'), KEY)))
        return render_template('profile.html', first_name=cl_data['Firstname'], last_name=cl_data['Lastname'], birth_date=cl_data['BirthDate'],
                                phone=cl_data['Phone'], email=cl_data['Email'], personal_discount=cl_data['PersonalDiscount'], delivery_adress=cl_data['DeliveryAdress'])


@app.route('/profile-edit', methods=['GET', 'POST'])
def profileEdit():
    if request.method == 'POST':
        if request.form['action'] == 'cancel':
            return redirect(url_for('profile',
                                    login=request.args.get('login'),
                                    password=request.args.get('password')))
        else:
            newData = (db_login(simple_decrypt(request.args.get('login'), KEY), simple_decrypt(request.args.get('password'), KEY)),
                       request.form['firstName'], request.form['lastName'], request.form['birthDate'],
                       request.form['phone'], request.form['email'], request.form['address'])
            setClientData(newData)
            return redirect(url_for('profile', login=request.args.get('login'), password=request.args.get('password')))
    else:
        cl_data = getClientData(db_login(simple_decrypt(request.args.get('login'), KEY),
                                         simple_decrypt(request.args.get('password'), KEY)))
        return render_template('profile_edit.html', user=cl_data)



if __name__ == '__main__':
  app.run(debug=True)