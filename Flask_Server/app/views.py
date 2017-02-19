from flask import render_template, flash, redirect, request, url_for
from app import app
from .forms import LoginForm,RegistrationForm
from flask.ext.login import LoginManager, UserMixin, login_required



@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    form = LoginForm()
    if request.method == 'POST' and form.validate():
        flash('The login access is success')
        return redirect(url_for('temp'))

    return render_template('index.html',title='Home',form=form,content='Hello, world!')

@app.route('/reg', methods=['GET', 'POST'])
def reg():
    form = RegistrationForm()
    if request.method == 'POST' and form.validate():
        user = User(form.username.data, form.email.data,
                    form.password.data)
        db_session.add(user)
        flash('Thanks for registering')
        return redirect(url_for('login'))
    return render_template('registration.html',title='Registration',form=form)

@app.route('/test', methods=['GET', 'POST'])
def temp():
    return render_template('test.html')


