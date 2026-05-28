from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date, timedelta
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

# XAMPP の limitrecord データベースを使う設定です。
# root のパスワードがない場合はこのままでOKです。
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@127.0.0.1/limitrecord'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

CATEGORY_ICONS = {
    '野菜': 'vegetables.svg',
    '果物': 'fruit.svg',
    '乳製品': 'dairy.svg',
    '肉・魚': 'meat.svg',
    '調味料': 'seasoning.svg',
    'その他': 'other.svg',
}

CATEGORY_CHOICES = list(CATEGORY_ICONS.keys())

class Food(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    quantity = db.Column(db.Float, nullable=False, default=1)
    unit_price = db.Column(db.Float, nullable=False, default=0.0)
    expiration_date = db.Column(db.Date, nullable=True)
    notes = db.Column(db.String(255), nullable=True)

    @property
    def total_price(self):
        return self.quantity * self.unit_price

    @property
    def image_name(self):
        return CATEGORY_ICONS.get(self.category, 'default.svg')

    @property
    def is_expired(self):
        if not self.expiration_date:
            return False
        return self.expiration_date < date.today()

    @property
    def is_expiring_soon(self):
        if not self.expiration_date:
            return False
        return date.today() <= self.expiration_date <= date.today() + timedelta(days=3)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    category = request.args.get('category', '')
    query = Food.query
    if category:
        query = query.filter_by(category=category)

    foods = query.order_by(Food.expiration_date.is_(None), Food.expiration_date.asc(), Food.name.asc()).all()
    total_value = sum(food.total_price for food in foods)

    return render_template(
        'foodslist.html',
        foods=foods,
        categories=CATEGORY_CHOICES,
        selected_category=category,
        total_value=total_value,
    )

@app.route('/add', methods=['POST'])
def add_food():
    name = request.form.get('name', '').strip()
    category = request.form.get('category', '')
    quantity = request.form.get('quantity', '1')
    unit_price = request.form.get('unit_price', '0')
    expiration_date = request.form.get('expiration_date', '')
    notes = request.form.get('notes', '').strip()

    if not name or category not in CATEGORY_CHOICES:
        flash('名前とカテゴリは必須です。')
        return redirect(url_for('index'))

    try:
        quantity = float(quantity)
        unit_price = float(unit_price)
    except ValueError:
        flash('数量と単価は数字で入力してください。')
        return redirect(url_for('index'))

    expiration_date_obj = None
    if expiration_date:
        try:
            expiration_date_obj = datetime.strptime(expiration_date, '%Y-%m-%d').date()
        except ValueError:
            flash('期限日は YYYY-MM-DD 形式で入力してください。')
            return redirect(url_for('index'))

    food = Food(
        name=name,
        category=category,
        quantity=quantity,
        unit_price=unit_price,
        expiration_date=expiration_date_obj,
        notes=notes,
    )
    db.session.add(food)
    db.session.commit()
    flash('在庫を登録しました。')
    return redirect(url_for('index'))

@app.route('/edit/<int:item_id>', methods=['GET', 'POST'])
def edit_food(item_id):
    food = Food.query.get_or_404(item_id)
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        category = request.form.get('category', '')
        quantity = request.form.get('quantity', '1')
        unit_price = request.form.get('unit_price', '0')
        expiration_date = request.form.get('expiration_date', '')
        notes = request.form.get('notes', '').strip()

        if not name or category not in CATEGORY_CHOICES:
            flash('名前とカテゴリは必須です。')
            return redirect(url_for('edit_food', item_id=item_id))

        try:
            quantity = float(quantity)
            unit_price = float(unit_price)
        except ValueError:
            flash('数量と単価は数字で入力してください。')
            return redirect(url_for('edit_food', item_id=item_id))

        expiration_date_obj = None
        if expiration_date:
            try:
                expiration_date_obj = datetime.strptime(expiration_date, '%Y-%m-%d').date()
            except ValueError:
                flash('期限日は YYYY-MM-DD 形式で入力してください。')
                return redirect(url_for('edit_food', item_id=item_id))

        food.name = name
        food.category = category
        food.quantity = quantity
        food.unit_price = unit_price
        food.expiration_date = expiration_date_obj
        food.notes = notes
        db.session.commit()
        flash('在庫を更新しました。')
        return redirect(url_for('index'))

    return render_template('edit_food.html', food=food, categories=CATEGORY_CHOICES)

@app.route('/delete/<int:item_id>', methods=['POST'])
def delete_food(item_id):
    food = Food.query.get_or_404(item_id)
    db.session.delete(food)
    db.session.commit()
    flash('在庫を削除しました。')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, port=5001)
