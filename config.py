import os 
from pathlib import Path

class Config(object):
    SECRET_KEY= os.environ.get('SECRET_KEY') or 'fvjnfjbnjfbnjfgnbjfgnbjfg'
    SQLALCHEMY_DATABASE_URI= 'sqlite:///'+ os.path.join(Path().absolute(),'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS= False
