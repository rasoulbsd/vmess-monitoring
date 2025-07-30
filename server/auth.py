from functools import wraps
from flask import request, jsonify
from .config import Config


def require_api_key(f):
    """Decorator to require API key authentication"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        if not api_key or api_key != Config.API_KEY:
            return jsonify({'error': 'Invalid or missing API key'}), 401
        return f(*args, **kwargs)
    return decorated_function


def require_basic_auth(f):
    """Decorator to require basic authentication"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth = request.authorization
        if (not auth or auth.username != Config.USERNAME or 
                auth.password != Config.PASSWORD):
            return jsonify({'error': 'Invalid credentials'}), 401
        return f(*args, **kwargs)
    return decorated_function


def get_auth_method():
    """Get the authentication method from request headers"""
    if request.headers.get('X-API-Key'):
        return 'api_key'
    elif request.authorization:
        return 'basic_auth'
    return None 