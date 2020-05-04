import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):

    # SECRET KEY
    SECRET_KEY =  os.environ.get('SECRET_KEY') or 'A-VERY-LONG-SECRET-KEY'

    # RECAPTCHA PUBLIC KEY
    RECAPTCHA_PUBLIC_KEY = os.environ.get('RECAPTCHA_PUBLIC_KEY') or '6LcF7uwUAAAAAPn3nBtir1PB-kW-Pd2W4H4cFtgF'
    RECAPTCHA_PRIVATE_KEY = os.environ.get('RECAPTCHA_PRIVATE_KEY') or '6LcF7uwUAAAAAMfRGik8Jend-I0T82GX-nnL03wm'

    # database configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False