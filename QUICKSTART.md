# Quick Start Guide - Image Transcriber

## For Windows Users

### Step 1: Extract the ZIP
Extract the `ImageTranscriber.zip` file to your desired location.

### Step 2: Open Command Prompt
Navigate to the ImageTranscriber folder:
```
cd path\to\ImageTranscriber
```

### Step 3: Create Virtual Environment
```
python -m venv venv
venv\Scripts\activate
```

### Step 4: Install Dependencies
```
pip install -r requirements.txt
```

### Step 5: Setup Environment
```
copy .env.example .env
```

Edit `.env` file with Notepad:
```
OPENAI_API_KEY=your-api-key-here
DEBUG=True
```

### Step 6: Setup Database
```
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic --noinput
```

### Step 7: Run Server
```
python manage.py runserver
```

### Step 8: Access Application
- Open browser: `http://localhost:8000`
- Admin panel: `http://localhost:8000/admin`

---

## For macOS Users

### Step 1: Extract the ZIP
Extract the `ImageTranscriber.zip` file.

### Step 2: Open Terminal
Navigate to the folder:
```bash
cd path/to/ImageTranscriber
```

### Step 3: Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 4: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 5: Setup Environment
```bash
cp .env.example .env
nano .env  # Edit and add OPENAI_API_KEY
```

### Step 6: Setup Database
```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic --noinput
```

### Step 7: Run Server
```bash
python manage.py runserver
```

### Step 8: Access Application
- Open browser: `http://localhost:8000`
- Admin panel: `http://localhost:8000/admin`

---

## For Linux Users

### Step 1: Extract the ZIP
```bash
unzip ImageTranscriber.zip
cd ImageTranscriber
```

### Step 2: Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Setup Environment
```bash
cp .env.example .env
nano .env  # Add OPENAI_API_KEY=your-key
```

### Step 5: Setup Database
```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic --noinput
```

### Step 6: Run Server
```bash
python manage.py runserver
```

### Step 7: Access Application
- Open browser: `http://localhost:8000`
- Admin panel: `http://localhost:8000/admin`

---

## Troubleshooting

### "Python not found"
Make sure Python 3.8+ is installed. Download from: https://www.python.org

### "pip is not recognized"
Use `python -m pip` instead of `pip`

### "Virtual environment not activating"
Try:
```
# Windows
python -m venv venv
venv\Scripts\python -m pip install -r requirements.txt

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### "OpenAI API key error"
1. Get your API key from: https://platform.openai.com/api-keys
2. Edit `.env` file
3. Add: `OPENAI_API_KEY=sk-your-actual-key-here`
4. Restart the server

### "Port 8000 already in use"
Use a different port:
```
python manage.py runserver 8001
```

---

## Using OpenAI API

### Getting Your API Key
1. Go to https://platform.openai.com/api-keys
2. Click "Create new secret key"
3. Copy the key (you won't see it again)
4. Paste it in the `.env` file

### API Costs
- Vision API costs based on image size and number of requests
- Monitor usage: https://platform.openai.com/account/usage

---

## Project Features

✅ **Upload Images** - PNG, JPG, GIF, WebP (max 20MB)
✅ **AI Transcription** - Uses OpenAI Vision API
✅ **Text Formatting** - ALL CAPS, Title Case, Sentence case
✅ **Mobile Responsive** - Works on phone, tablet, desktop
✅ **History** - Keep track of all transcriptions
✅ **Export** - Copy or download transcribed text

---

## Next Steps

After getting comfortable with local development:

1. Read `README.md` for full documentation
2. Read `DEPLOYMENT.md` to deploy on DigitalOcean
3. Customize the application as needed
4. Deploy to your server

---

## Getting Help

- **Django Docs**: https://docs.djangoproject.com
- **OpenAI Docs**: https://platform.openai.com/docs
- **Bootstrap Docs**: https://getbootstrap.com/docs

---

Happy transcribing! 🎉
