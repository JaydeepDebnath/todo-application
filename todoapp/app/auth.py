from flask_keycloak import FlaskKeycloak
from flask import request
from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix


class KeycloakMiddleware:
    def __init__(self, app):
        self.app = app
        self.keycloak = FlaskKeycloak(app)
        
    def __call__(self, environ, start_response):
        with self.app.request_context(environ):
            if not request.endpoint or request.endpoint == 'static':
                return self.app(environ, start_response)
            elif not self.keycloak.introspect():
                start_response('401 Unauthorized', [('Content-Type', 'application/json')])
                return [b'{"error": "Unauthorized"}']
            return self.app(environ, start_response)
        
def create_app():
    app = Flask(__name__)
    app.wsgi_app = ProxyFix(app.wsgi_app) 
    app.config['KEYCLOAK_SERVER_URL'] = 'YOUR_KEYCLOAK_SERVER_URL'
    app.config['KEYCLOAK_REALM'] = 'YOUR_KEYCLOAK_REALM'
    app.config['KEYCLOAK_CLIENT_ID'] = 'YOUR_CLIENT_ID'

    keycloak_middleware = KeycloakMiddleware(app)

    return app

app = create_app