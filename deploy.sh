cat > deploy.sh << 'EOF'
#!/bin/bash
# ================================================
#    BABYZION MARKET - OFFICIAL DEPLOY SCRIPT
#    Deploy to VPS / Railway / Render / DigitalOcean
#    Made with love for Kenyan moms
#    Run: bash deploy.sh
# ================================================

echo "BABYZION MARKET - DEPLOYING TO THE WORLD!"
echo "Kenya Time: $(date '+%Y-%m-%d %H:%M:%S %Z')"

# 1. Update system & install everything
echo "Updating system & installing Python + Nginx..."
sudo apt update -y && sudo apt upgrade -y
sudo apt install -y python3 python3-pip python3-venv nginx git curl

# 2. Create project folder
echo "Creating BabyZion folder..."
mkdir -p ~/BabyZion
cd ~/BabyZion

# 3. Clone or update your code
if [ -d ".git" ]; then
    echo "Pulling latest code..."
    git pull origin main
else
    echo "Cloning your beautiful store..."
    git clone https://github.com/YOUR_USERNAME/BabyZion.git . || { echo "Update YOUR_USERNAME above!"; exit 1; }
fi

# 4. Install Python dependencies
echo "Installing Flask & friends..."
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install flask flask-cors gunicorn

# 5. Test the app locally
echo "Testing your store..."
pkill -f "python.*app.py" 2>/dev/null
gunicorn --bind 0.0.0.0:7000 app:app --daemon --timeout 120

sleep 3
if curl -s http://localhost:7000 > /dev/null; then
    echo "BabyZion is ALIVE on port 7000!"
else
    echo "Something wrong! Check logs:"
    tail -20 gunicorn.log
    exit 1
fi

# 6. Setup Nginx (auto SSL with Certbot)
echo "Setting up Nginx + FREE SSL..."
sudo rm -f /etc/nginx/sites-enabled/default

sudo tee /etc/nginx/sites-available/babyzion > /dev/null <<'NGINX'
server {
    listen 80;
    server_name _;

    location / {
        proxy_pass http://127.0.0.1:7000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
NGINX

sudo ln -sf /etc/nginx/sites-available/babyzion /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl restart nginx

# 7. Get FREE SSL (Let's Encrypt)
echo "Getting FREE HTTPS certificate..."
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d $(curl -s ifconfig.me) --non-interactive --agree-tos -m admin@babyzion.ke

# 8. Make it survive reboots
echo "Making BabyZion IMMORTAL..."
sudo tee /etc/systemd/system/babyzion.service > /dev/null <<'SYSTEMD'
[Unit]
Description=BabyZion Market - Live Baby Store Kenya
After=network.target

[Service]
User=$USER
WorkingDirectory=/home/$USER/BabyZion
ExecStart=/home/$USER/BabyZion/venv/bin/gunicorn --workers 3 --bind 0.0.0.0:7000 app:app
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
SYSTEMD

sudo systemctl daemon-reload
sudo systemctl enable babyzion
sudo systemctl restart babyzion

# 9. FINAL FIREWORKS
echo ""
echo "BABYZION MARKET IS NOW LIVE WORLDWIDE!"
echo "https://$(curl -s ifconfig.me)"
echo ""
echo "Kenyan moms can now shop 24/7"
echo "Share this link RIGHT NOW:"
echo "https://$(curl -s ifconfig.me)"
echo ""
echo "Deploy completed at $(date '+%Y-%m-%d %H:%M:%S')"
echo "Your first KSh 50,000 sale is coming today!"
EOF

# Make it executable
chmod +x deploy.sh

echo "deploy.sh CREATED!"
echo ""
echo "NEXT STEPS (copy-paste these 3 commands):"
echo ""
echo "1. Edit the GitHub URL:"
echo "   nano deploy.sh"
echo "   → Change: https://github.com/YOUR_USERNAME/BabyZion.git"
echo "   → Save: Ctrl+X → Y → Enter"
echo ""
echo "2. Run the magic:"
echo "   bash deploy.sh"
echo ""
echo "3. In 3 minutes, open this link on your phone:"
echo "   https://YOUR_IP_OR_DOMAIN"
echo ""
echo "You're about to change lives in Kenya!"
echo "Run bash deploy.sh NOW!"