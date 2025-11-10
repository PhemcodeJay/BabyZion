
from flask import Flask, jsonify, request, send_from_directory, session
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import sqlite3
import json
from datetime import datetime
import os
import uuid
import requests
import secrets
import re
from cj_client import CJDropshippingClient

app = Flask(__name__, static_folder='.', static_url_path='')
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', secrets.token_hex(32))
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

CORS(app, supports_credentials=True)

# Rate limiting
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://"
)

cj_client = CJDropshippingClient()

DATABASE = 'babyzion.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_phone(phone):
    """Validate phone number format"""
    pattern = r'^\+?[0-9]{10,15}$'
    return re.match(pattern, phone.replace(' ', '').replace('-', '')) is not None

def sanitize_input(text, max_length=500):
    """Sanitize user input"""
    if not text:
        return ""
    text = str(text).strip()
    return text[:max_length]

def init_db():
    with app.app_context():
        conn = get_db()
        conn.executescript('''
            CREATE TABLE IF NOT EXISTS products (
                id TEXT PRIMARY KEY, name TEXT, description TEXT, price REAL,
                category TEXT, image TEXT, in_stock INTEGER DEFAULT 1
            );
            CREATE TABLE IF NOT EXISTS orders (
                id TEXT PRIMARY KEY, customer_name TEXT, customer_email TEXT,
                customer_phone TEXT, shipping_address TEXT, shipping_city TEXT,
                shipping_country TEXT, items TEXT, subtotal REAL,
                shipping_cost REAL, total REAL, status TEXT DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            CREATE TABLE IF NOT EXISTS uploads (
                id INTEGER PRIMARY KEY AUTOINCREMENT, product_name TEXT,
                description TEXT, price REAL, category TEXT,
                seller_name TEXT, seller_email TEXT, status TEXT DEFAULT 'pending'
            );
        ''')
        
        count = conn.execute('SELECT COUNT(*) FROM products').fetchone()[0]
        if count == 0:
            products = [
                ('P001', 'Somali Dirac Baby Set', 'Premium cultural wear', 35.00, 'Cultural Baby Wear', 'https://images.unsplash.com/photo-1515488042361-ee00e0ddd4e4?w=400&h=400&fit=crop', 1),
                ('P002', 'Montessori Wooden Rattle', '100% organic beech wood', 15.00, 'Wooden Toys', 'https://images.unsplash.com/photo-1580130732478-3ddc2f96f6e4?w=400&h=400&fit=crop', 1),
                ('P003', 'Newborn Swaddle Pack', '3-piece muslin set', 22.00, 'Newborn Essentials', 'https://images.unsplash.com/photo-1515488042361-ee00e0ddd4e4?w=400&h=400&fit=crop', 1),
                ('P004', 'Mom & Baby Ankara Set', 'Matching mommy-me', 55.00, 'Mom & Baby Sets', 'https://images.unsplash.com/photo-1566694271453-390536dd1f0d?w=400&h=400&fit=crop', 1),
                ('P005', 'Eid Mubarak Onesie', 'Gold embroidery', 25.00, 'Cultural Baby Wear', 'https://images.unsplash.com/photo-1515488042361-ee00e0ddd4e4?w=400&h=400&fit=crop', 1),
                ('P006', 'Silicone Teething Ring', 'Food-grade silicone', 9.00, 'Wooden Toys', 'https://images.unsplash.com/photo-1580130732478-3ddc2f96f6e4?w=400&h=400&fit=crop', 1)
            ]
            conn.executemany('INSERT INTO products VALUES (?,?,?,?,?,?,?)', products)
            print(f"✅ Seeded {len(products)} products into database")
        conn.commit()

init_db()

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def static_files(path):
    return send_from_directory('.', path)

@app.route('/api/products')
def products():
    try:
        category = request.args.get('category')
        conn = get_db()
        if category:
            rows = conn.execute('SELECT * FROM products WHERE category=? AND in_stock=1', (category,)).fetchall()
        else:
            rows = conn.execute('SELECT * FROM products WHERE in_stock=1').fetchall()
        conn.close()
        products_list = [dict(row) for row in rows]
        print(f"✅ Returning {len(products_list)} products")
        return jsonify(products_list)
    except Exception as e:
        print(f"❌ Error fetching products: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/categories')
def categories():
    conn = get_db()
    cats = conn.execute('SELECT DISTINCT category FROM products').fetchall()
    conn.close()
    return jsonify([row['category'] for row in cats])

# CJ Dropshipping Integration
@app.route('/api/cj/sync', methods=['POST'])
def sync_cj_products():
    try:
        data = request.json or {}
        keyword = data.get('keyword', 'baby')
        page_size = min(int(data.get('page_size', 50)), 100)
        
        products = cj_client.search_products(keyword=keyword, page_size=page_size)
        
        if not products:
            return jsonify({
                'success': False, 
                'message': 'No products found or CJ API not configured',
                'hint': 'Set CJ_EMAIL and CJ_API_KEY environment variables'
            }), 200
        
        conn = get_db()
        added = 0
        for product in products:
            try:
                conn.execute('''
                    INSERT OR REPLACE INTO products (id, name, description, price, category, image, in_stock)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (product['id'], product['name'], product['description'], 
                      product['price'], product['category'], product['image'], product['in_stock']))
                added += 1
            except Exception as e:
                print(f"Error inserting product: {e}")
        
        conn.commit()
        conn.close()
        
        return jsonify({
            'success': True,
            'message': f'Synced {added} products from CJ Dropshipping',
            'count': added
        })
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

# Orders Management
@app.route('/api/orders', methods=['POST'])
@limiter.limit("10 per hour")
def create_order():
    try:
        data = request.json
        
        # Validate required fields
        required_fields = ['name', 'email', 'phone', 'address', 'city', 'country', 'items']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'success': False, 'message': f'Missing required field: {field}'}), 400
        
        # Validate email
        if not validate_email(data.get('email')):
            return jsonify({'success': False, 'message': 'Invalid email format'}), 400
        
        # Validate phone
        if not validate_phone(data.get('phone')):
            return jsonify({'success': False, 'message': 'Invalid phone number'}), 400
        
        # Sanitize inputs
        customer_name = sanitize_input(data.get('name'), 100)
        customer_email = sanitize_input(data.get('email'), 100)
        customer_phone = sanitize_input(data.get('phone'), 20)
        shipping_address = sanitize_input(data.get('address'), 200)
        shipping_city = sanitize_input(data.get('city'), 100)
        shipping_country = sanitize_input(data.get('country'), 100)
        
        # Validate items
        items = data.get('items', [])
        if not items or not isinstance(items, list):
            return jsonify({'success': False, 'message': 'Invalid items'}), 400
        
        order_id = f"BZ{uuid.uuid4().hex[:8].upper()}"
        
        conn = get_db()
        conn.execute('''
            INSERT INTO orders (id, customer_name, customer_email, customer_phone,
                              shipping_address, shipping_city, shipping_country,
                              items, subtotal, shipping_cost, total, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            order_id,
            customer_name,
            customer_email,
            customer_phone,
            shipping_address,
            shipping_city,
            shipping_country,
            json.dumps(items),
            float(data.get('subtotal', 0)),
            float(data.get('shipping_cost', 12)),
            float(data.get('total', 0)),
            'pending'
        ))
        conn.commit()
        conn.close()
        
        return jsonify({
            'success': True,
            'order_id': order_id,
            'message': 'Order created successfully'
        })
    except ValueError as e:
        return jsonify({'success': False, 'message': 'Invalid numeric value'}), 400
    except Exception as e:
        return jsonify({'success': False, 'message': 'Server error'}), 500

@app.route('/api/orders/<order_id>', methods=['GET'])
def get_order(order_id):
    try:
        conn = get_db()
        order = conn.execute('SELECT * FROM orders WHERE id=?', (order_id,)).fetchone()
        conn.close()
        
        if order:
            return jsonify(dict(order))
        else:
            return jsonify({'error': 'Order not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Paystack Payment Integration
@app.route('/api/paystack/initialize', methods=['POST'])
@limiter.limit("10 per hour")
def initialize_paystack():
    try:
        paystack_public_key = os.environ.get('PAYSTACK_PUBLIC_KEY', '')
        
        if not paystack_public_key:
            return jsonify({
                'success': False,
                'message': 'Paystack not configured',
                'hint': 'Set PAYSTACK_PUBLIC_KEY environment variable'
            }), 200
        
        return jsonify({
            'success': True,
            'public_key': paystack_public_key
        })
    except Exception as e:
        return jsonify({'success': False, 'message': 'Server error'}), 500

# PayPal Payment Integration
@app.route('/api/paypal/create-order', methods=['POST'])
@limiter.limit("10 per hour")
def create_paypal_order():
    try:
        data = request.json
        amount = data.get('amount', 0)
        
        paypal_client_id = os.environ.get('PAYPAL_CLIENT_ID', '')
        paypal_secret = os.environ.get('PAYPAL_CLIENT_SECRET', '')
        
        if not paypal_client_id or not paypal_secret:
            return jsonify({
                'success': False,
                'message': 'PayPal credentials not configured',
                'hint': 'Set PAYPAL_CLIENT_ID and PAYPAL_CLIENT_SECRET'
            }), 200
        
        paypal_base = os.environ.get('PAYPAL_BASE_URL', 'https://api-m.sandbox.paypal.com')
        
        auth_response = requests.post(
            f'{paypal_base}/v1/oauth2/token',
            auth=(paypal_client_id, paypal_secret),
            data={'grant_type': 'client_credentials'},
            headers={'Content-Type': 'application/x-www-form-urlencoded'}
        )
        
        if not auth_response.ok:
            return jsonify({'success': False, 'message': 'PayPal authentication failed'}), 500
        
        access_token = auth_response.json()['access_token']
        
        order_response = requests.post(
            f'{paypal_base}/v2/checkout/orders',
            headers={
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {access_token}'
            },
            json={
                'intent': 'CAPTURE',
                'purchase_units': [{
                    'amount': {
                        'currency_code': 'USD',
                        'value': f'{amount:.2f}'
                    }
                }]
            }
        )
        
        if order_response.ok:
            order_data = order_response.json()
            return jsonify({'success': True, 'order_id': order_data['id']})
        else:
            return jsonify({'success': False, 'message': 'Failed to create PayPal order'}), 500
            
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/paypal/capture-order/<order_id>', methods=['POST'])
def capture_paypal_order(order_id):
    try:
        paypal_client_id = os.environ.get('PAYPAL_CLIENT_ID', '')
        paypal_secret = os.environ.get('PAYPAL_CLIENT_SECRET', '')
        paypal_base = os.environ.get('PAYPAL_BASE_URL', 'https://api-m.sandbox.paypal.com')
        
        auth_response = requests.post(
            f'{paypal_base}/v1/oauth2/token',
            auth=(paypal_client_id, paypal_secret),
            data={'grant_type': 'client_credentials'},
            headers={'Content-Type': 'application/x-www-form-urlencoded'}
        )
        
        access_token = auth_response.json()['access_token']
        
        capture_response = requests.post(
            f'{paypal_base}/v2/checkout/orders/{order_id}/capture',
            headers={
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {access_token}'
            }
        )
        
        if capture_response.ok:
            return jsonify({'success': True, 'data': capture_response.json()})
        else:
            return jsonify({'success': False, 'message': 'Failed to capture payment'}), 500
            
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

# Seller Upload
@app.route('/api/uploads', methods=['GET', 'POST'])
@limiter.limit("5 per hour")
def handle_uploads():
    if request.method == 'GET':
        try:
            conn = get_db()
            uploads = conn.execute('SELECT * FROM uploads ORDER BY id DESC LIMIT 100').fetchall()
            conn.close()
            return jsonify([dict(upload) for upload in uploads])
        except Exception as e:
            return jsonify({'error': 'Server error'}), 500
    else:
        try:
            data = request.json
            
            # Validate required fields
            if not data.get('product_name') or not data.get('seller_email'):
                return jsonify({'success': False, 'message': 'Missing required fields'}), 400
            
            # Validate email
            if not validate_email(data.get('seller_email')):
                return jsonify({'success': False, 'message': 'Invalid email format'}), 400
            
            # Validate price
            try:
                price = float(data.get('price', 0))
                if price < 0 or price > 10000:
                    return jsonify({'success': False, 'message': 'Invalid price range'}), 400
            except ValueError:
                return jsonify({'success': False, 'message': 'Invalid price'}), 400
            
            # Sanitize inputs
            product_name = sanitize_input(data.get('product_name'), 200)
            description = sanitize_input(data.get('description'), 1000)
            category = sanitize_input(data.get('category'), 100)
            seller_name = sanitize_input(data.get('seller_name'), 100)
            seller_email = sanitize_input(data.get('seller_email'), 100)
            
            conn = get_db()
            conn.execute('''
                INSERT INTO uploads (product_name, description, price, category, seller_name, seller_email)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (product_name, description, price, category, seller_name, seller_email))
            conn.commit()
            conn.close()
            
            return jsonify({'success': True, 'message': 'Product uploaded for review'})
        except Exception as e:
            return jsonify({'success': False, 'message': 'Server error'}), 500

@app.errorhandler(404)
def not_found(e):
    return jsonify({'error': 'Resource not found'}), 404

@app.errorhandler(500)
def internal_error(e):
    return jsonify({'error': 'Internal server error'}), 500

@app.after_request
def add_header(response):
    if os.environ.get('FLASK_ENV', 'production') != 'production':
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
    return response

if __name__ == '__main__':
    # Ensure database is initialized
    print("BABYZION MARKET - Initializing database...")
    init_db()
    
    port = int(os.environ.get('PORT', 5000))
    debug_mode = os.environ.get('FLASK_ENV', 'production') != 'production'
    print("BABYZION MARKET - Starting server...")
    print(f"Server running on http://0.0.0.0:{port}")
    print(f"Environment: {'Development' if debug_mode else 'Production'}")
    print(f"Access the app at: http://0.0.0.0:{port}")
    app.run(host='0.0.0.0', port=port, debug=debug_mode)