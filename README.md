# Arrowhead MTA 26

A mobile-first web application for managing Arrowhead Maintenance Availability 2026 work item documentation.

## 🚀 Quick Start

### 1. Setup
```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the app
python run.py
```

### 2. Access the App
- Open browser: `http://localhost:5001`
- **Crew Login:** Password: `crew2026`
- **Admin Login:** Username: `admin`, Password: `admin2026`

> **Note:** Port changed to 5001 due to macOS AirTunes using port 5000

## 📋 What's Included

### Core Files
- `SHIP_MAINTENANCE_APP_BUILD_GUIDE.md` - Complete build instructions
- `requirements.txt` - Python dependencies
- `run.py` - Application entry point
- `config.py` - Configuration settings

### Templates
- `admin_login.html` - Admin authentication
- `admin_view_item.html` - View work item details
- Additional templates in `/app/templates/` (see build guide)

## 📁 Project Structure

```
ship-maintenance-tracker/
├── app/
│   ├── __init__.py
│   ├── models.py
│   ├── auth.py
│   ├── crew.py
│   ├── admin.py
│   ├── docx_generator.py
│   ├── utils.py
│   ├── static/
│   │   ├── css/style.css
│   │   └── js/main.js
│   └── templates/
│       ├── base.html
│       ├── login.html
│       ├── crew_form.html
│       ├── crew_success.html
│       ├── admin_login.html
│       ├── admin_dashboard.html
│       └── admin_view_item.html
├── uploads/
├── generated_docs/
├── config.py
├── requirements.txt
├── run.py
└── README.md
```

## 🔨 Build Instructions

For complete step-by-step build instructions, see:
**`SHIP_MAINTENANCE_APP_BUILD_GUIDE.md`**

This guide includes:
- Detailed implementation phases
- Complete code for all files
- Deployment instructions
- Troubleshooting tips
- Testing checklist

## 🌐 Deployment

### Railway
```bash
railway login
railway init
railway up
```

### Render
Connect your GitHub repo and deploy directly from Render dashboard.

## 📸 Features

- ✅ Mobile-optimized submission form
- ✅ Photo upload with auto-resize (4" width)
- ✅ Generates .docx files matching template
- ✅ Admin dashboard with status tracking
- ✅ Batch download as .zip
- ✅ Works on iPhone and Android

## 🔐 Security Notes

**IMPORTANT:** Change these defaults in production:
- `SECRET_KEY` in config.py
- `CREW_PASSWORD` in config.py
- `ADMIN_PASSWORD` in config.py

## 📝 Customization

### Update Crew Members
Edit `config.py`:
```python
CREW_MEMBERS = [
    'Your',
    'Crew',
    'Names',
    'Here'
]
```

### Adjust Photo Settings
Edit `config.py`:
```python
PHOTO_MAX_WIDTH = 576  # 4 inches at 144 DPI
PHOTO_MIN_COUNT = 2
PHOTO_MAX_COUNT = 6
```

## 🐛 Troubleshooting

### Common Issues

1. **ModuleNotFoundError**: Run `pip install -r requirements.txt`
2. **Database errors**: Delete `maintenance.db` and restart
3. **Port in use**: Change port in `run.py`
4. **Photos not uploading**: Check folder permissions

## 📚 Documentation

- **Build Guide**: `SHIP_MAINTENANCE_APP_BUILD_GUIDE.md`
- **Flask Docs**: https://flask.palletsprojects.com/
- **python-docx Docs**: https://python-docx.readthedocs.io/

## ⚓ Credits

Built for maritime maintenance tracking operations.

## 📄 License

Proprietary - For internal use only.
