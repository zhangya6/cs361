from flask import render_template, flash, redirect, url_for, request, jsonify
from flask_login import login_user, login_required, current_user, logout_user

from app import app, bcrypt, db
from app.forms import RegisterForm, LoginForm, PasswordRestRequestForm
from app.models import User

from app.helperFunctions import get_news_list
from app.helperFunctions import get_stats_list
import sqlite3


@app.route('/')
def index():
    title = 'COVID Coach'
    listOf2 = get_stats_list()
    world_dict = listOf2[0]
    usa_dict = listOf2[1]
    return render_template('index.html', world=world_dict, usa=usa_dict, title=title)


@app.route('/register', methods=['GET', 'POST'])
def register():
    title = 'COVID Coach Account Registration'
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = bcrypt.generate_password_hash(form.password.data)
        user = User(username=username, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        flash('Registration Success', category='success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form, title=title)


@app.route('/news')
def news_page():
    title = 'COVID Coach Get News'
    news_list = get_news_list()
    return render_template('news.html', context=news_list, title=title)


@app.route('/news_detail/<key>')
def news_detail_page(key):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('SELECT * FROM news_table where news_id = ?',(key))
    fetched_item = c.fetchone()
    pass_context = (fetched_item[0],fetched_item[1],fetched_item[2],fetched_item[3],fetched_item[4],fetched_item[5],fetched_item[6],fetched_item[7])
    return render_template('news_detail.html', context = pass_context)


@app.route('/help')
def instruction_page():
    title = 'COVID Coach Get Help'
    return render_template('help.html', title=title)
    
@app.route('/find')
def find_page():
    title = 'COVID Coach Get Help'
    return render_template('find.html', title=title)

@app.route('/board')
def board_page():
    title = 'COVID Coach Message Board'
    return render_template('board.html', title=title)


@app.route('/login', methods=['GET', 'POST'])
def login():
    title = 'COVID Coach Account Log In'
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        remember = form.remember.data
        # Check if password is matched
        user = User.query.filter_by(username=username).first()
        # The reason we are combining these two conditions together is due to security, we don't want hackers to know if account exist or just password is wrong
        if user and bcrypt.check_password_hash(user.password, password):
            # User exists and password matched
            login_user(user, remember=remember)
            flash('Login success', category='info')
            # Next three lines: we don't want redirect index page everytime when user login,we'll get which page user would like to access and redirect to that page
            if request.args.get('next'):
                next_page = request.args.get('next')
                return redirect(next_page)
            return redirect(url_for('index'))
        flash('User not exists or password not matched', category='danger')
    return render_template('login.html', form=form, title=title)


@app.route('/account')
@login_required
def user_account_page():
    title = 'COVID Coach My Account'
    return render_template('myaccount.html', title=title)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/send_password_reset_request', methods=['GET', 'POST'])
def send_password_reset_request():
    title = 'COVID Coach Reset Password'
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = PasswordRestRequestForm()
    return render_template('send_password_reset_request.html', form=form, title=title)