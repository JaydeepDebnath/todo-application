import os

class Config:
    DEBUG = False
    TESTING = False
    SECRET_KEY = '*'  # Change this to a secure value
    SQLALCHEMY_DATABASE_URI = 'sqlite:///your_database_name.db'  # Example for SQLite database
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    KEYCLOAK_SERVER_URL = 'KEYCLOAK_SERVER_URL'
    KEYCLOAK_REALM = 'KEYCLOAK_REALM'
    KEYCLOAK_CLIENT_ID = 'CLIENT_ID'

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    # Configure for production settings
    pass

# Choose the configuration class based on environment
def get_config():
    env = os.environ.get('env', 'development')
    if env == 'production':
        return ProductionConfig()
    else:
        return DevelopmentConfig()