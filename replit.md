
# BABYZION MARKET

## Overview
BABYZION MARKET is a full-featured baby products e-commerce marketplace with shopping cart, payment processing, and seller upload capabilities. Built with Flask backend and modern responsive frontend.

## Project Type
Full-stack web application with Flask backend and vanilla JavaScript frontend

## Tech Stack
- **Backend**: Python 3.11, Flask, SQLite
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Payment**: PayPal Integration (Sandbox/Production)
- **Database**: SQLite with ORM
- **Deployment**: Replit Autoscale

## Project Structure
```
├── app.py                 # Flask application with API endpoints
├── database.py            # Database initialization and seeding
├── cart.js               # Shopping cart management system
├── products-data.js      # Product loading and filtering
├── index.html            # Homepage
├── about.html            # About/Our Story page
├── collections.html      # Product collections page
├── products.html         # All products listing with filters
├── upload.html           # Seller upload form
├── cart.html             # Shopping cart page
├── shipping.html         # Shipping information form
├── payment.html          # Payment processing page
├── order-complete.html   # Order confirmation
├── thank-you.html        # Thank you page
├── styles.css            # Main stylesheet
└── babyzion.db           # SQLite database
```

## Features

### Shopping Features
- **Product Catalog**: Browse 15+ pre-seeded baby products across 6 categories
- **Smart Filtering**: Filter products by category (Newborn, Toys, Cultural Wear, etc.)
- **Shopping Cart**: Persistent cart using localStorage with add/remove/update quantity
- **Live Cart Count**: Real-time cart item counter across all pages
- **Order Processing**: Complete checkout flow with shipping and payment

### Backend Features
- **RESTful API**: JSON endpoints for products, orders, and uploads
- **Database**: Auto-initializing SQLite with product seeding
- **PayPal Integration**: Sandbox and production payment processing
- **Order Management**: Order creation and tracking system
- **Seller Uploads**: Form submission for new product listings

### UI/UX Features
- **Responsive Design**: Mobile-first responsive layout
- **Gradient Backgrounds**: Modern pink/purple gradient theme
- **Smooth Animations**: Hover effects, transitions, and notifications
- **Image Previews**: Product images with fallback support
- **Toast Notifications**: User feedback for cart actions
- **Loading States**: Spinner animations during data fetching

## Setup Instructions

### 1. Environment Variables (Required for Payment Processing)
Set up your PayPal credentials using Replit Secrets:
1. Click on "Secrets" in the left sidebar (or Tools > Secrets)
2. Add the following secrets:
   - `PAYPAL_CLIENT_ID`: Your PayPal Client ID
   - `PAYPAL_CLIENT_SECRET`: Your PayPal Secret Key

For testing, you can use sandbox credentials from [PayPal Developer Dashboard](https://developer.paypal.com/)

### 2. Running the Application

**Development Mode:**
Click the **Run** button at the top of the workspace. This starts the Flask development server on port 5000.

The application will:
- Auto-initialize the SQLite database
- Seed 15 sample products across 6 categories
- Start serving on http://0.0.0.0:5000

**Accessing the App:**
- Click the webview that opens automatically
- Or visit the URL shown in the console output

### 3. Database
The SQLite database (`babyzion.db`) is automatically created on first run with:
- **Products table**: Pre-loaded with 15 baby products
- **Orders table**: Tracks customer orders and shipping info
- **Uploads table**: Stores seller product submissions

No manual database setup required!

### 4. Testing the Application

**Browse Products:**
1. Visit the homepage (index.html)
2. Navigate to "Shop All" to see all products
3. Use category filters to browse specific product types

**Shopping Cart:**
1. Click "Add to Cart" on any product
2. Notice the cart count update in the navigation
3. Visit cart.html to view/edit your cart
4. Update quantities or remove items

**Checkout Flow:**
1. Click "Proceed to Checkout" from cart
2. Fill out shipping information
3. Process payment (uses PayPal sandbox in development)
4. View order confirmation

**Seller Upload:**
1. Navigate to "Sell With Us"
2. Fill out the product upload form
3. Submit to database (appears in uploads table)

## API Endpoints

### Products
- `GET /api/products` - Get all products
- `GET /api/products?category=<name>` - Filter by category
- `GET /api/products/<id>` - Get specific product
- `GET /api/categories` - Get all categories

### Orders
- `POST /api/orders` - Create new order
- `GET /api/orders/<id>` - Get order details

### Uploads
- `POST /api/uploads` - Submit new product listing

### Payment
- `POST /api/paypal/create-order` - Create PayPal order
- `POST /api/paypal/capture-order/<id>` - Capture payment

## Deployment on Replit

### Autoscale Deployment (Recommended)

1. **Open Deployments Tab:**
   - Click "Deploy" button at top right
   - Or open Tools > Deployments

2. **Select Autoscale:**
   - Choose "Autoscale" deployment type
   - Click "Set up your deployment"

3. **Configuration:**
   - **Machine Power**: 1 vCPU, 2 GiB RAM (default)
   - **Max Instances**: 3 (scales automatically)
   - **Primary Domain**: Choose your domain name
   - **Build Command**: Leave blank (no build step needed)
   - **Run Command**: `python3 app.py`

4. **Set Secrets for Production:**
   - Add production PayPal credentials in Secrets
   - Update `PAYPAL_BASE_URL` in app.py if needed

5. **Deploy:**
   - Click "Deploy" button
   - Wait 2-3 minutes for deployment
   - Your app will be live!

### Deployment Features
- **Auto-scaling**: Scales 0-3 instances based on traffic
- **Cost-effective**: Only pay for actual usage
- **Zero downtime**: Rolling updates
- **HTTPS**: Automatic SSL certificates

## Troubleshooting

**Products not loading:**
- Check console for API errors
- Ensure database initialized (check for babyzion.db file)
- Verify Flask server is running

**Cart not persisting:**
- Check browser localStorage is enabled
- Clear cache and reload
- Ensure cart.js is loaded

**Payment failing:**
- Verify PayPal secrets are set correctly
- Check you're using sandbox credentials for testing
- Review Flask console for API errors

**Database issues:**
- Delete babyzion.db and restart (will reseed)
- Check database.py for errors
- Ensure SQLite permissions

## Development Notes

**Port Configuration:**
- Development: Port 5000 (0.0.0.0)
- Production: Auto-configured by Replit

**Caching:**
- Development server disables caching for instant updates
- Production uses standard caching

**Database:**
- SQLite is auto-created and seeded
- No migrations needed for initial setup
- Upgrade to PostgreSQL for production at scale

## Recent Updates

**November 10, 2025** - Replit Environment Setup
- ✅ Configured Flask app for Replit (port 5000 with environment variable support)
- ✅ Installed all Python dependencies (Flask, Flask-CORS, requests, gunicorn)
- ✅ Added cache-control headers for development
- ✅ Created .gitignore for Python project
- ✅ Configured workflow for automatic server startup
- ✅ Set up Autoscale deployment with gunicorn production server
- ✅ Verified application runs successfully on Replit

**November 08, 2025** - Major Feature Upgrade
- ✅ Complete shopping cart system with localStorage
- ✅ Live cart count across all pages
- ✅ Product filtering by category
- ✅ Enhanced UI with animations and transitions
- ✅ Toast notifications for user actions
- ✅ Complete checkout flow (cart → shipping → payment)
- ✅ PayPal payment integration
- ✅ Image preview on upload form
- ✅ Responsive design improvements
- ✅ Error handling and loading states
- ✅ Complete API integration
- ✅ Modern gradient design system
- ✅ Deployment configuration for Autoscale

## Support
For issues or questions about deployment, refer to [Replit Deployment Docs](https://docs.replit.com/hosting/deployments/about-deployments)
