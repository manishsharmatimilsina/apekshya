# Image Transcriber - Deployment Guide for DigitalOcean

## Overview
This guide will help you deploy the Image Transcriber application on a DigitalOcean droplet. The application uses Django, Gunicorn, and Nginx.

## Prerequisites
- A DigitalOcean droplet with Ubuntu 22.04 or later
- SSH access to your droplet
- A registered domain name (optional, but recommended)
- OpenAI API key

## Step 1: Initial Server Setup

### 1.1 Connect to your droplet
```bash
ssh root@your_droplet_ip
```

### 1.2 Update system packages
```bash
apt update && apt upgrade -y
```

### 1.3 Install required packages
```bash
apt install -y python3-pip python3-venv python3-dev postgresql postgresql-contrib nginx curl git build-essential
```

## Step 2: Create Django User and Project Directory

### 2.1 Create a new user for Django
```bash
useradd -m -s /bin/bash django
usermod -aG sudo django
```

### 2.2 Create project directory
```bash
mkdir -p /home/django/ImageTranscriber
chown -R django:django /home/django/ImageTranscriber
chmod -R 755 /home/django
```

### 2.3 Upload your project
Transfer your project files to the server:
```bash
scp -r ImageTranscriber/* django@your_droplet_ip:/home/django/ImageTranscriber/
```

## Step 3: Set Up Python Virtual Environment

### 3.1 Switch to django user
```bash
su - django
cd /home/django/ImageTranscriber
```

### 3.2 Create virtual environment
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3.3 Install Python dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

## Step 4: Configure Django Application

### 4.1 Set up environment variables
```bash
cp .env.example .env
nano .env
```

Edit the `.env` file with your settings:
- Set `DEBUG=False` for production
- Generate a new SECRET_KEY (use: `python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'`)
- Add your OpenAI API key
- Set `ALLOWED_HOSTS` to your domain

### 4.2 Run migrations
```bash
python manage.py migrate
```

### 4.3 Create superuser (admin account)
```bash
python manage.py createsuperuser
```

### 4.4 Collect static files
```bash
python manage.py collectstatic --noinput
```

### 4.5 Create media and log directories
```bash
mkdir -p /home/django/ImageTranscriber/media
chmod -R 755 /home/django/ImageTranscriber/media
```

## Step 5: Set Up Gunicorn

### 5.1 Test Gunicorn
```bash
gunicorn --bind 127.0.0.1:8000 config.wsgi:application
```

If this works, you'll see "Listening at: http://127.0.0.1:8000"

Press Ctrl+C to stop.

### 5.2 Create systemd service file
As root user:
```bash
sudo nano /etc/systemd/system/image_transcriber.service
```

Copy the content from `image_transcriber.service` file provided in the project.

### 5.3 Create log directory
```bash
sudo mkdir -p /var/log/image_transcriber
sudo chown -R django:www-data /var/log/image_transcriber
```

### 5.4 Enable and start the service
```bash
sudo systemctl daemon-reload
sudo systemctl enable image_transcriber
sudo systemctl start image_transcriber
sudo systemctl status image_transcriber
```

## Step 6: Configure Nginx

### 6.1 Copy Nginx configuration
```bash
sudo cp /home/django/ImageTranscriber/nginx.conf /etc/nginx/sites-available/image_transcriber
sudo ln -s /etc/nginx/sites-available/image_transcriber /etc/nginx/sites-enabled/
```

### 6.2 Update Nginx configuration
```bash
sudo nano /etc/nginx/sites-available/image_transcriber
```

Update the following:
- Replace `server_name _;` with your domain: `server_name yourdomain.com www.yourdomain.com;`
- Update paths if needed (especially the `alias` paths for static and media files)

### 6.3 Test Nginx configuration
```bash
sudo nginx -t
```

### 6.4 Restart Nginx
```bash
sudo systemctl restart nginx
```

## Step 7: Set Up SSL with Let's Encrypt (Recommended)

### 7.1 Install Certbot
```bash
sudo apt install -y certbot python3-certbot-nginx
```

### 7.2 Obtain SSL certificate
```bash
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

Follow the prompts to set up SSL.

## Step 8: Configure Firewall

### 8.1 Allow necessary ports
```bash
sudo ufw allow 22/tcp    # SSH
sudo ufw allow 80/tcp    # HTTP
sudo ufw allow 443/tcp   # HTTPS
sudo ufw enable
```

## Step 9: Database Setup (Optional - PostgreSQL)

If you want to use PostgreSQL instead of SQLite:

### 9.1 Create database and user
```bash
sudo su - postgres
createdb transcriber_db
createuser transcriber_user
psql
```

In psql:
```sql
ALTER ROLE transcriber_user SET client_encoding TO 'utf8';
ALTER ROLE transcriber_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE transcriber_user SET default_transaction_deferrable TO on;
ALTER ROLE transcriber_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE transcriber_db TO transcriber_user;
\q
```

### 9.2 Exit postgres user
```bash
exit
```

### 9.3 Update .env file
```bash
nano /home/django/ImageTranscriber/.env
```

Add:
```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=transcriber_db
DB_USER=transcriber_user
DB_PASSWORD=your-password
DB_HOST=localhost
DB_PORT=5432
```

### 9.4 Update settings.py to use environment variables
The settings.py should already have this, but verify the database configuration.

### 9.5 Run migrations
```bash
cd /home/django/ImageTranscriber
source venv/bin/activate
python manage.py migrate
```

## Step 10: Verify Deployment

1. Visit your domain in a browser: `https://yourdomain.com`
2. You should see the Image Transcriber home page
3. Test uploading an image to verify the application works
4. Access admin panel: `https://yourdomain.com/admin`

## Maintenance Commands

### View application logs
```bash
sudo journalctl -u image_transcriber -f
```

### Restart the application
```bash
sudo systemctl restart image_transcriber
```

### Check application status
```bash
sudo systemctl status image_transcriber
```

### Update application
```bash
cd /home/django/ImageTranscriber
source venv/bin/activate
git pull origin main  # if using git
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
sudo systemctl restart image_transcriber
```

## Troubleshooting

### Application not responding
```bash
sudo journalctl -u image_transcriber -n 50
```

### Nginx errors
```bash
sudo tail -f /var/log/nginx/error.log
```

### Permission issues
Ensure the `django` user owns the project directory:
```bash
sudo chown -R django:django /home/django/ImageTranscriber
```

### SSL certificate renewal
```bash
sudo certbot renew --dry-run  # Test renewal
sudo certbot renew           # Actual renewal
```

## Performance Optimization Tips

1. **Increase Gunicorn workers** based on your CPU cores:
   ```bash
   # For 2 CPU cores: 2 * 2 + 1 = 5 workers
   # For 4 CPU cores: 4 * 2 + 1 = 9 workers
   ```

2. **Enable Nginx gzip compression** in nginx.conf:
   ```
   gzip on;
   gzip_types text/plain text/css text/xml text/javascript application/x-javascript application/xml+rss;
   gzip_vary on;
   ```

3. **Use Redis for caching** (advanced):
   Install Redis and configure Django caching.

## Security Checklist

- [ ] Changed Django SECRET_KEY
- [ ] Set DEBUG=False in production
- [ ] Set up SSL/HTTPS
- [ ] Configured ALLOWED_HOSTS
- [ ] Secured OpenAI API key in environment variables
- [ ] Enabled firewall
- [ ] Set up regular backups
- [ ] Updated all packages

## Support

For issues or questions, refer to:
- Django Documentation: https://docs.djangoproject.com
- Gunicorn: https://gunicorn.org
- Nginx: https://nginx.org/en/docs/
- DigitalOcean: https://www.digitalocean.com/docs
