# Image Transcriber for Dr. Apekshya Bhattarai

A professional web application that transcribes text from images using OpenAI's Vision API and formats it with proper capitalization. Built with Django and optimized for mobile devices.

## Features

✨ **Core Features:**
- 📸 **Image Upload & Processing** - Upload images in PNG, JPG, GIF, or WebP format
- 🤖 **AI-Powered Transcription** - Uses OpenAI's Vision API to extract text from images
- 📝 **Text Formatting** - Multiple capitalization options:
  - ALL CAPS
  - Title Case
  - Sentence case
- 📱 **Mobile-Responsive Design** - Works seamlessly on desktop, tablet, and mobile devices
- 💾 **History Management** - Keep track of all your transcriptions
- 📥 **Export Options** - Copy to clipboard or download as text file
- 🎨 **Modern UI** - Beautiful gradient design with smooth animations
- ⚡ **Fast Processing** - Optimized performance with caching

## System Requirements

- Python 3.8 or higher
- Django 4.2+
- OpenAI API key
- 2GB RAM (minimum for DigitalOcean droplet)

## Local Development Setup

### 1. Clone or Extract Project
```bash
cd ImageTranscriber
```

### 2. Create Virtual Environment
```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
```bash
cp .env.example .env
```

Edit `.env` and add your OpenAI API key:
```
OPENAI_API_KEY=sk-your-api-key-here
DEBUG=True
SECRET_KEY=your-secret-key
```

### 5. Run Migrations
```bash
python manage.py migrate
```

### 6. Create Superuser (Admin)
```bash
python manage.py createsuperuser
```

### 7. Collect Static Files
```bash
python manage.py collectstatic --noinput
```

### 8. Run Development Server
```bash
python manage.py runserver
```

Visit `http://localhost:8000` in your browser.

## Production Deployment

For detailed deployment instructions on DigitalOcean, see [DEPLOYMENT.md](DEPLOYMENT.md)

Quick summary:
1. Set up Ubuntu 22.04 droplet on DigitalOcean
2. Follow the step-by-step deployment guide
3. Configure domain and SSL certificate
4. Start using the application

## Project Structure

```
ImageTranscriber/
├── config/                    # Django project settings
│   ├── settings.py           # Main settings file
│   ├── urls.py               # URL configuration
│   └── wsgi.py               # WSGI configuration
├── transcriber/              # Main app
│   ├── models.py             # Database models
│   ├── views.py              # View functions
│   ├── forms.py              # Django forms
│   ├── services.py           # OpenAI integration logic
│   ├── urls.py               # App URLs
│   ├── admin.py              # Admin configuration
│   ├── templates/            # HTML templates
│   │   └── transcriber/
│   │       ├── base.html     # Base template
│   │       ├── index.html    # Home page
│   │       ├── detail.html   # Transcription detail
│   │       └── history.html  # History page
│   └── static/               # CSS, JavaScript, images
│       ├── css/
│       └── js/
├── media/                    # User uploaded images
├── manage.py                 # Django management script
├── requirements.txt          # Python dependencies
├── .env.example             # Environment variables template
├── nginx.conf               # Nginx configuration
├── image_transcriber.service # Systemd service file
├── DEPLOYMENT.md            # Deployment guide
└── README.md                # This file
```

## Usage Guide

### Basic Workflow
1. **Upload Image**: Click the upload area or drag-and-drop an image
2. **Wait for Processing**: The app will use OpenAI Vision API to transcribe text
3. **View Results**: See both original and formatted text
4. **Format Text**: Choose different capitalization styles
5. **Export**: Copy to clipboard or download as text file

### Admin Panel
Access the admin panel at `/admin`:
- Manage transcriptions
- View processing history
- Monitor API usage
- Delete old records

## API Endpoints

### Public Endpoints
- `GET /` - Home page
- `POST /upload/` - Upload and process image
- `GET /detail/<id>/` - View transcription details
- `POST /reformat/<id>/` - Reformat text with different capitalization
- `GET /history/` - View all transcriptions
- `DELETE /delete/<id>/` - Delete transcription

### API Endpoints
- `GET /api/transcription/<id>/` - Get transcription data as JSON

## Configuration

### Environment Variables (.env)
```
DEBUG=True/False              # Django debug mode
SECRET_KEY=your-key          # Django secret key
ALLOWED_HOSTS=localhost      # Allowed hostnames
OPENAI_API_KEY=sk-...        # OpenAI API key
DB_ENGINE=...                # Database engine
DB_NAME=...                  # Database name
```

### Django Settings
Modify `config/settings.py` to:
- Change database backend
- Add custom middleware
- Configure logging
- Set up caching

## Supported Image Formats

| Format | Extension | Supported |
|--------|-----------|-----------|
| JPEG   | .jpg, .jpeg | ✅ |
| PNG    | .png      | ✅ |
| GIF    | .gif      | ✅ |
| WebP   | .webp     | ✅ |

**Maximum file size**: 20 MB

## OpenAI API Usage

### Model Used
- **Model**: GPT-4O Mini Vision
- **Cost**: Varies based on usage
- **Rate Limits**: Subject to OpenAI's rate limiting

### Optimization Tips
1. Optimize image size before uploading
2. Use appropriate image formats
3. Monitor API usage in OpenAI dashboard

## Troubleshooting

### Common Issues

**Issue**: "ModuleNotFoundError: No module named 'openai'"
```bash
pip install -r requirements.txt
```

**Issue**: "OpenAI API key not found"
- Check `.env` file has `OPENAI_API_KEY`
- Restart the application
- Verify API key is valid

**Issue**: "Image processing timeout"
- Check server resources
- Verify Gunicorn timeout is set to 300s
- Use smaller images

**Issue**: Static files not loading in production
```bash
python manage.py collectstatic --noinput --clear
sudo systemctl restart image_transcriber
```

## Performance Optimization

### Database
- Use PostgreSQL in production instead of SQLite
- Set up database indexes on frequently searched fields
- Regular cleanup of old transcriptions

### Caching
- Implement Redis for session caching
- Cache static files on CDN
- Use HTTP caching headers

### Image Processing
- Optimize image sizes before uploading
- Use appropriate formats
- Consider image compression

## Security Features

✅ **Built-in Security**:
- CSRF protection on all forms
- SQL injection prevention
- XSS protection
- Secure password hashing
- Environment-based secrets management

⚙️ **Production Hardening**:
- SSL/TLS encryption
- Secure HTTP headers
- Rate limiting
- Input validation
- Permission-based access control

## Monitoring & Logging

### View Application Logs
```bash
sudo journalctl -u image_transcriber -f
```

### View Nginx Logs
```bash
sudo tail -f /var/log/nginx/error.log
```

### Monitor System Resources
```bash
top
df -h
ps aux | grep gunicorn
```

## Backup Strategy

### Database Backup
```bash
# SQLite
cp db.sqlite3 db.sqlite3.backup

# PostgreSQL
pg_dump transcriber_db > backup.sql
```

### Media Files Backup
```bash
tar -czf media_backup.tar.gz media/
```

## Contributing

To contribute to this project:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is proprietary and created specifically for Dr. Apekshya Bhattarai.

## Support & Contact

For issues, feature requests, or support:
- 📧 Email: support@example.com
- 🐛 Report bugs with detailed information
- 💡 Suggest improvements

## Version History

### v1.0.0 (Initial Release)
- Image upload and transcription
- Text formatting with multiple capitalization styles
- History management
- Mobile-responsive design
- DigitalOcean deployment guide

## Acknowledgments

- Built with [Django](https://www.djangoproject.com/)
- Powered by [OpenAI Vision API](https://platform.openai.com/docs/guides/vision)
- UI Framework: [Bootstrap 5](https://getbootstrap.com/)
- Icons: [Font Awesome](https://fontawesome.com/)

## Getting Help

### Common Commands

**Start development server**:
```bash
source venv/bin/activate
python manage.py runserver
```

**Create migrations**:
```bash
python manage.py makemigrations
python manage.py migrate
```

**Access Django shell**:
```bash
python manage.py shell
```

**Create new app**:
```bash
python manage.py startapp app_name
```

## Technology Stack

- **Backend**: Django 4.2
- **Frontend**: HTML5, CSS3, Bootstrap 5, JavaScript
- **AI**: OpenAI Vision API
- **Web Server**: Nginx
- **App Server**: Gunicorn
- **Database**: SQLite (dev) / PostgreSQL (production)
- **Storage**: Local filesystem / AWS S3 (optional)

---

**Created for**: Dr. Apekshya Bhattarai  
**Created by**: Your Development Team  
**Last Updated**: 2024
