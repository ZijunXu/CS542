from flask import render_template, flash, redirect, request, url_for
from flask_login import login_user
from app import app
from .database import User
from .forms import LoginForm,RegistrationForm



@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    form = LoginForm()
    if request.method == 'POST' and form.validate():
        user = User.query.filter_by(name=form.username.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('temp'))
        flash('The login access is unsuccess')
        return redirect(url_for('index'))

    return render_template('index.html', title='Home', form=form, content='Hello, world!')

@app.route('/reg', methods=['GET', 'POST'])
def reg():
    form = RegistrationForm()
    if request.method == 'POST' and form.validate():
        user = User(form.userame.data, form.email.data,
                    form.password.data)
        db_session.add(user)
        flash('Thanks for registering')
        return redirect(url_for('login'))
    return render_template('registration.html',title='Registration',form=form)

@app.route('/test', methods=['GET', 'POST'])
def temp():
    return render_template('test.html')


