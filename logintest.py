from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'userlogintest.db')
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
    return render_template('logintest.html', users=users)

# 登録ボタンが押された時の動き
@app.route('/add', methods=['POST'])
def add_user():
    name = request.form.get('username') # フォームから名前を取得
    email = request.form.get('email')   # フォームからメールアドレスを取得
    password = request.form.get('password') # フォームからパスワードを取得
    new_user = User(name=name, email=email, password=password) # 新しいユーザー作成
    db.session.add(new_user)             # DBに追加
    db.session.commit()                  # 保存を確定
    return redirect('/')                 # 画面を更新

if __name__ == '__main__':
    app.run(debug=True)