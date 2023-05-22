import os
from flask import Flask, render_template, request, flash, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from model import db, connect_to_db, User, OnHand
from werkzeug.security import check_password_hash
from forms import LoginForm, CreateUserForm

app = Flask(__name__)
app.secret_key = os.environ['FLASK_SECRET_KEY']
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def home():
    '''View homepage'''
    
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    '''Create a new user'''
    create_user_form = CreateUserForm()
    
    if create_user_form.validate_on_submit():
        if create_user_form.password.data != create_user_form.confirm_password.data:
            flash('Passwords do not match. Please try again.')
            return redirect(url_for('register'))
        else:
            check_user = User.query.filter_by(username=create_user_form.username.data).first()
            check_email = User.query.filter_by(email=create_user_form.email.data).first()
            if check_email:
                flash("Sorry, a user with that email already exists.")
            elif check_user:
                flash("Sorry, a user with that username already exists.")
            else:
                new_user = User.create(create_user_form.username.data, create_user_form.email.data, create_user_form.password.data)
                db.session.add(new_user)
                db.session.commit()
                flash("New user created! Please Log In")
                return redirect(url_for('login'))
    
    return render_template('register.html', create_user_form=create_user_form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    
    if login_form.validate_on_submit():
        user = User.query.filter_by(username=login_form.username.data).first()
        if user:
            if check_password_hash(user.password, login_form.password.data):
                login_user(user)
                flash('Login Successful')
                return redirect(url_for('dashboard'))
            else: 
                flash('Wrong Pasword - Try Again!')
        else:
            flash("That user does not exist.")
    
    return render_template('login.html', login_form=login_form)

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash("You have been logged out!")
    return redirect(url_for('login'))

@app.route('/menus')
@login_required
def menus():
    pass

@app.route('/pantry')
@login_required
def pantry():
    user_pantry = OnHand.query.filter_by(user_id=current_user.id).all()
    
    return render_template('pantry.html', user_pantry=user_pantry)
    
@app.route('/pantry/delfrom/<ingredient_id>')
def del_from_pantry(ingredient_id):
    to_delete = OnHand.query.filter_by(user_id=current_user.id, ingredient_id=ingredient_id).first()
    db.session.delete(to_delete)
    db.session.commit()
    flash("Ingredient deleted from pantry!")
    return redirect(url_for('pantry'))

@app.route('/lists')
@login_required
def lists():
    pass

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    
    return render_template('dashboard.html')

if __name__ == '__main__':
    connect_to_db(app)
    app.run(debug=True)