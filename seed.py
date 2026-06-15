from database import db, Category, Product, User
from werkzeug.security import generate_password_hash

def seed_data():
    if Category.query.first():
        return  # Already seeded

    # Categories
    cats = [
        Category(name='Electronics', slug='electronics', icon='📱'),
        Category(name='Fashion', slug='fashion', icon='👗'),
        Category(name='Home & Kitchen', slug='home-kitchen', icon='🏠'),
        Category(name='Books', slug='books', icon='📚'),
        Category(name='Sports', slug='sports', icon='⚽'),
        Category(name='Beauty', slug='beauty', icon='💄'),
        Category(name='Toys', slug='toys', icon='🎮'),
        Category(name='Grocery', slug='grocery', icon='🛒'),
    ]
    db.session.add_all(cats)
    db.session.flush()

    e, f, h, b, s, bty, t, g = cats

    products = [
        # Electronics
        Product(name='Samsung Galaxy S24 Ultra 5G', price=124999, discount=15, brand='Samsung',
                category_id=e.id, rating=4.6, review_count=2341, is_featured=True, stock=50,
                image='https://images.unsplash.com/photo-1610945415295-d9bbf067e59c?w=400',
                description='Latest Samsung flagship with 200MP camera, S Pen, 12GB RAM, 256GB storage.',
                specifications='Display: 6.8" Dynamic AMOLED | Battery: 5000mAh | OS: Android 14'),
        Product(name='Apple iPhone 15 Pro Max', price=159900, discount=5, brand='Apple',
                category_id=e.id, rating=4.8, review_count=5432, is_featured=True, stock=30,
                image='https://images.unsplash.com/photo-1696446702183-cbd38f7ada06?w=400',
                description='Titanium design, A17 Pro chip, 48MP camera system, USB-C.',
                specifications='Display: 6.7" Super Retina XDR | Battery: 4422mAh | Chip: A17 Pro'),
        Product(name='Sony WH-1000XM5 Headphones', price=29990, discount=25, brand='Sony',
                category_id=e.id, rating=4.7, review_count=1876, is_featured=True, stock=80,
                image='https://images.unsplash.com/photo-1618366712010-f4ae9c647dcb?w=400',
                description='Industry-leading noise cancellation, 30hr battery, multipoint connection.',
                specifications='Type: Over-ear | Connectivity: Bluetooth 5.2 | Battery: 30hrs'),
        Product(name='Dell XPS 15 Laptop', price=149990, discount=10, brand='Dell',
                category_id=e.id, rating=4.5, review_count=987, is_featured=True, stock=20,
                image='https://images.unsplash.com/photo-1593642632559-0c6d3fc62b89?w=400',
                description='Intel Core i7, 16GB RAM, 512GB SSD, OLED 4K display.',
                specifications='Processor: Intel Core i7-13700H | RAM: 16GB | Storage: 512GB SSD'),
        Product(name='iPad Air 5th Gen', price=59900, discount=8, brand='Apple',
                category_id=e.id, rating=4.6, review_count=2109, stock=45,
                image='https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0?w=400',
                description='M1 chip, 10.9-inch Liquid Retina display, USB-C, Touch ID.',
                specifications='Display: 10.9" Liquid Retina | Chip: M1 | Storage: 64GB'),
        Product(name='OnePlus 12 5G', price=64999, discount=20, brand='OnePlus',
                category_id=e.id, rating=4.4, review_count=1543, stock=60,
                image='https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=400',
                description='Snapdragon 8 Gen 3, 50W wireless charging, Hasselblad cameras.',
                specifications='Display: 6.82" LTPO AMOLED | Battery: 5400mAh | RAM: 12GB'),

        # Fashion
        Product(name="Levi's 501 Original Jeans", price=3999, discount=30, brand="Levi's",
                category_id=f.id, rating=4.3, review_count=892, stock=200,
                image='https://images.unsplash.com/photo-1542272604-787c3835535d?w=400',
                description='Classic straight-fit jeans, 100% cotton denim, timeless style.',
                specifications='Material: 100% Cotton | Fit: Straight | Rise: Mid-rise'),
        Product(name='Nike Air Max 270', price=11995, discount=15, brand='Nike',
                category_id=f.id, rating=4.5, review_count=2341, is_featured=True, stock=150,
                image='https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400',
                description='Largest Air unit yet for all-day comfort and style.',
                specifications='Material: Mesh Upper | Sole: Rubber | Closure: Lace-up'),
        Product(name='Zara Floral Midi Dress', price=5990, discount=40, brand='Zara',
                category_id=f.id, rating=4.2, review_count=567, stock=80,
                image='https://images.unsplash.com/photo-1515372039744-b8f02a3ae446?w=400',
                description='Elegant floral print midi dress, perfect for any occasion.',
                specifications='Material: Polyester | Length: Midi | Care: Machine Washable'),

        # Home & Kitchen
        Product(name='Instant Pot Duo 7-in-1', price=8999, discount=35, brand='Instant Pot',
                category_id=h.id, rating=4.7, review_count=3421, is_featured=True, stock=120,
                image='https://images.unsplash.com/photo-1585515320310-259814833e62?w=400',
                description='Pressure Cooker, Slow Cooker, Rice Cooker, Steamer, 7 functions.',
                specifications='Capacity: 6 Quart | Functions: 7-in-1 | Material: Stainless Steel'),
        Product(name='Dyson V15 Vacuum Cleaner', price=52900, discount=12, brand='Dyson',
                category_id=h.id, rating=4.6, review_count=1234, is_featured=True, stock=35,
                image='https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=400',
                description='Laser Detect technology, 60-min runtime, HEPA filtration.',
                specifications='Type: Cordless | Battery: 60 mins | Filtration: HEPA'),

        # Books
        Product(name='Atomic Habits by James Clear', price=499, discount=20, brand='Penguin',
                category_id=b.id, rating=4.8, review_count=12340, stock=500,
                image='https://images.unsplash.com/photo-1544947950-fa07a98d237f?w=400',
                description='The proven system for building good habits and breaking bad ones.',
                specifications='Pages: 320 | Language: English | Publisher: Penguin'),
        Product(name='Rich Dad Poor Dad', price=299, discount=15, brand='Plata Publishing',
                category_id=b.id, rating=4.6, review_count=8765, stock=400,
                image='https://images.unsplash.com/photo-1589998059171-988d887df646?w=400',
                description="What the rich teach their kids about money that the poor don't.",
                specifications='Pages: 336 | Language: English | Genre: Finance'),

        # Sports
        Product(name='Yonex Arcsaber 11 Badminton Racket', price=14999, discount=18, brand='Yonex',
                category_id=s.id, rating=4.7, review_count=876, stock=60,
                image='https://images.unsplash.com/photo-1626224583764-f87db24ac4ea?w=400',
                description='Professional-grade carbon fiber racket for advanced players.',
                specifications='Weight: 83g | String Tension: 19-27 lbs | Material: HM Graphite'),
        Product(name='Decathlon Fitness Cycle', price=24999, discount=22, brand='Decathlon',
                category_id=s.id, rating=4.4, review_count=543, is_featured=True, stock=25,
                image='https://images.unsplash.com/photo-1534438327276-14e5300c3a48?w=400',
                description='Exercise bike with 8 resistance levels, LCD display, foldable.',
                specifications='Resistance: 8 levels | Display: LCD | Max Weight: 120kg'),

        # Beauty
        Product(name='Lakme 9to5 Foundation', price=449, discount=25, brand='Lakme',
                category_id=bty.id, rating=4.3, review_count=2341, stock=300,
                image='https://images.unsplash.com/photo-1522335789203-aabd1fc54bc9?w=400',
                description='Full coverage, long-lasting foundation for all skin types.',
                specifications='Type: Foundation | Coverage: Full | Finish: Matte'),
        Product(name='The Ordinary Niacinamide Serum', price=699, discount=10, brand='The Ordinary',
                category_id=bty.id, rating=4.6, review_count=4532, stock=200,
                image='https://images.unsplash.com/photo-1620916566398-39f1143ab7be?w=400',
                description='10% Niacinamide + 1% Zinc for pore minimising and blemish reduction.',
                specifications='Type: Serum | Volume: 30ml | Skin Type: All'),
    ]

    db.session.add_all(products)

    # Demo user
    demo = User(name='Rahul Sharma', email='demo@nexomart.com',
                phone='9876543210', password=generate_password_hash('demo123'))
    db.session.add(demo)
    db.session.commit()
    print("✅ Database seeded successfully!")
