from flask import render_template, flash, redirect, request, url_for
from flask_login import login_user
from app import app, db, mongo
from .database import User
from .forms import LoginForm, RegistrationForm, ItemQueryForm


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(name=form.username.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            flash('Thanks for login')
            return redirect(request.args.get('next') or url_for('temp'))
        flash('The login access is unsuccess')
        return redirect(url_for('index'))

    return render_template('index.html', title='Home', form=form, content='Hello, world!')


@app.route('/reg', methods=['GET', 'POST'])
def reg():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(name=form.username.data, email=form.email.data,
                    password=form.password.data)
        db.session.add(user)
        flash('Thanks for registering')
        return redirect(request.args.get('next') or url_for('temp'))
    return render_template('registration.html', title='Registration', form=form)


@app.route('/query', methods=['GET', 'POST'])
def query():
    form = ItemQueryForm()
    if form.validate_on_submit():
        item = mongo.db.users.find({'online': True})
        if item is not None and item.verify_password(form.password.data):
            login_user(item, form.remember_me.data)
            flash('Thanks for login')
            return redirect(request.args.get('next') or url_for('temp'))
        flash('The login access is unsuccess')
        return redirect(url_for('index'))
    return render_template('query.html', title='Item Query', form=form)


@app.route('/test', methods=['GET', 'POST'])
def temp():
    return render_template('test.html')


