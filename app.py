from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from database import db, User, Product, Order, OrderItem, CartItem, Category, Review, Address
# from werkzeug.security import generate_password_hash, check_password_hash

from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import random
import string
import os

app = Flask(__name__)
app.secret_key = 'nexomart_secret_key_2024'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///nexomart.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

def generate_order_id():
    return 'NXM' + ''.join(random.choices(string.digits, k=10))
# ─── AUTH ───────────────────────────────────────────────────────────────────
@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        password = request.form['password']
        if User.query.filter_by(email=email).first():
            flash('Email already registered!', 'danger')
            return redirect(url_for('register'))
        
        hashed_password = generate_password_hash(password)
        user = User(name=name, email=email, phone=phone,
                    password_hash=hashed_password)
        

        db.session.add(user)
        db.session.commit()
        flash('Account created! Please login.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()

        # if user and check_password_hash(user.password, password):
        if user and check_password_hash(user.password_hash, password):
            session['user_id'] = user.id
            session['user_name'] = user.name
            flash(f'Welcome back, {user.name}!', 'success')
            return redirect(url_for('index'))
        flash('Invalid credentials!', 'danger')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

# ─── HOME ────────────────────────────────────────────────────────────────────
@app.route('/')
def index():
    categories = Category.query.all()
    featured = Product.query.filter_by(is_featured=True).limit(8).all()
    deals = Product.query.filter(Product.discount > 20).limit(8).all()
    new_arrivals = Product.query.order_by(Product.id.desc()).limit(8).all()
    return render_template('index.html', categories=categories,
                           featured=featured, deals=deals, new_arrivals=new_arrivals)

# ─── PRODUCTS ────────────────────────────────────────────────────────────────
@app.route('/products')
def products():
    q = request.args.get('q', '')
    cat = request.args.get('category', '')
    sort = request.args.get('sort', 'popular')
    min_price = request.args.get('min_price', 0, type=float)
    max_price = request.args.get('max_price', 999999, type=float)

    query = Product.query
    if q:
        query = query.filter(Product.name.ilike(f'%{q}%'))
    if cat:
        category = Category.query.filter_by(slug=cat).first()
        if category:
            query = query.filter_by(category_id=category.id)
    query = query.filter(Product.price >= min_price, Product.price <= max_price)
    if sort == 'price_asc':
        query = query.order_by(Product.price.asc())
    elif sort == 'price_desc':
        query = query.order_by(Product.price.desc())
    elif sort == 'newest':
        query = query.order_by(Product.id.desc())
    else:
        query = query.order_by(Product.rating.desc())

    products = query.all()
    categories = Category.query.all()
    return render_template('products.html', products=products, categories=categories,
                           q=q, selected_cat=cat, sort=sort)

@app.route('/product/<int:pid>')
def product_detail(pid):
    product = Product.query.get_or_404(pid)
    reviews = Review.query.filter_by(product_id=pid).all()
    related = Product.query.filter_by(category_id=product.category_id).filter(Product.id != pid).limit(4).all()
    in_wishlist = False
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
        in_wishlist = str(pid) in (user.wishlist or '').split(',')
    return render_template('product_detail.html', product=product,
                           reviews=reviews, related=related, in_wishlist=in_wishlist)

# ─── CART ─────────────────────────────────────────────────────────────────────
@app.route('/cart')
def cart():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    items = CartItem.query.filter_by(user_id=session['user_id']).all()
    total = sum(i.product.price * (1 - i.product.discount/100) * i.quantity for i in items)
    return render_template('cart.html', items=items, total=total)

@app.route('/cart/add/<int:pid>', methods=['POST'])
def add_to_cart(pid):
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'Login required'})
    qty = int(request.form.get('quantity', 1))
    item = CartItem.query.filter_by(user_id=session['user_id'], product_id=pid).first()
    if item:
        item.quantity += qty
    else:
        item = CartItem(user_id=session['user_id'], product_id=pid, quantity=qty)
        db.session.add(item)
    db.session.commit()
    cart_count = CartItem.query.filter_by(user_id=session['user_id']).count()
    return jsonify({'success': True, 'cart_count': cart_count})

@app.route('/cart/remove/<int:item_id>')
def remove_from_cart(item_id):
    item = CartItem.query.get_or_404(item_id)
    if item.user_id == session.get('user_id'):
        db.session.delete(item)
        db.session.commit()
    return redirect(url_for('cart'))

@app.route('/cart/update/<int:item_id>', methods=['POST'])
def update_cart(item_id):
    item = CartItem.query.get_or_404(item_id)
    if item.user_id == session.get('user_id'):
        qty = int(request.form.get('quantity', 1))
        if qty <= 0:
            db.session.delete(item)
        else:
            item.quantity = qty
        db.session.commit()
    return redirect(url_for('cart'))

# ─── WISHLIST ─────────────────────────────────────────────────────────────────
@app.route('/wishlist/toggle/<int:pid>')
def toggle_wishlist(pid):
    if 'user_id' not in session:
        return jsonify({'success': False})
    user = User.query.get(session['user_id'])
    wishlist = set(filter(None, (user.wishlist or '').split(',')))
    if str(pid) in wishlist:
        wishlist.discard(str(pid))
        added = False
    else:
        wishlist.add(str(pid))
        added = True
    user.wishlist = ','.join(wishlist)
    db.session.commit()
    return jsonify({'success': True, 'added': added})

@app.route('/wishlist')
def wishlist():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user = User.query.get(session['user_id'])
    ids = list(filter(None, (user.wishlist or '').split(',')))
    products = Product.query.filter(Product.id.in_(ids)).all() if ids else []
    return render_template('wishlist.html', products=products)

# ─── CHECKOUT ────────────────────────────────────────────────────────────────
@app.route('/checkout', methods=['GET','POST'])
def checkout():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    items = CartItem.query.filter_by(user_id=session['user_id']).all()
    if not items:
        flash('Cart is empty!', 'warning')
        return redirect(url_for('cart'))

    if request.method == 'POST':
        address_line = request.form['address']
        city = request.form['city']
        state = request.form['state']
        pincode = request.form['pincode']
        payment = request.form['payment']

        order_id = generate_order_id()
        total = sum(i.product.price * (1 - i.product.discount/100) * i.quantity for i in items)
        est_delivery = datetime.now() + timedelta(days=random.randint(3, 7))

        order = Order(
            order_id=order_id, user_id=session['user_id'],
            total_amount=round(total, 2), status='Confirmed',
            address=f"{address_line}, {city}, {state} - {pincode}",
            payment_method=payment,
            estimated_delivery=est_delivery
        )
        db.session.add(order)
        db.session.flush()

        for item in items:
            oi = OrderItem(order_id=order.id, product_id=item.product_id,
                           quantity=item.quantity,
                           price=round(item.product.price * (1 - item.product.discount/100), 2))
            db.session.add(oi)
            db.session.delete(item)

        db.session.commit()
        flash(f'Order {order_id} placed successfully!', 'success')
        return redirect(url_for('order_detail', order_id=order_id))

    total = sum(i.product.price * (1 - i.product.discount/100) * i.quantity for i in items)
    addresses = Address.query.filter_by(user_id=session['user_id']).all()
    return render_template('checkout.html', items=items, total=total, addresses=addresses)

# ─── ORDERS ──────────────────────────────────────────────────────────────────
@app.route('/orders')
def orders():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user_orders = Order.query.filter_by(user_id=session['user_id']).order_by(Order.created_at.desc()).all()
    return render_template('orders.html', orders=user_orders)

@app.route('/order/<order_id>')
def order_detail(order_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    order = Order.query.filter_by(order_id=order_id, user_id=session['user_id']).first_or_404()
    # Simulate tracking steps
    steps = [
        ('Order Placed', order.created_at, True),
        ('Order Confirmed', order.created_at + timedelta(hours=1), order.status in ['Confirmed','Shipped','Out for Delivery','Delivered']),
        ('Shipped', order.created_at + timedelta(days=1), order.status in ['Shipped','Out for Delivery','Delivered']),
        ('Out for Delivery', order.estimated_delivery - timedelta(hours=4), order.status in ['Out for Delivery','Delivered']),
        ('Delivered', order.estimated_delivery, order.status == 'Delivered'),
    ]
    return render_template('order_detail.html', order=order, steps=steps)

@app.route('/order/cancel/<order_id>')
def cancel_order(order_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    order = Order.query.filter_by(order_id=order_id, user_id=session['user_id']).first_or_404()
    if order.status in ['Confirmed', 'Processing']:
        order.status = 'Cancelled'
        db.session.commit()
        flash('Order cancelled successfully.', 'success')
    else:
        flash('This order cannot be cancelled.', 'danger')
    return redirect(url_for('order_detail', order_id=order_id))

# ─── REVIEWS ─────────────────────────────────────────────────────────────────
@app.route('/review/<int:pid>', methods=['POST'])
def add_review(pid):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    rating = int(request.form['rating'])
    comment = request.form['comment']
    review = Review(product_id=pid, user_id=session['user_id'],
                    rating=rating, comment=comment)
    db.session.add(review)
    # Update product avg rating
    product = Product.query.get(pid)
    reviews = Review.query.filter_by(product_id=pid).all()
    product.rating = round((sum(r.rating for r in reviews) + rating) / (len(reviews) + 1), 1)
    db.session.commit()
    flash('Review submitted!', 'success')
    return redirect(url_for('product_detail', pid=pid))

# ─── PROFILE ─────────────────────────────────────────────────────────────────
@app.route('/profile', methods=['GET','POST'])
def profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user = User.query.get(session['user_id'])
    if request.method == 'POST':
        user.name = request.form['name']
        user.phone = request.form['phone']
        db.session.commit()
        session['user_name'] = user.name
        flash('Profile updated!', 'success')
    return render_template('profile.html', user=user)

@app.route('/address/add', methods=['POST'])
def add_address():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    addr = Address(
        user_id=session['user_id'],
        name=request.form['name'],
        phone=request.form['phone'],
        address_line=request.form['address_line'],
        city=request.form['city'],
        state=request.form['state'],
        pincode=request.form['pincode'],
        address_type=request.form.get('address_type', 'Home')
    )
    db.session.add(addr)
    db.session.commit()
    flash('Address added!', 'success')
    return redirect(url_for('profile'))

# ─── API ─────────────────────────────────────────────────────────────────────
@app.route('/api/cart_count')
def cart_count():
    if 'user_id' not in session:
        return jsonify({'count': 0})
    count = CartItem.query.filter_by(user_id=session['user_id']).count()
    return jsonify({'count': count})

@app.route('/api/search_suggestions')
def search_suggestions():
    q = request.args.get('q', '')
    if len(q) < 2:
        return jsonify([])
    products = Product.query.filter(Product.name.ilike(f'%{q}%')).limit(5).all()
    return jsonify([{'id': p.id, 'name': p.name, 'price': p.price} for p in products])

# ─── CONTEXT PROCESSORS ──────────────────────────────────────────────────────
@app.context_processor
def inject_globals():
    cart_count = 0
    if 'user_id' in session:
        cart_count = CartItem.query.filter_by(user_id=session['user_id']).count()
    categories = Category.query.all()
    return dict(cart_count=cart_count, all_categories=categories,
                current_year=datetime.now().year)

@app.route('/admin')
def admin_dashboard():
    print("ADMIN ROUTE HIT")
    if not session.get('user_id'):
        return redirect(url_for('login'))

    user = User.query.get(session['user_id'])

    if user.role != 'admin':
        flash('Access denied', 'danger')
        return redirect(url_for('index'))

    return render_template('admin/dashboard.html')

print(app.url_map)
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        from seed import seed_data
        seed_data()
    app.run(debug=True)


