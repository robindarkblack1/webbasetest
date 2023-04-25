from flask import Flask, render_template, request, redirect, session, flash, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_mysqldb import MySQL
from datetime import datetime
from flask_mail import Mail, Message
import random, string,os
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
from functools import wraps
from sqlalchemy.exc import IntegrityError
from flask_login import LoginManager, login_user, login_required, logout_user, UserMixin
from flask_session import Session


app = Flask(__name__)
from sqlalchemy import create_engine

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///info.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # specify the database path
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
db = SQLAlchemy(app)

app.secret_key = 'vhd8djr87hf8h'
# Define the serializer object
s = URLSafeTimedSerializer('vhd8djr87hf8h')


class UserInfo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50))
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f'<User {self.name}>'
    

# Set up Flask-Mail
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'robin20033hood@gmail.com'
app.config['MAIL_PASSWORD'] = 'wshlrvtntoglqcvr'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)

# Generate OTP
def generate_otp(length=6):
    """Generate a random OTP of given length."""
    return ''.join(random.choices(string.digits, k=length))


# Send OTP to user's email
def send_otp(email, otp):
    """Send the OTP to the user's email."""
    msg = Message('Your OTP', sender='your-email-id', recipients=[email])
    msg.body = f'Your OTP is: {otp}'
    mail.send(msg)



@app.route('/')
def home():
    return render_template('web/index.html')

@app.route('/about')
def about():
    return render_template('web/toolsweb/about.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    return render_template('web/toolsweb/signup.html')


@app.route('/tools')
def tools():
    return render_template('web/toolsweb/tools.html')

@app.route('/contact')
def contact():
    return render_template('web/toolsweb/contact.html')




@app.route('/newuser', methods=['GET', 'POST'])
def newuser():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        otp = generate_otp()
        session['otp'] = otp
        session['name'] = name
        session['email'] = email
        session['password'] = password
        send_otp(email, otp)
        return redirect('/verify')
    info = UserInfo.query.all()
    return render_template('index.html', info=info)

with app.app_context():
    db.create_all()


@app.route('/verify', methods=['GET', 'POST'])
def verify():
    if request.method == 'POST':
        otp = request.form['otp']
        if int(otp) == int(session.get('otp', 0)):
            name = session.get('name')
            email = session.get('email')
            password = session.get('password')
            new_user = UserInfo(name=name, email=email, password=password)
            db.session.add(new_user)
            try:
                db.session.commit()
            except IntegrityError as e:
                if "UNIQUE constraint failed: user_info.email" in str(e):
                    return render_template('web/toolsweb/email_exists.html', error='Email already exists.')
                else:
                    flash('An error occurred. Please try again.', 'danger')
                    db.session.rollback()
                    return redirect('/signup')
            session.pop('otp', None)
            session.pop('name', None)
            session.pop('email', None)
            session.pop('password', None)
            flash('Email verified successfully!', 'success')
            return redirect(url_for('get_started', name=name))
        else:
            flash('Invalid OTP code. Please try again.', 'danger')
    return render_template('web/toolsweb/verify.html')


@app.route('/get_started')
def get_started():
    # Retrieve user's name from URL parameter
    name = request.args.get('name')
    # Render the Get Started page with the user's name
    return render_template('web/toolsweb/getstarted.html', name=name)


@app.route('/login', methods=['GET', 'POST'])
def login():
    name = request.args.get('name')
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = UserInfo.query.filter_by(email=email).first()
        if user and user.password == password:
            session['user'] = user.sno
            # return redirect('/dashboard')
            return render_template('web/toolsweb/indevlopment.html', name=name)
        else:
            flash('Invalid login credentials. Please try again.')
            error = 'Invalid login credentials. Please try again.'
            return render_template('web/toolsweb/login.html', error=error)
    return render_template('web/toolsweb/login.html')

@app.route('/admin', methods=['GET','POST'])
def admin():
   if  session.get('name') == 'admin':
        return redirect('/admin_dashboard')
   
   if request.method == 'POST':
        adminname = request.form['username']
        adminpass = request.form['password']
        if adminname == 'admin' and adminpass == 'admin':
            session['name'] = adminname
            return redirect('/admin_dashboard')
        
        
            
        else:
            error = 'Invalid login credentials. Please try again.'
            return render_template('web/admin/login.html', error=error)

   return render_template('web/admin/login.html')

@app.route('/admin_dashboard' )
def admin_dashboard():
    if  session.get('name') == 'admin':
      return render_template('web/admin/admin_dashboard.html')
        
    return redirect('/admin')

@app.route('/logout_admin')
def logout():
    session.pop('name', None)
    return redirect('/admin')

@app.route('/Insta-video-download')
def Insta_video_download():
    return render_template('web/toolsweb/indevlopment.html')

@app.route('/Youtube-video-download')
def Youtube_video_download():
    return render_template('web/toolsweb/indevlopment.html')



# if __name__ == "__main__":
#      app.run(debug=True, port=8000)

