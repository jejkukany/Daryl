# ─── ENV LIBS ───────────────────────────────────────────────────────────────────

import os
from dotenv import load_dotenv

# ─── ENV LOADER ─────────────────────────────────────────────────────────────────

load_dotenv()

TTOKEN= os.getenv('TTOKEN')
APIKEY= os.getenv('APIKEY')
AUTHDOMAIN= os.getenv('AUTHDOMAIN')
DATABASEURL= os.getenv('DATABASEURL')
PROJECTID= os.getenv('PROJECTID')
STORAGEBUCKET= os.getenv('STORAGEBUCKET')
MESSAGINGSENDERID= os.getenv('MESSAGINGSENDERID')
APPID= os.getenv('APPID')
MEASUREMENTID= os.getenv('MEASUREMENTID')

# ─── KEYS AND CONFIG ────────────────────────────────────────────────────────────

ttoken = TTOKEN

firebaseconfig = {
'apiKey': APIKEY,
'authDomain': AUTHDOMAIN,
'databaseURL': DATABASEURL,
'projectId': PROJECTID,
'storageBucket': STORAGEBUCKET,
'messagingSenderId': MESSAGINGSENDERID,
'appId': APPID,
'measurementId': MEASUREMENTID
}