
#!/usr/bin/env python3
import sqlite3
import os

DATABASE = 'babyzion.db'

def init_database():
    # Remove existing database
    if os.path.exists(DATABASE):
        os.remove(DATABASE)
        print(f"✅ Removed existing database: {DATABASE}")
    
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
    
    # Seed 100 products with diverse images
    products = [
        # Newborn Essentials (20 products)
        ('prod_001', 'Organic Cotton Baby Blanket', 'Soft, breathable blanket made from 100% organic cotton. Perfect for newborns.', 34.99, 'Newborn Essentials', 'https://images.unsplash.com/photo-1519689373023-dd07c7988603?w=400&h=400&fit=crop', 1),
        ('prod_002', 'Muslin Swaddle Set (3-Pack)', 'Breathable muslin swaddles in beautiful prints. Essential for every newborn.', 28.50, 'Newborn Essentials', 'https://images.unsplash.com/photo-1617479187759-37cda2ad2b5a?w=400&h=400&fit=crop', 1),
        ('prod_003', 'Organic Teething Rings', 'Set of 3 organic cotton teething rings. Safe, soothing, and washable.', 24.99, 'Newborn Essentials', 'https://images.unsplash.com/photo-1596461404969-9ae70f2830c1?w=400&h=400&fit=crop', 1),
        ('prod_004', 'Organic Baby Gift Basket', 'Complete gift set with organic essentials. Perfect for baby showers!', 65.00, 'Newborn Essentials', 'https://images.unsplash.com/photo-1608364099111-9a1e8a344a68?w=400&h=400&fit=crop', 1),
        ('prod_005', 'Bamboo Baby Bath Towel Set', 'Ultra-soft bamboo hooded towels. Hypoallergenic and gentle on skin.', 32.00, 'Newborn Essentials', 'https://images.unsplash.com/photo-1620188526357-ff08e03ed498?w=400&h=400&fit=crop', 1),
        ('prod_006', 'Newborn Onesie Set (5-Pack)', 'Soft cotton onesies in neutral colors. Essential wardrobe basics.', 29.99, 'Newborn Essentials', 'https://images.unsplash.com/photo-1515488042361-ee00e0ddd4e4?w=400&h=400&fit=crop', 1),
        ('prod_007', 'Baby Mittens & Booties Set', 'Keep tiny hands and feet warm. Made from organic cotton.', 18.50, 'Newborn Essentials', 'https://images.unsplash.com/photo-1612818192304-f01419a572ce?w=400&h=400&fit=crop', 1),
        ('prod_008', 'Sleep Sack Swaddle', 'Safe sleep solution for newborns. Prevents startle reflex.', 36.00, 'Newborn Essentials', 'https://images.unsplash.com/photo-1602524206684-b3e9a8dca89d?w=400&h=400&fit=crop', 1),
        ('prod_009', 'Burp Cloth Set (6-Pack)', 'Super absorbent organic cotton burp cloths. Essential for feeding time.', 22.00, 'Newborn Essentials', 'https://images.unsplash.com/photo-1522771930-78848d9293e8?w=400&h=400&fit=crop', 1),
        ('prod_010', 'Newborn Hat Collection', 'Adorable hats to keep baby warm. Set of 4 different styles.', 24.99, 'Newborn Essentials', 'https://images.unsplash.com/photo-1584473457325-7ae49767c846?w=400&h=400&fit=crop', 1),
        ('prod_011', 'Organic Receiving Blankets', 'Versatile blankets for swaddling, nursing, and more. Pack of 3.', 31.50, 'Newborn Essentials', 'https://images.unsplash.com/photo-1566694271453-390536dd1f0d?w=400&h=400&fit=crop', 1),
        ('prod_012', 'Baby Bath Time Essentials', 'Complete bath set with soft towel, washcloths, and gentle soap.', 42.00, 'Newborn Essentials', 'https://images.unsplash.com/photo-1600618528240-fb9fc964b853?w=400&h=400&fit=crop', 1),
        ('prod_013', 'Newborn Photo Props Set', 'Adorable props for memorable newborn photos. Includes wraps and headbands.', 38.50, 'Newborn Essentials', 'https://images.unsplash.com/photo-1555252333-9f8e92e65df9?w=400&h=400&fit=crop', 1),
        ('prod_014', 'Organic Crib Sheets (2-Pack)', 'Soft, breathable sheets that fit standard cribs. Easy to wash.', 35.00, 'Newborn Essentials', 'https://images.unsplash.com/photo-1515488042361-ee00e0ddd4e4?w=400&h=400&fit=crop', 1),
        ('prod_015', 'Baby Pacifier Set', 'Orthodontic pacifiers in different sizes. BPA-free and safe.', 16.99, 'Newborn Essentials', 'https://images.unsplash.com/photo-1590736969955-71cc94901144?w=400&h=400&fit=crop', 1),
        ('prod_016', 'Hooded Baby Bathrobe', 'Plush hooded robe for after bath time. Super soft and absorbent.', 28.00, 'Newborn Essentials', 'https://images.unsplash.com/photo-1607083206968-13611e3d76db?w=400&h=400&fit=crop', 1),
        ('prod_017', 'Baby Grooming Kit', 'Complete grooming essentials: nail clippers, brush, comb, and thermometer.', 26.50, 'Newborn Essentials', 'https://images.unsplash.com/photo-1581579438747-9a4c0652d30a?w=400&h=400&fit=crop', 1),
        ('prod_018', 'Breathable Crib Bumper', 'Safe mesh crib bumper. Prevents bumps while allowing airflow.', 44.99, 'Newborn Essentials', 'https://images.unsplash.com/photo-1612900047005-bd5e97ab50b5?w=400&h=400&fit=crop', 1),
        ('prod_019', 'Baby Changing Pad Cover', 'Waterproof, machine-washable covers. Set of 3 in different patterns.', 23.50, 'Newborn Essentials', 'https://images.unsplash.com/photo-1587654780291-39c9404d746b?w=400&h=400&fit=crop', 1),
        ('prod_020', 'Newborn Sleep Essentials Kit', 'Everything for peaceful sleep: white noise machine, nightlight, and monitor.', 89.99, 'Newborn Essentials', 'https://images.unsplash.com/photo-1611074409092-3b2d21e2f86e?w=400&h=400&fit=crop', 1),
        
        # Wooden Toys (20 products)
        ('prod_021', 'Handcrafted Wooden Rattle', 'Natural wood baby rattle, safe and eco-friendly. Great for sensory development.', 18.50, 'Wooden Toys', 'https://images.unsplash.com/photo-1587654780291-39c9404d746b?w=400&h=400&fit=crop', 1),
        ('prod_022', 'Wooden Pull-Along Duck', 'Classic wooden pull toy. Perfect for toddlers learning to walk.', 22.00, 'Wooden Toys', 'https://images.unsplash.com/photo-1578022761797-b8636ac1773c?w=400&h=400&fit=crop', 1),
        ('prod_023', 'Wooden Stacking Rings', 'Rainbow stacking toy made from sustainable wood. Teaches colors and sizes.', 26.99, 'Wooden Toys', 'https://images.unsplash.com/photo-1580870069867-74c2be28f47c?w=400&h=400&fit=crop', 1),
        ('prod_024', 'Wooden Building Blocks Set', '50-piece natural wood blocks. Endless creative possibilities.', 45.00, 'Wooden Toys', 'https://images.unsplash.com/photo-1611074409092-3b2d21e2f86e?w=400&h=400&fit=crop', 1),
        ('prod_025', 'Wooden Shape Sorter', 'Classic shape sorting toy. Develops problem-solving skills.', 29.50, 'Wooden Toys', 'https://images.unsplash.com/photo-1581579438747-9a4c0652d30a?w=400&h=400&fit=crop', 1),
        ('prod_026', 'Wooden Puzzle Set', 'Animal-themed wooden puzzles. Great for cognitive development.', 32.00, 'Wooden Toys', 'https://images.unsplash.com/photo-1580130732478-3ddc2f96f6e4?w=400&h=400&fit=crop', 1),
        ('prod_027', 'Wooden Train Set', 'Classic train with tracks and accessories. Hours of imaginative play.', 56.00, 'Wooden Toys', 'https://images.unsplash.com/photo-1599669454699-248893623440?w=400&h=400&fit=crop', 1),
        ('prod_028', 'Wooden Hammer & Pegs Toy', 'Pound-a-peg toy for hand-eye coordination. Safe and durable.', 24.50, 'Wooden Toys', 'https://images.unsplash.com/photo-1603354350317-6f7aaa5911c5?w=400&h=400&fit=crop', 1),
        ('prod_029', 'Wooden Balancing Game', 'Stacking and balancing toy. Improves fine motor skills.', 27.99, 'Wooden Toys', 'https://images.unsplash.com/photo-1596461404969-9ae70f2830c1?w=400&h=400&fit=crop', 1),
        ('prod_030', 'Wooden Memory Game', 'Classic matching game with wooden tiles. Educational and fun.', 21.00, 'Wooden Toys', 'https://images.unsplash.com/photo-1587037577931-11f85e70daac?w=400&h=400&fit=crop', 1),
        ('prod_031', 'Wooden Xylophone', 'Musical toy with colorful keys. Introduces music fundamentals.', 33.50, 'Wooden Toys', 'https://images.unsplash.com/photo-1581619424770-8a8e7f34d39f?w=400&h=400&fit=crop', 1),
        ('prod_032', 'Wooden Counting Beads', 'Abacus-style toy for learning numbers. Bright, engaging colors.', 28.00, 'Wooden Toys', 'https://images.unsplash.com/photo-1599669454699-248893623440?w=400&h=400&fit=crop', 1),
        ('prod_033', 'Wooden Tool Bench', 'Pretend play workbench with tools. Encourages imaginative play.', 52.99, 'Wooden Toys', 'https://images.unsplash.com/photo-1611074409092-3b2d21e2f86e?w=400&h=400&fit=crop', 1),
        ('prod_034', 'Wooden Farm Animals Set', 'Hand-painted wooden farm animals. Perfect for storytelling.', 36.50, 'Wooden Toys', 'https://images.unsplash.com/photo-1587654780291-39c9404d746b?w=400&h=400&fit=crop', 1),
        ('prod_035', 'Wooden Lacing Cards', 'Threading toy for fine motor skills. Includes 6 different shapes.', 19.99, 'Wooden Toys', 'https://images.unsplash.com/photo-1580870069867-74c2be28f47c?w=400&h=400&fit=crop', 1),
        ('prod_036', 'Wooden Dollhouse', 'Multi-level dollhouse with furniture. Encourages creative play.', 89.00, 'Wooden Toys', 'https://images.unsplash.com/photo-1578022761797-b8636ac1773c?w=400&h=400&fit=crop', 1),
        ('prod_037', 'Wooden Alphabet Blocks', 'Classic ABC blocks with letters and pictures. Learning made fun.', 31.50, 'Wooden Toys', 'https://images.unsplash.com/photo-1611074409092-3b2d21e2f86e?w=400&h=400&fit=crop', 1),
        ('prod_038', 'Wooden Spinning Top', 'Traditional spinning top. Simple yet mesmerizing toy.', 14.99, 'Wooden Toys', 'https://images.unsplash.com/photo-1587037577931-11f85e70daac?w=400&h=400&fit=crop', 1),
        ('prod_039', 'Wooden Nesting Dolls', 'Matryoshka-style nesting dolls. Beautiful and educational.', 38.00, 'Wooden Toys', 'https://images.unsplash.com/photo-1587654780291-39c9404d746b?w=400&h=400&fit=crop', 1),
        ('prod_040', 'Wooden Marble Run', 'Build-your-own marble run. STEM learning through play.', 64.99, 'Wooden Toys', 'https://images.unsplash.com/photo-1599669454699-248893623440?w=400&h=400&fit=crop', 1),
        
        # Mom & Baby Sets (15 products)
        ('prod_041', 'Cultural Baby Carrier Wrap', 'Traditional baby wrap with modern comfort. Celebrates cultural heritage.', 55.00, 'Mom & Baby Sets', 'https://images.unsplash.com/photo-1555252333-9f8e92e65df9?w=400&h=400&fit=crop', 1),
        ('prod_042', 'Mom & Baby Matching Set', 'Matching outfit set for mom and baby. Comfortable and stylish.', 78.00, 'Mom & Baby Sets', 'https://images.unsplash.com/photo-1566694271453-390536dd1f0d?w=400&h=400&fit=crop', 1),
        ('prod_043', 'Nursing Cover & Bib Set', 'Stylish nursing cover with matching baby bibs. Privacy meets fashion.', 38.50, 'Mom & Baby Sets', 'https://images.unsplash.com/photo-1584473457325-7ae49767c846?w=400&h=400&fit=crop', 1),
        ('prod_044', 'Mom & Baby Headband Set', 'Adorable matching headbands. Perfect for photo sessions.', 24.00, 'Mom & Baby Sets', 'https://images.unsplash.com/photo-1515488764276-beab7607c1e6?w=400&h=400&fit=crop', 1),
        ('prod_045', 'Coordinating Diaper Bag & Changing Pad', 'Stylish diaper bag with matching portable changing pad.', 89.99, 'Mom & Baby Sets', 'https://images.unsplash.com/photo-1590736969955-71cc94901144?w=400&h=400&fit=crop', 1),
        ('prod_046', 'Nursing Pillow & Cover Set', 'Ergonomic nursing pillow with washable cover. Supports mom and baby.', 44.99, 'Mom & Baby Sets', 'https://images.unsplash.com/photo-1612900047005-bd5e97ab50b5?w=400&h=400&fit=crop', 1),
        ('prod_047', 'Mom & Baby Pajama Set', 'Matching pajamas for bedtime bonding. Soft and comfortable.', 62.00, 'Mom & Baby Sets', 'https://images.unsplash.com/photo-1515488042361-ee00e0ddd4e4?w=400&h=400&fit=crop', 1),
        ('prod_048', 'Bonding Robe & Blanket Set', 'Cozy robe for mom, swaddle blanket for baby. Perfect for skin-to-skin.', 72.50, 'Mom & Baby Sets', 'https://images.unsplash.com/photo-1555252333-9f8e92e65df9?w=400&h=400&fit=crop', 1),
        ('prod_049', 'Mom & Baby Sunhat Set', 'Matching sun protection hats. UV-protective and stylish.', 32.00, 'Mom & Baby Sets', 'https://images.unsplash.com/photo-1566694271453-390536dd1f0d?w=400&h=400&fit=crop', 1),
        ('prod_050', 'Postpartum Care & Baby Essentials', 'Recovery kit for mom, essentials for baby. Complete support set.', 96.00, 'Mom & Baby Sets', 'https://images.unsplash.com/photo-1584473457325-7ae49767c846?w=400&h=400&fit=crop', 1),
        ('prod_051', 'Mom & Baby Spa Gift Set', 'Natural skincare for both. Organic lotions, oils, and soaps.', 54.99, 'Mom & Baby Sets', 'https://images.unsplash.com/photo-1515488764276-beab7607c1e6?w=400&h=400&fit=crop', 1),
        ('prod_052', 'Nursing Essentials Bundle', 'Everything for breastfeeding: pads, cream, storage bags, and more.', 48.50, 'Mom & Baby Sets', 'https://images.unsplash.com/photo-1612900047005-bd5e97ab50b5?w=400&h=400&fit=crop', 1),
        ('prod_053', 'Mom & Baby Exercise Set', 'Postpartum workout gear and baby play mat. Stay active together.', 68.00, 'Mom & Baby Sets', 'https://images.unsplash.com/photo-1566694271453-390536dd1f0d?w=400&h=400&fit=crop', 1),
        ('prod_054', 'Travel Essentials Kit', 'Organized travel set for mom and baby. Includes portable organizers.', 76.99, 'Mom & Baby Sets', 'https://images.unsplash.com/photo-1590736969955-71cc94901144?w=400&h=400&fit=crop', 1),
        ('prod_055', 'Mom & Baby Keepsake Box', 'Memory box set with journal and photo album. Cherish special moments.', 42.00, 'Mom & Baby Sets', 'https://images.unsplash.com/photo-1555252333-9f8e92e65df9?w=400&h=400&fit=crop', 1),
        
        # Educational Toys (15 products)
        ('prod_056', 'Montessori Wooden Play Set', 'Educational toy set promoting learning through play. Made from sustainable wood.', 42.00, 'Educational Toys', 'https://images.unsplash.com/photo-1587654780291-39c9404d746b?w=400&h=400&fit=crop', 1),
        ('prod_057', 'Cultural Lullaby Music Box', 'Wooden music box playing traditional lullabies from around the world.', 32.00, 'Educational Toys', 'https://images.unsplash.com/photo-1599669454699-248893623440?w=400&h=400&fit=crop', 1),
        ('prod_058', 'Alphabet Learning Blocks', 'Colorful wooden blocks with letters, numbers, and pictures.', 36.50, 'Educational Toys', 'https://images.unsplash.com/photo-1596461404969-9ae70f2830c1?w=400&h=400&fit=crop', 1),
        ('prod_059', 'Musical Instrument Set', 'Child-safe instruments including xylophone, maracas, and tambourine.', 48.00, 'Educational Toys', 'https://images.unsplash.com/photo-1603354350317-6f7aaa5911c5?w=400&h=400&fit=crop', 1),
        ('prod_060', 'Sensory Play Mat', 'Interactive mat with textures, mirrors, and crinkle sounds.', 52.99, 'Educational Toys', 'https://images.unsplash.com/photo-1596461404969-9ae70f2830c1?w=400&h=400&fit=crop', 1),
        ('prod_061', 'Counting & Sorting Toy', 'Learn numbers and colors through sorting activities. Montessori-inspired.', 29.99, 'Educational Toys', 'https://images.unsplash.com/photo-1580870069867-74c2be28f47c?w=400&h=400&fit=crop', 1),
        ('prod_062', 'Interactive Activity Cube', 'Multi-sided activity center. Develops multiple skills simultaneously.', 58.00, 'Educational Toys', 'https://images.unsplash.com/photo-1599669454699-248893623440?w=400&h=400&fit=crop', 1),
        ('prod_063', 'STEM Building Set', 'Magnetic tiles for building 3D structures. Introduces engineering concepts.', 64.50, 'Educational Toys', 'https://images.unsplash.com/photo-1611074409092-3b2d21e2f86e?w=400&h=400&fit=crop', 1),
        ('prod_064', 'Language Learning Cards', 'Flash cards in multiple languages. Bilingual learning made easy.', 26.00, 'Educational Toys', 'https://images.unsplash.com/photo-1587654780291-39c9404d746b?w=400&h=400&fit=crop', 1),
        ('prod_065', 'Busy Board Activity Panel', 'Montessori busy board with locks, latches, and switches. Fine motor skills.', 46.99, 'Educational Toys', 'https://images.unsplash.com/photo-1580870069867-74c2be28f47c?w=400&h=400&fit=crop', 1),
        ('prod_066', 'Color & Shape Learning Set', 'Teach shapes, colors, and patterns. Hands-on learning tool.', 31.50, 'Educational Toys', 'https://images.unsplash.com/photo-1596461404969-9ae70f2830c1?w=400&h=400&fit=crop', 1),
        ('prod_067', 'Storytelling Puppet Theater', 'Puppet theater with characters. Encourages language and creativity.', 54.00, 'Educational Toys', 'https://images.unsplash.com/photo-1599669454699-248893623440?w=400&h=400&fit=crop', 1),
        ('prod_068', 'Science Exploration Kit', 'Age-appropriate science experiments. Spark curiosity early.', 42.50, 'Educational Toys', 'https://images.unsplash.com/photo-1603354350317-6f7aaa5911c5?w=400&h=400&fit=crop', 1),
        ('prod_069', 'Geography Puzzle Globe', 'Interactive globe puzzle. Learn about world geography.', 38.99, 'Educational Toys', 'https://images.unsplash.com/photo-1587654780291-39c9404d746b?w=400&h=400&fit=crop', 1),
        ('prod_070', 'Art & Creativity Station', 'Complete art supplies for little artists. Non-toxic and washable.', 49.00, 'Educational Toys', 'https://images.unsplash.com/photo-1580870069867-74c2be28f47c?w=400&h=400&fit=crop', 1),
        
        # Feeding & Nursing (15 products)
        ('prod_071', 'Organic Baby Food Starter Kit', 'Complete set for making healthy homemade baby food. BPA-free containers included.', 38.99, 'Feeding & Nursing', 'https://images.unsplash.com/photo-1609220136736-443140cffec6?w=400&h=400&fit=crop', 1),
        ('prod_072', 'Silicone Baby Feeding Set', 'Complete feeding set: plate, bowl, spoon. BPA-free, dishwasher safe.', 29.99, 'Feeding & Nursing', 'https://images.unsplash.com/photo-1618220179428-22790b461013?w=400&h=400&fit=crop', 1),
        ('prod_073', 'Bamboo Baby Utensils', 'Eco-friendly bamboo spoons and forks. Safe for babies and the environment.', 16.50, 'Feeding & Nursing', 'https://images.unsplash.com/photo-1607920592124-98a69eae8ecf?w=400&h=400&fit=crop', 1),
        ('prod_074', 'Anti-Colic Baby Bottles (4-Pack)', 'Reduces gas and fussiness. Easy to clean and assemble.', 42.00, 'Feeding & Nursing', 'https://images.unsplash.com/photo-1599549008343-e53ef8cf5952?w=400&h=400&fit=crop', 1),
        ('prod_075', 'Breast Pump & Storage Kit', 'Electric breast pump with storage bottles and bags. Efficient and comfortable.', 156.00, 'Feeding & Nursing', 'https://images.unsplash.com/photo-1609220136736-443140cffec6?w=400&h=400&fit=crop', 1),
        ('prod_076', 'High Chair Feeding Essentials', 'Placemat, utensils, and sippy cup set. Makes mealtime easier.', 34.50, 'Feeding & Nursing', 'https://images.unsplash.com/photo-1618220179428-22790b461013?w=400&h=400&fit=crop', 1),
        ('prod_077', 'Bottle Warmer & Sterilizer', '2-in-1 device for warming and sterilizing. Quick and convenient.', 68.99, 'Feeding & Nursing', 'https://images.unsplash.com/photo-1599549008343-e53ef8cf5952?w=400&h=400&fit=crop', 1),
        ('prod_078', 'Snack Containers Set', 'Leak-proof containers for on-the-go snacks. Set of 4 different sizes.', 22.00, 'Feeding & Nursing', 'https://images.unsplash.com/photo-1607920592124-98a69eae8ecf?w=400&h=400&fit=crop', 1),
        ('prod_079', 'Sippy Cup Variety Pack', 'Different spout styles for transitioning. Spill-proof and easy to hold.', 28.50, 'Feeding & Nursing', 'https://images.unsplash.com/photo-1609220136736-443140cffec6?w=400&h=400&fit=crop', 1),
        ('prod_080', 'Baby Food Freezer Tray', 'Make and freeze homemade baby food portions. BPA-free silicone.', 19.99, 'Feeding & Nursing', 'https://images.unsplash.com/photo-1618220179428-22790b461013?w=400&h=400&fit=crop', 1),
        ('prod_081', 'Nursing Bra & Pad Set', 'Comfortable nursing bras with washable pads. Essential for breastfeeding moms.', 46.00, 'Feeding & Nursing', 'https://images.unsplash.com/photo-1609220136736-443140cffec6?w=400&h=400&fit=crop', 1),
        ('prod_082', 'Divided Baby Plates (3-Pack)', 'Suction plates with compartments. Reduce mealtime mess.', 24.99, 'Feeding & Nursing', 'https://images.unsplash.com/photo-1607920592124-98a69eae8ecf?w=400&h=400&fit=crop', 1),
        ('prod_083', 'Formula Dispenser & Bottle Set', 'Portable formula dispenser with bottles. Perfect for travel.', 32.50, 'Feeding & Nursing', 'https://images.unsplash.com/photo-1599549008343-e53ef8cf5952?w=400&h=400&fit=crop', 1),
        ('prod_084', 'Toddler Utensil Training Set', 'Ergonomic utensils for self-feeding. Promotes independence.', 18.00, 'Feeding & Nursing', 'https://images.unsplash.com/photo-1618220179428-22790b461013?w=400&h=400&fit=crop', 1),
        ('prod_085', 'Baby Food Recipe Book & Tools', 'Recipe book with food prep tools. Make nutritious meals at home.', 36.99, 'Feeding & Nursing', 'https://images.unsplash.com/photo-1609220136736-443140cffec6?w=400&h=400&fit=crop', 1),
        
        # Cultural Baby Wear (15 products)
        ('prod_086', 'Eid Special Baby Outfit', 'Beautiful handcrafted outfit for Eid celebrations. Includes matching accessories.', 48.00, 'Cultural Baby Wear', 'https://images.unsplash.com/photo-1522771930-78848d9293e8?w=400&h=400&fit=crop', 1),
        ('prod_087', 'Traditional Dashiki Baby Set', 'Vibrant African print baby outfit with matching hat.', 42.50, 'Cultural Baby Wear', 'https://images.unsplash.com/photo-1519689373023-dd07c7988603?w=400&h=400&fit=crop', 1),
        ('prod_088', 'Kimono Style Baby Romper', 'Japanese-inspired wrap romper in soft organic cotton.', 38.00, 'Cultural Baby Wear', 'https://images.unsplash.com/photo-1515488042361-ee00e0ddd4e4?w=400&h=400&fit=crop', 1),
        ('prod_089', 'Henna Pattern Baby Onesie', 'Beautiful mehndi-inspired designs on premium cotton.', 26.99, 'Cultural Baby Wear', 'https://images.unsplash.com/photo-1595452767754-59dfdcf98960?w=400&h=400&fit=crop', 1),
        ('prod_090', 'Cultural Print Baby Shoes Set', 'Soft sole shoes in traditional patterns. Set of 3 pairs.', 35.00, 'Cultural Baby Wear', 'https://images.unsplash.com/photo-1542060748-10c28b62716f?w=400&h=400&fit=crop', 1),
        ('prod_091', 'Kente Cloth Baby Wrap', 'Traditional African Kente pattern baby carrier wrap.', 52.00, 'Cultural Baby Wear', 'https://images.unsplash.com/photo-1522771930-78848d9293e8?w=400&h=400&fit=crop', 1),
        ('prod_092', 'Diwali Baby Kurta Set', 'Traditional Indian kurta for festive celebrations. Includes pajama.', 44.50, 'Cultural Baby Wear', 'https://images.unsplash.com/photo-1519689373023-dd07c7988603?w=400&h=400&fit=crop', 1),
        ('prod_093', 'Chinese New Year Baby Outfit', 'Lucky red outfit with gold embroidery. Perfect for celebrations.', 46.00, 'Cultural Baby Wear', 'https://images.unsplash.com/photo-1515488042361-ee00e0ddd4e4?w=400&h=400&fit=crop', 1),
        ('prod_094', 'Native American Inspired Set', 'Respectfully designed outfit with traditional patterns.', 40.99, 'Cultural Baby Wear', 'https://images.unsplash.com/photo-1595452767754-59dfdcf98960?w=400&h=400&fit=crop', 1),
        ('prod_095', 'Caribbean Print Romper', 'Colorful island-inspired romper. Lightweight and comfortable.', 32.50, 'Cultural Baby Wear', 'https://images.unsplash.com/photo-1522771930-78848d9293e8?w=400&h=400&fit=crop', 1),
        ('prod_096', 'Traditional Maori Baby Cloak', 'Handwoven baby cloak with cultural significance. Heirloom quality.', 124.00, 'Cultural Baby Wear', 'https://images.unsplash.com/photo-1542060748-10c28b62716f?w=400&h=400&fit=crop', 1),
        ('prod_097', 'Mexican Fiesta Baby Dress', 'Colorful embroidered dress for special occasions.', 36.00, 'Cultural Baby Wear', 'https://images.unsplash.com/photo-1515488042361-ee00e0ddd4e4?w=400&h=400&fit=crop', 1),
        ('prod_098', 'Scottish Tartan Baby Outfit', 'Traditional tartan pattern outfit. Includes bonnet.', 48.50, 'Cultural Baby Wear', 'https://images.unsplash.com/photo-1519689373023-dd07c7988603?w=400&h=400&fit=crop', 1),
        ('prod_099', 'Bollywood Style Baby Lehenga', 'Miniature lehenga choli for baby girls. Festive and adorable.', 54.99, 'Cultural Baby Wear', 'https://images.unsplash.com/photo-1522771930-78848d9293e8?w=400&h=400&fit=crop', 1),
        ('prod_100', 'Global Baby Outfit Collection', 'Set of 5 onesies representing different cultures. Celebrate diversity.', 62.00, 'Cultural Baby Wear', 'https://images.unsplash.com/photo-1515488042361-ee00e0ddd4e4?w=400&h=400&fit=crop', 1),
    ]
    
    c.executemany('INSERT INTO products (id, name, description, price, category, image, in_stock) VALUES (?, ?, ?, ?, ?, ?, ?)', products)
    conn.commit()
    print(f"✅ Seeded {len(products)} products into database")
    
    conn.close()
    print("✅ Database initialized successfully!")

if __name__ == '__main__':
    init_database()
