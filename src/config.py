from dotenv import load_dotenv
import os

load_dotenv()

DB_HOST = os.environ.get('DB_HOST')
DB_PORT = os.environ.get('DB_PORT')
DB_NAME = os.environ.get('DB_NAME')
DB_USER = os.environ.get('DB_USER')
DB_PASS = os.environ.get('DB_PASS')
SECRET_KEY_PUBLIC = os.environ.get('SECRET_KEY_PUBLIC')
SECRET_KEY_PRIVATE = os.environ.get('SECRET_KEY_PRIVATE')
SECRET_KEY_HS256 = os.environ.get('SECRET_KEY_HS256')
SECRET_KEY_RESET = os.environ.get('SECRET_KEY_RESET')
SECRET_KEY_VERIFICATION = os.environ.get('SECRET_KEY_VERIFICATION')


