import os
from datetime import timedelta


class Config:
    # Flask Environment
    FLASK_ENV = os.environ.get('FLASK_ENV', 'development')

    # Security
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'

    # Ensure SECRET_KEY is set in production
    if FLASK_ENV == 'production' and SECRET_KEY == 'dev-secret-key-change-in-production':
        raise ValueError("SECRET_KEY must be set in production environment!")

    # Database Configuration
    database_url = os.environ.get('DATABASE_URL') or 'sqlite:///maintenance.db'

    # Railway provides DATABASE_URL starting with postgres://
    # but SQLAlchemy 1.4+ requires postgresql://
    if database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)

    SQLALCHEMY_DATABASE_URI = database_url
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,
        'pool_recycle': 300,
    }

    # File Upload Configuration
    # Railway allows only ONE volume per service
    # Mount volume at /app/data and use subdirectories
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    DATA_DIR = os.path.join(BASE_DIR, 'data')
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER') or os.path.join(BASE_DIR, 'uploads')
    GENERATED_DOCS_FOLDER = os.environ.get('GENERATED_DOCS_FOLDER') or os.path.join(DATA_DIR, 'generated_docs')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'heic', 'heif'}

    PHOTO_MAX_WIDTH = 576
    PHOTO_MIN_COUNT = 0
    PHOTO_MAX_COUNT = 6

    CREW_PASSWORD = os.environ.get('CREW_PASSWORD') or 'crew350'

    ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME') or 'admin'
    ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD') or 'admin350'

    CREW_MEMBERS = [
        'DP',
        'AL',
        'Kaitlyn',
        'Mark',
        'Art',
        'D2',
        'Zach',
        'Maverick',
        'Rhyan',
    ]

    # EV Yard Items (from sister ship Eagleview scope)
    EV_YARD_ITEMS = [
        '0101 - Pilot House Windows',
        '0104 - Exterior Deck Coatings',
        '0110 - Misc Welding Repairs',
        '0113 - Main Deck Inspection & Steel',
        '0114 - Bow Thruster Exhaust Insulation',
        '0115 - Main Deck Exhaust Painting',
        '0117 - Frames 66/70 for GMS Installation',
        '0310 - Electrical Panel Load Survey',
        '0401 - Ships Horn Installation',
        '0502 - Deck Crane Maintenance',
        '0503 - Rebuild Steering Cylinders',
        '0604 - Replace Countertops & Sinks',
        '0605 - Replace Stateroom Toilets',
        '0701 - Aft GMS Installation',
        '0702 - Weapons Maintenance Area',
        '0703 - Main Deck Magazine Repairs',
        '0705 - Deck Container Painting',
        '0958 - Propeller Clean/Polish & Hull',
    ]

    # Draft Items (new work items for 2026)
    DRAFT_ITEMS = [
        'DRAFT_0001 - Replace All A/C Units',
        'DRAFT_0002 - Replace Immersion Suits',
        'DRAFT_0003 - Main Deck ARMAG Mods',
        'DRAFT_0004 - Remove Unused Cabling/Rewire',
        'DRAFT_0005 - Galley Gaylord Hood Clean/Reseal',
        'DRAFT_0006 - Chemical Drain Clean & MSD Service',
        'DRAFT_0007 - Replace Angle Drive Spider Gear',
        'DRAFT_0008 - Load Bank on SSDGs & Switchboard Breakers',
        'DRAFT_0009 - EMI Steering Upgrades',
        'DRAFT_0010 - Red Gear Shaft Drive Pumps',
        'DRAFT_0011 - Potable Water Pumps Replacement',
        'DRAFT_0012 - Refurbish Fire Trunk Fire Barriers',
        'DRAFT_0013 - Fuel Piping Mount 14S',
        'DRAFT_0014 - ATOS Valves Quantum',
        'DRAFT_0015 - Reband Wire Runs on Mast',
        'DRAFT_0016 - Gyro Sensitive Elements Replacement',
        'DRAFT_0017 - Head Tank Sight Glasses/Valves/Murphy Switches',
        'DRAFT_0018 - Annex Passageway Floor Bubble Repair',
        'DRAFT_0019 - Add Smoke Detector/Phone to Conference',
    ]

    PERMANENT_SESSION_LIFETIME = timedelta(hours=8)
    
    # Status workflow options
    STATUS_OPTIONS = [
        'Submitted',
        'In Review by DP',
        'In Review by AL',
        'Needs Revision',
        'Awaiting Photos',
        'Completed Review',
    ]
    
    # SMS Notifications via Twilio
    ENABLE_NOTIFICATIONS = os.environ.get('ENABLE_NOTIFICATIONS', 'False').lower() == 'true'

    # Twilio credentials
    TWILIO_ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID')
    TWILIO_AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN')
    TWILIO_FROM_NUMBER = os.environ.get('TWILIO_FROM_NUMBER')

    # Base URL for crew login page (used in SMS messages)
    CREW_LOGIN_URL = os.environ.get('CREW_LOGIN_URL', 'http://localhost:5000/crew/login')

    # Crew phone number mapping (for SMS notifications)
    # Format: E.164 (e.g., +1234567890)
    CREW_PHONES = {
        'DP': os.environ.get('DP_PHONE'),
        'AL': os.environ.get('AL_PHONE'),
        'Kaitlyn': os.environ.get('KAITLYN_PHONE'),
        'Mark': os.environ.get('MARK_PHONE'),
        'Art': os.environ.get('ART_PHONE'),
        'D2': os.environ.get('D2_PHONE'),
        'Zach': os.environ.get('ZACH_PHONE'),
        'Maverick': os.environ.get('MAVERICK_PHONE'),
        'Rhyan': os.environ.get('RHYAN_PHONE'),
    }
