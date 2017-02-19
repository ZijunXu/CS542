from flask import render_template, flash, redirect, request
from app import app
from .forms import LoginForm,RegistrationForm

@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index():
    form = LoginForm()

    if form.validate_on_submit():
        flash('Login requested for OpenID="%s", remember_me=%s' %
              (form.UserID.data, str(form.remember_me.data)))
        return redirect('/index')

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
