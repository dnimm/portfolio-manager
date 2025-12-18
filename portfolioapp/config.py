# config.py

# simple dictionary for the database info
database_config = {
    "user": "root",
    "password": "12345678",   
    "host": "localhost",
    "port": "3306",
    "database": "portfolio_db"
}

class Config:
    DEBUG = True

    # connection string for flask_sqlalchemy
    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{database_config['user']}:{database_config['password']}"
        f"@{database_config['host']}:{database_config['port']}/{database_config['database']}"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False
