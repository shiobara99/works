from flask import Flask, render_template, request, redirect, session, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

# MySQL に変更
# XAMPP の phpMyAdmin で作った DB 名に合わせてください
# 例: root でパスワードなしなら 'mysql+pymysql://root:@127.0.0.1/limitrecord'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@127.0.0.1/limitrecord'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

with app.app_context():
    db.create_all()

# メイン画面：DBから全員分取り出してHTMLに渡す
@app.route('/')
def home():
    users = User.query.all()
    current_user = None
    if 'user_id' in session:
        current_user = User.query.get(session['user_id'])
    return render_template('logintest.html', users=users, current_user=current_user)

# 登録ボタンが押された時の動き
@app.route('/add', methods=['POST'])
def add_user():
    name = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    if not name or not email or not password:
        flash('すべての項目を入力してください。')
        return redirect(url_for('home'))

    hashed_password = generate_password_hash(password)
    new_user = User(name=name, email=email, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    flash('ユーザー登録が完了しました。')
    return redirect(url_for('home'))

@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('login_email')
    password = request.form.get('login_password')
    user = User.query.filter_by(email=email).first()
    if user and check_password_hash(user.password, password):
        session['user_id'] = user.user_id
        session['user_name'] = user.name
        flash('ログインしました。')
        return redirect(url_for('home'))

    flash('ログインに失敗しました。メールアドレスまたはパスワードを確認してください。')
    return redirect(url_for('home'))

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('user_name', None)
    flash('ログアウトしました。')
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)