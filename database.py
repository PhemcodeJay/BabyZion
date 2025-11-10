
import sqlite3
import json
from datetime import datetime

DATABASE = 'babyzion.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    
    # Create products table
    c.execute('''CREATE TABLE IF NOT EXISTS products
                 (id TEXT PRIMARY KEY,
                  name TEXT NOT NULL,
                  description TEXT,
                  price REAL NOT NULL,
                  category TEXT,
                  image TEXT,
                  in_stock INTEGER DEFAULT 1,
                  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    
    # Create orders table
    c.execute('''CREATE TABLE IF NOT EXISTS orders
                 (id TEXT PRIMARY KEY,
                  customer_name TEXT NOT NULL,
                  customer_email TEXT NOT NULL,
                  customer_phone TEXT,
                  shipping_address TEXT,
                  shipping_city TEXT,
                  shipping_country TEXT,
                  items TEXT NOT NULL,
                  subtotal REAL NOT NULL,
                  shipping_cost REAL NOT NULL,
                  total REAL NOT NULL,
                  status TEXT DEFAULT 'pending',
                  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    
    # Create uploads table
    c.execute('''CREATE TABLE IF NOT EXISTS uploads
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  product_name TEXT NOT NULL,
                  description TEXT,
                  price REAL NOT NULL,
                  category TEXT,
                  seller_name TEXT NOT NULL,
                  seller_email TEXT NOT NULL,
                  status TEXT DEFAULT 'pending',
                  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    
    # Check if products already exist
    count = c.execute('SELECT COUNT(*) FROM products').fetchone()[0]
    
    # Seed initial products if table is empty
    if count == 0:
        products = [
            ('prod_001', 'Organic Cotton Baby Blanket', 'Soft, breathable blanket made from 100% organic cotton. Perfect for newborns.', 34.99, 'Newborn Essentials', 'https://images.unsplash.com/photo-1515488042361-ee00e0ddd4e4?w=400&h=400&fit=crop'),
            ('prod_002', 'Handcrafted Wooden Rattle', 'Natural wood baby rattle, safe and eco-friendly. Great for sensory development.', 18.50, 'Wooden Toys', 'https://images.unsplash.com/photo-1580130732478-3ddc2f96f6e4?w=400&h=400&fit=crop'),
            ('prod_003', 'Cultural Baby Carrier Wrap', 'Traditional baby wrap with modern comfort. Celebrates cultural heritage.', 55.00, 'Mom & Baby Sets', 'https://images.unsplash.com/photo-1566694271453-390536dd1f0d?w=400&h=400&fit=crop'),
            ('prod_004', 'Montessori Wooden Play Set', 'Educational toy set promoting learning through play. Made from sustainable wood.', 42.00, 'Educational Toys', 'https://images.unsplash.com/photo-1587654780291-39c9404d746b?w=400&h=400&fit=crop'),
            ('prod_005', 'Organic Baby Food Starter Kit', 'Complete set for making healthy homemade baby food. BPA-free containers included.', 38.99, 'Feeding & Nursing', 'https://images.unsplash.com/photo-1609220136736-443140cffec6?w=400&h=400&fit=crop'),
            ('prod_006', 'Silicone Baby Feeding Set', 'Complete feeding set: plate, bowl, spoon. BPA-free, dishwasher safe.', 29.99, 'Feeding & Nursing', 'https://images.unsplash.com/photo-1609220136736-443140cffec6?w=400&h=400&fit=crop'),
            ('prod_007', 'Eid Special Baby Outfit', 'Beautiful handcrafted outfit for Eid celebrations. Includes matching accessories.', 48.00, 'Cultural Baby Wear', 'https://images.unsplash.com/photo-1515488042361-ee00e0ddd4e4?w=400&h=400&fit=crop'),
            ('prod_008', 'Wooden Pull-Along Duck', 'Classic wooden pull toy. Perfect for toddlers learning to walk.', 22.00, 'Wooden Toys', 'https://images.unsplash.com/photo-1587037577931-11f85e70daac?w=400&h=400&fit=crop'),
            ('prod_009', 'African Print Baby Romper', 'Vibrant African print romper. Comfortable, stylish, and celebrates culture.', 28.00, 'Cultural Baby Wear', 'https://images.unsplash.com/photo-1522771930-78848d9293e8?w=400&h=400&fit=crop'),
            ('prod_010', 'Nursing Pillow', 'Ergonomic nursing pillow with removable, washable cover. Makes feeding comfortable.', 39.99, 'Mom & Baby Sets', 'https://images.unsplash.com/photo-1566694271453-390536dd1f0d?w=400&h=400&fit=crop'),
            ('prod_011', 'Organic Baby Gift Basket', 'Complete gift set with organic essentials. Perfect for baby showers!', 65.00, 'Newborn Essentials', 'https://images.unsplash.com/photo-1515488042361-ee00e0ddd4e4?w=400&h=400&fit=crop'),
            ('prod_012', 'Bamboo Baby Utensils', 'Eco-friendly bamboo spoons and forks. Safe for babies and the environment.', 16.50, 'Feeding & Nursing', 'https://images.unsplash.com/photo-1609220136736-443140cffec6?w=400&h=400&fit=crop'),
            ('prod_013', 'Cultural Lullaby Music Box', 'Wooden music box playing traditional lullabies from around the world.', 32.00, 'Educational Toys', 'https://images.unsplash.com/photo-1587654780291-39c9404d746b?w=400&h=400&fit=crop'),
            ('prod_014', 'Organic Teething Rings', 'Set of 3 organic cotton teething rings. Safe, soothing, and washable.', 24.99, 'Newborn Essentials', 'https://images.unsplash.com/photo-1515488042361-ee00e0ddd4e4?w=400&h=400&fit=crop'),
            ('prod_015', 'Mom & Baby Matching Set', 'Matching outfit set for mom and baby. Comfortable and stylish.', 78.00, 'Mom & Baby Sets', 'https://images.unsplash.com/photo-1566694271453-390536dd1f0d?w=400&h=400&fit=crop')
        ]
        
        c.executemany('INSERT INTO products (id, name, description, price, category, image) VALUES (?, ?, ?, ?, ?, ?)', products)
        conn.commit()
        print(f"✅ Seeded {len(products)} products into database")
    
    conn.close()

if __name__ == '__main__':
    init_db()
    print("Database initialized successfully!")
