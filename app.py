
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import sqlite3
import json
from datetime import datetime
import os
import uuid
import requests
from cj_client import CJDropshippingClient

app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)

cj_client = CJDropshippingClient()

DATABASE = 'babyzion.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

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
                ('P001', 'Somali Dirac Baby Set', 'Premium cultural wear', 3500, 'Cultural Baby Wear', 'dirac.jpg'),
                ('P002', 'Montessori Wooden Rattle', '100% organic beech wood', 1500, 'Wooden Toys', 'rattle.jpg'),
                ('P003', 'Newborn Swaddle Pack', '3-piece muslin set', 2200, 'Newborn Essentials', 'swaddle.jpg'),
                ('P004', 'Mom & Baby Ankara Set', 'Matching mommy-me', 5500, 'Mom & Baby Sets', 'ankara.jpg'),
                ('P005', 'Eid Mubarak Onesie', 'Gold embroidery', 2500, 'Cultural Baby Wear', 'eid.jpg'),
                ('P006', 'Silicone Teething Ring', 'Food-grade silicone', 900, 'Wooden Toys', 'teether.jpg')
            ]
            conn.executemany('INSERT INTO products VALUES (?,?,?,?,?,?)', products)
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
    category = request.args.get('category')
    conn = get_db()
    if category:
        rows = conn.execute('SELECT * FROM products WHERE category=? AND in_stock=1', (category,)).fetchall()
    else:
        rows = conn.execute('SELECT * FROM products WHERE in_stock=1').fetchall()
    conn.close()
    return jsonify([dict(row) for row in rows])

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
def create_order():
    try:
        data = request.json
        order_id = f"BZ{uuid.uuid4().hex[:8].upper()}"
        
        conn = get_db()
        conn.execute('''
            INSERT INTO orders (id, customer_name, customer_email, customer_phone,
                              shipping_address, shipping_city, shipping_country,
                              items, subtotal, shipping_cost, total, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            order_id,
            data.get('name'),
            data.get('email'),
            data.get('phone'),
            data.get('address'),
            data.get('city'),
            data.get('country'),
            json.dumps(data.get('items', [])),
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
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

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

# PayPal Payment Integration
@app.route('/api/paypal/create-order', methods=['POST'])
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
@app.route('/api/uploads', methods=['POST'])
def create_upload():
    try:
        data = request.json
        conn = get_db()
        conn.execute('''
            INSERT INTO uploads (product_name, description, price, category, seller_name, seller_email)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            data.get('product_name'),
            data.get('description'),
            float(data.get('price', 0)),
            data.get('category'),
            data.get('seller_name'),
            data.get('seller_email')
        ))
        conn.commit()
        conn.close()
        
        return jsonify({'success': True, 'message': 'Product uploaded for review'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

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
    port = int(os.environ.get('PORT', 5000))
    debug_mode = os.environ.get('FLASK_ENV', 'production') != 'production'
    print("BABYZION MARKET - Starting server...")
    print(f"Server running on http://0.0.0.0:{port}")
    print(f"Environment: {'Development' if debug_mode else 'Production'}")
    app.run(host='0.0.0.0', port=port, debug=debug_mode)