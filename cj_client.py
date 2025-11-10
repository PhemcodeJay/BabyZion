import requests
import os
from datetime import datetime, timedelta
import json

class CJDropshippingClient:
    def __init__(self):
        self.base_url = "https://developers.cjdropshipping.com/api2.0/v1"
        self.email = os.environ.get('CJ_EMAIL')
        self.api_key = os.environ.get('CJ_API_KEY')
        self.access_token = None
        self.refresh_token = None
        self.token_expiry = None
        
    def authenticate(self):
        if not self.email or not self.api_key:
            print("CJ credentials not set, skipping authentication")
            return False
            
        url = f"{self.base_url}/authentication/getAccessToken"
        payload = {
            "email": self.email,
            "apiKey": self.api_key
        }
        
        try:
            response = requests.post(url, json=payload, timeout=30)
            data = response.json()
            
            if data.get('result'):
                self.access_token = data['data']['accessToken']
                self.refresh_token = data['data']['refreshToken']
                self.token_expiry = datetime.now() + timedelta(days=14)
                print("CJ Authentication successful!")
                return True
            else:
                print(f"CJ Auth failed: {data.get('message')}")
                return False
        except Exception as e:
            print(f"CJ Auth error: {e}")
            return False
    
    def refresh_access_token(self):
        if not self.refresh_token:
            return self.authenticate()
            
        url = f"{self.base_url}/authentication/refreshAccessToken"
        payload = {"refreshToken": self.refresh_token}
        
        try:
            response = requests.post(url, json=payload, timeout=30)
            data = response.json()
            
            if data.get('result'):
                self.access_token = data['data']['accessToken']
                self.refresh_token = data['data']['refreshToken']
                self.token_expiry = datetime.now() + timedelta(days=14)
                return True
            else:
                return self.authenticate()
        except Exception as e:
            print(f"Token refresh error: {e}")
            return self.authenticate()
    
    def ensure_auth(self):
        if not self.access_token or (self.token_expiry and datetime.now() >= self.token_expiry):
            return self.authenticate()
        return True
    
    def search_products(self, keyword="baby", category_id=None, page=1, page_size=20):
        if not self.ensure_auth():
            return []
            
        url = f"{self.base_url}/product/list"
        headers = {
            "CJ-Access-Token": self.access_token,
            "Content-Type": "application/json"
        }
        
        payload = {
            "productNameEn": keyword,
            "pageNum": page,
            "pageSize": page_size
        }
        
        if category_id:
            payload["categoryId"] = category_id
        
        try:
            response = requests.post(url, json=payload, headers=headers, timeout=30)
            data = response.json()
            
            if data.get('result') and data.get('data'):
                return self.normalize_products(data['data'].get('list', []))
            else:
                print(f"CJ Product search failed: {data.get('message')}")
                return []
        except Exception as e:
            print(f"CJ Product search error: {e}")
            return []
    
    def normalize_products(self, cj_products):
        normalized = []
        for p in cj_products:
            try:
                normalized.append({
                    'id': f"CJ_{p.get('pid', '')}",
                    'name': p.get('productNameEn', 'Baby Product'),
                    'description': p.get('description', '')[:200],
                    'price': float(p.get('sellPrice', 0)),
                    'category': self.categorize_product(p.get('productNameEn', '')),
                    'image': p.get('productImage', ''),
                    'in_stock': 1 if p.get('sellPrice', 0) > 0 else 0
                })
            except Exception as e:
                print(f"Error normalizing product: {e}")
                continue
        return normalized
    
    def categorize_product(self, name):
        name_lower = name.lower()
        
        if any(word in name_lower for word in ['newborn', 'infant', 'swaddle', 'blanket']):
            return 'Newborn Essentials'
        elif any(word in name_lower for word in ['toy', 'rattle', 'wooden', 'play']):
            return 'Wooden Toys'
        elif any(word in name_lower for word in ['cultural', 'traditional', 'ethnic', 'ankara', 'dirac']):
            return 'Cultural Baby Wear'
        elif any(word in name_lower for word in ['mom', 'mother', 'mommy', 'matching']):
            return 'Mom & Baby Sets'
        elif any(word in name_lower for word in ['feed', 'bottle', 'nursing', 'sippy']):
            return 'Feeding & Nursing'
        elif any(word in name_lower for word in ['learn', 'educational', 'montessori']):
            return 'Educational Toys'
        else:
            return 'Baby Essentials'
    
    def get_product_detail(self, product_id):
        if not self.ensure_auth():
            return None
            
        url = f"{self.base_url}/product/query"
        headers = {
            "CJ-Access-Token": self.access_token,
            "Content-Type": "application/json"
        }
        
        payload = {"pid": product_id}
        
        try:
            response = requests.post(url, json=payload, headers=headers, timeout=30)
            data = response.json()
            
            if data.get('result') and data.get('data'):
                products = self.normalize_products([data['data']])
                return products[0] if products else None
            return None
        except Exception as e:
            print(f"CJ Product detail error: {e}")
            return None
