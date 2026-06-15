# 🛒 NEXOMART - AI E-Commerce Platform

A full-featured e-commerce web app inspired by Flipkart, built with Python Flask, SQLite, and dynamic HTML/CSS/JS.

---

## ✅ Features

- 🏠 Homepage with Hero Banner, Featured Products, Deals of Day, New Arrivals
- 🔍 Product Search with Live Suggestions + Filters (Category, Price, Sort)
- 📦 Product Detail Page with Reviews, Ratings, Related Products
- 🛒 Shopping Cart (Add, Remove, Update Quantity)
- ❤️ Wishlist (Toggle products)
- 💳 Checkout with Address + Payment Selection (UPI, Card, COD, Net Banking)
- 📬 Order Placement with unique Order ID
- 📍 **Order Tracking** with Step-by-Step Timeline (Confirmed → Shipped → Out for Delivery → Delivered)
- ❌ Order Cancellation
- ⭐ Product Reviews & Star Ratings
- 👤 User Profile (Edit info, Manage Addresses)
- 🔐 Auth (Register / Login / Logout)
- 📱 Responsive Design

---

## 🚀 Setup & Run (VS Code)

### Step 1: Open the folder in VS Code
```
File → Open Folder → select nexomart/
```

### Step 2: Create a Virtual Environment
```bash
python -m venv venv
```

### Step 3: Activate it
- **Windows:** `venv\Scripts\activate`
- **Mac/Linux:** `source venv/bin/activate`

### Step 4: Install dependencies
```bash
pip install -r requirements.txt
```

### Step 5: Run the app
```bash
python app.py
```

### Step 6: Open in browser
```
http://127.0.0.1:5000
```

---

## 🔑 Demo Login
- **Email:** demo@nexomart.com
- **Password:** demo123

---

## 📁 Project Structure

```
nexomart/
├── app.py              # Main Flask app + all routes
├── database.py         # SQLAlchemy models
├── seed.py             # Sample data (products, categories)
├── requirements.txt
├── instance/
│   └── nexomart.db     # SQLite DB (auto-created)
├── static/
│   ├── css/style.css   # Full Flipkart-style CSS
│   └── js/main.js      # Cart, toast, search JS
└── templates/
    ├── base.html        # Header, footer, nav
    ├── index.html       # Homepage
    ├── products.html    # Product listing + filters
    ├── product_detail.html
    ├── _product_card.html  # Reusable card
    ├── cart.html
    ├── checkout.html
    ├── orders.html
    ├── order_detail.html   # 📍 Tracking page
    ├── login.html
    ├── register.html
    ├── profile.html
    └── wishlist.html
```

---

## 🛠 Tech Stack
- **Backend:** Python Flask
- **Database:** SQLite via Flask-SQLAlchemy
- **Frontend:** HTML5, CSS3, Vanilla JS
- **Icons:** Font Awesome
- **Fonts:** Google Fonts (Poppins)
