from flask import Flask,render_template, request, url_for, redirect, flash
import flask_login
from flask import Blueprint
from extensions import db, login_manager
from models import User, Markets, MarketsPro
from utilities import TrendFollower 
import threading
from os import environ

# Getting sensitive data stored in environment variables
user_name = environ.get('USER_NAME')
user_password = environ.get('USER_PASSWORD')
email_name = environ.get('EMAIL_NAME')
email_password = environ.get('EMAIL_PASSWORD')

main = Blueprint('main', __name__)

tf = TrendFollower(user_name = user_name, user_password = user_password,
email_name = email_name, email_password = email_password)

# Setting login manager
@login_manager.user_loader
def user_loader(name):
    if name not in tf.data:
        return

    user = User()
    user.id = name
    return user


@login_manager.request_loader
def request_loader(request):
    name = request.form.get('name')
    if name not in tf.data:
        return

    user = User()
    user.id = name

    # Authenticating currently logged in user
    user.is_authenticated = request.form['password'] == tf.data[name]['password']

    return user



@main.route('/')
def index_get():
    
    # Querying data base for all saved markets available for anonymous users
    all_markets = Markets.query.order_by(Markets.name).all()
    return render_template('index.html',all_markets=all_markets,  data=tf.markets_data )

@main.route('/pro')
@flask_login.login_required
def pro_get():
    
    # Querying data base for all saved markets available only after providing correct credentials
    all_markets = MarketsPro.query.order_by(MarketsPro.name).all()
    return render_template('pro.html',all_markets=all_markets,  data=tf.marketspro_data)

@main.route('/', methods=['POST'])
def index_post():
    err_msg = ''
    
    # Getting submitted market name
    new_market = request.form.get('market')
    
    # Available markets with associated tickers
    markets = {
    'S&P 500' : 'SP500',
    'GOLD' : 'GOLDAMGBD228NLBM',
    'BITCOIN' : 'CBBTCUSD'
    }   
    
    if new_market:
        
        # Checking for existing data base record 
        existing_market = Markets.query.filter_by(name=new_market).first()
        
        # Saving new market together with its current trend
        if not existing_market:
            symbol = markets[new_market]
            new_trend = tf.get_trend(symbol)
            data = Markets(name=new_market, symbol=symbol, trend=new_trend)
            db.session.add(data)
            db.session.commit()
            
        # Flashing error message should user submit an already existing market
        else:
            err_msg = 'MARKET ALREADY ADDED. BECOME A PRO MEMBER AND GET ACCESS TO MORE FINANCIAL INSTRUMENTS!'

    if err_msg:
        flash(err_msg)
    else:
        flash('MARKET ADDED. BECOME A PRO MEMBER AND GET ACCESS TO MORE FINANCIAL INSTRUMENTS!')
    return redirect(url_for('main.index_get'))

@main.route('/pro', methods=['POST'])
@flask_login.login_required
def pro_post():
    err_msg = ''
    
    # Getting submitted market name
    new_market = request.form.get('market') 
    
    if new_market:
        
        # Checking for existing data base record 
        existing_market = MarketsPro.query.filter_by(name=new_market).first()
        
        # Saving new market together with its current trend
        if not existing_market:
            symbol = tf.markets[new_market]
            new_trend = tf.get_trend(symbol)
            data = MarketsPro(name=new_market, symbol=symbol, trend=new_trend)
            db.session.add(data)
            db.session.commit()
            
        # Flashing error message should user submit an already existing market
        else:
            err_msg = 'MARKET ALREADY ADDED'

    if err_msg:
        flash(err_msg)
    else:
        flash('MARKET ADDED')
    return redirect(url_for('main.pro_get'))



@main.route('/delete/<int:id>', methods=['GET', 'POST', 'DELETE'])
def delete(id):
    market = Markets.query.get_or_404(id)
    db.session.delete(market)
    db.session.commit()
    return redirect(url_for('main.index_get'))

@main.route('/delete_pro/<int:id>', methods=['GET', 'POST', 'DELETE'] )
@flask_login.login_required
def delete_pro(id):
    market = MarketsPro.query.get_or_404(id)
    db.session.delete(market)
    db.session.commit()
    return redirect(url_for('main.pro_get'))

@main.route('/update/<int:id>', methods=['GET', 'POST', 'PATCH'])
def update(id):
    market = Markets.query.get_or_404(id)
    symbol = market.symbol
    new_trend = tf.get_trend(symbol)
    market.trend = new_trend
    db.session.commit()
    return redirect(url_for('main.index_get'))

@main.route('/update_pro/<int:id>', methods=['GET', 'POST', 'PATCH'])
@flask_login.login_required
def update_pro(id):
    market = MarketsPro.query.get_or_404(id)
    symbol = market.symbol
    new_trend = tf.get_trend(symbol)
    market.trend = new_trend
    db.session.commit()
    return redirect(url_for('main.pro_get'))

@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    try:
        name = request.form['name']
        
        # Ensuring that provided password match existing data base record
        if request.form['password'] == tf.data[name]['password']:
            user = User()
            user.id = name
            flask_login.login_user(user)
            return redirect(url_for('main.pro_get'))
        
        # Flashing error message should user provide incorrect credentials
        flash('WRONG NAME OR PASSWORD!')
        return redirect(url_for('main.login'))
    
    except KeyError:
        flash('WRONG NAME OR PASSWORD!')
        return redirect(url_for('main.login'))



@main.route('/logout')
@flask_login.login_required
def logout():
    flask_login.logout_user()
    return render_template('logout.html')

@main.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        
        # Moving sending email function to a background thread
        t1 = threading.Thread(target=tf.send_mail, args=[name, email])
        t1.start()
        
        flash('THANK YOU. PLEASE CHECK YOUR EMAIL!')
        return redirect(url_for('main.login'))
    return render_template('register.html')

@login_manager.unauthorized_handler
def unauthorized_handler():
    return render_template('unauthorized.html')

# Custom error pages
@main.app_errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404

@main.app_errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500
