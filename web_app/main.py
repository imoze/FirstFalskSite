import os
from datetime import datetime, timedelta

from flask import Flask, render_template, redirect, request, url_for

from db_handlers import db_login, db_register, getClientData, setClientData, placeOrder, orderSum, getOrders
from symmetric_crypto import simple_encrypt, simple_decrypt

app = Flask(__name__)

KEY = os.getenv("ENCR_KEY")

@app.route('/')
def index():
    return redirect('/mainpage')



@app.route('/mainpage', methods=['GET', 'POST'])
def mainpage():
    if request.method == 'POST':
        return redirect(url_for('models', login=request.args.get('login'), password=request.args.get('password')))
    else:
        return render_template('main.html', login=request.args.get('login'), password=request.args.get('password'))
    

@app.route('/models', methods=['GET', 'POST'])
def models():
    if request.method == 'POST':
        if request.form['model'] == 'SF90':
            return redirect(url_for('sf90', login=request.args.get('login'), password=request.args.get('password')))
        elif request.form['model'] == 'Roma':
            return redirect(url_for('roma', login=request.args.get('login'), password=request.args.get('password')))
        elif request.form['model'] == '296':
            return redirect(url_for('f296', login=request.args.get('login'), password=request.args.get('password')))
        elif request.form['model'] == 'Daytona SP3':
            return redirect(url_for('daytona', login=request.args.get('login'), password=request.args.get('password')))
        elif request.form['model'] == '12Cilindri':
            return redirect(url_for('cilindri', login=request.args.get('login'), password=request.args.get('password')))
    else:
        return render_template('models.html', login=request.args.get('login'), password=request.args.get('password'))


@app.route('/models/SF90',  methods=['GET', 'POST'])
def sf90():
    if request.method == 'POST':
        return redirect(url_for('buy', model='SF90 Stradale XX', login=request.args.get('login'), password=request.args.get('password')))
    else:
        return render_template('sf90.html', login=request.args.get('login'), password=request.args.get('password'))

@app.route('/models/Roma',  methods=['GET', 'POST'])
def roma():
    if request.method == 'POST':
        return redirect(url_for('buy', model='Roma', login=request.args.get('login'), password=request.args.get('password')))
    else:
        return render_template('roma.html', login=request.args.get('login'), password=request.args.get('password'))

@app.route('/models/296',  methods=['GET', 'POST'])
def f296():
    if request.method == 'POST':
        return redirect(url_for('buy', model='296', login=request.args.get('login'), password=request.args.get('password')))
    else:
        return render_template('296.html', login=request.args.get('login'), password=request.args.get('password'))

@app.route('/models/Daytona SP3',  methods=['GET', 'POST'])
def daytona():
    if request.method == 'POST':
        return redirect(url_for('buy', model='Daytona SP3', login=request.args.get('login'), password=request.args.get('password')))
    else:
        return render_template('daytonasp3.html', login=request.args.get('login'), password=request.args.get('password'))

@app.route('/models/12Cilindri',  methods=['GET', 'POST'])
def cilindri():
    if request.method == 'POST':
        return redirect(url_for('buy', model='12Cilindri', login=request.args.get('login'), password=request.args.get('password')))
    else:
        return render_template('12cilindri.html', login=request.args.get('login'), password=request.args.get('password'))
    


@app.route('/buy',  methods=['GET', 'POST'])
def buy():
    if request.method == 'POST':
        notBefore = datetime.now() + timedelta(days=1) < datetime.strptime(f'{request.form["delivery-date"]} {request.form["delivery-time"]}', '%Y-%m-%d %H:%M:%S')
        notToLong =  datetime.strptime(request.form['delivery-date'], '%Y-%m-%d') < datetime.now() + timedelta(days=365)
        if notBefore and notToLong:
            res = orderSum((db_login(simple_decrypt(request.args.get('login'), KEY), simple_decrypt(request.args.get('password'), KEY)),
                            request.args['model'], request.form['quantity']))[0]
            if res == 400:
                return render_template('buy.html', model=request.args['model'], error='This model with this amount is anavalible', login=request.args.get('login'), password=request.args.get('password'))
            else:
                return redirect(url_for('payment', login=request.args.get('login'), password=request.args.get('password'),
                                        model=request.args['model'], quantity=request.form['quantity'], sum=res,
                                        del_date=f'{request.form["delivery-date"]} {request.form["delivery-time"]}'))
        else:
            return render_template('buy.html', model=request.args['model'], error='Incorrect date', login=request.args.get('login'), password=request.args.get('password'))
    else:
        return render_template('buy.html', model=request.args['model'], login=request.args.get('login'), password=request.args.get('password'))
    

@app.route('/payment', methods=['GET', 'POST'])
def payment():
    if request.method == 'POST':
        if request.form['action'] == 'pay':
            placeOrder((db_login(simple_decrypt(request.args.get('login'), KEY),
                                 simple_decrypt(request.args.get('password'), KEY)),
                        datetime.strftime(datetime.now(),"%d-%m-%Y %H:%M:%S"),
                        datetime.strftime(datetime.strptime(request.args['del_date'], "%Y-%m-%d %H:%M:%S"), "%d-%m-%Y %H:%M:%S"),
                        request.args['model'],
                        request.args['quantity']))
            return redirect(url_for('success', login=request.args.get('login'), password=request.args.get('password'),
                            model=request.args['model'], quantity=request.args['quantity'], del_date=request.args['del_date'], sum=request.args['sum']))
        else:
            return redirect(url_for('models', login=request.args.get('login'), password=request.args.get('password')))
    else:
        return render_template('payment.html', model=request.args['model'], 
                               quantity=request.args['quantity'],
                               delivery_date=request.args['del_date'],
                               total_amount=request.args['sum'],
                               login=request.args.get('login'), password=request.args.get('password'))


@app.route('/success', methods=['GET', 'POST'])
def success():
    if request.method == 'POST':
        if request.form['action'] == 'hist':
            return redirect(url_for('history', login=request.args.get('login'), password=request.args.get('password')))
        else:
            return redirect(url_for('mainpage', login=request.args.get('login'), password=request.args.get('password')))
    else:
        return render_template('success_order.html', model=request.args['model'], quantity=request.args['quantity'],
                               delivery_date=request.args['del_date'], total_amount=request.args['sum'])
    

@app.route('/history', methods=['GET','POST'])
def history():
    if request.method == 'POST':
        return 123
    else:
        orders = getOrders(db_login(simple_decrypt(request.args.get('login'), KEY),
                                 simple_decrypt(request.args.get('password'), KEY)))
        
        return render_template('history.html', orders=orders, login=request.args.get('login'), password=request.args.get('password'))


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
        elif request.form['action'] == 'hist':
            return redirect(url_for('history', login=request.args.get('login'), password=request.args.get('password')))
        elif request.form['action'] == 'main':
            return redirect(url_for('mainpage', login=request.args.get('login'), password=request.args.get('password')))
        else:
            return redirect('/login')
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