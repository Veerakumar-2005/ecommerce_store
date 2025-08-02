from flask import Flask, render_template, request, redirect, session, url_for
import sqlite3

app = Flask(__name__)
app.secret_key = 'ecommerce_secret'

# DB setup
def get_db():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    db = get_db()
    db.execute('''CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT,
        price REAL,
        image TEXT
    )''')
    db.commit()

@app.route('/')
def index():
    db = get_db()
    products = db.execute('SELECT * FROM products').fetchall()
    return render_template('index.html', products=products)

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    db = get_db()
    product = db.execute('SELECT * FROM products WHERE id = ?', (product_id,)).fetchone()
    return render_template('product.html', product=product)

@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    if 'cart' not in session:
        session['cart'] = []
    session['cart'].append(product_id)
    session.modified = True
    return redirect(url_for('cart'))

@app.route('/cart')
def cart():
    db = get_db()
    cart_items = []
    total = 0
    if 'cart' in session:
        for pid in session['cart']:
            product = db.execute('SELECT * FROM products WHERE id = ?', (pid,)).fetchone()
            if product:
                cart_items.append(product)
                total += product['price']
    return render_template('cart.html', items=cart_items, total=total)

@app.route('/checkout')
def checkout():
    session.pop('cart', None)
    return "<h2>Order placed successfully!</h2><a href='/'>Continue Shopping</a>"

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
