from flask import Flask, render_template, redirect, request, url_for

from db_handlers import db_login, db_register, getClientData

app = Flask(__name__)

@app.route('/')
def index():
    return redirect('/login')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login, password = request.form['login'], request.form['password']
        user = db_login(login, password)
        if user == 0:
            return render_template('login.html', error='Worng login or password')
        else:
            return redirect(url_for('profile',user=user))
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
            return redirect(url_for('profileEdit', user=db_login(login, password)))
    else:
        return render_template('signup.html')

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if request.method == 'POST':
        if request.form['edit-btn'] == 'edit':
            return redirect(url_for('profileEdit', user=request.args.get('user')))
    else:
        cl_data = getClientData(request.args.get('user'))
        return render_template('profile.html', first_name=cl_data['Firstname'], last_name=cl_data['Lastname'], birth_date=cl_data['BirthDate'],
                                phone=cl_data['Phone'], email=cl_data['Email'], personal_discount=cl_data['PersonalDiscount'], delivery_adress=cl_data['DeliveryAdress'])


@app.route('/profile-edit', methods=['GET', 'POST'])
def profileEdit():
    if request.method == 'POST':
        return "POST"
    else:
        cl_data = getClientData(request.args.get('user'))
        return render_template('profile_edit.html', user=cl_data)

if __name__ == '__main__':
  app.run(debug=True)