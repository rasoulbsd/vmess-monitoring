from flask import Flask, request, jsonify
from .config import Config
from .auth import require_api_key, require_basic_auth
from .vmess_tester import test_vmess_connection


def create_app():
    """Create and configure the Flask application"""
    app = Flask(__name__)
    
    @app.route('/')
    def index():
        """Health check endpoint"""
        return jsonify({
            'status': 'running',
            'service': 'VMess Monitoring API',
            'version': '1.0.0'
        })
    
    @app.route('/health')
    def health():
        """Health check endpoint"""
        return jsonify({'status': 'healthy'})
    
    @app.route('/api/test-vmess', methods=['POST'])
    @require_api_key
    def test_vmess_api():
        """Test a VMess connection via API key authentication"""
        data = request.get_json()
        
        if not data or 'vmess_link' not in data:
            return jsonify({'error': 'vmess_link is required'}), 400
        
        vmess_link = data['vmess_link']
        dest_url = data.get('dest_url')
        
        result = test_vmess_connection(vmess_link, dest_url)
        return jsonify(result)
    
    @app.route('/api/test-vmess-basic', methods=['POST'])
    @require_basic_auth
    def test_vmess_basic():
        """Test a VMess connection via basic authentication"""
        data = request.get_json()
        
        if not data or 'vmess_link' not in data:
            return jsonify({'error': 'vmess_link is required'}), 400
        
        vmess_link = data['vmess_link']
        dest_url = data.get('dest_url')
        
        result = test_vmess_connection(vmess_link, dest_url)
        return jsonify(result)
    
    @app.route('/api/test-vmess-auth', methods=['POST'])
    def test_vmess_flexible():
        """Test a VMess connection with flexible authentication"""
        from .auth import get_auth_method
        
        auth_method = get_auth_method()
        if not auth_method:
            return jsonify({'error': 'Authentication required'}), 401
        
        data = request.get_json()
        
        if not data or 'vmess_link' not in data:
            return jsonify({'error': 'vmess_link is required'}), 400
        
        vmess_link = data['vmess_link']
        dest_url = data.get('dest_url')
        
        result = test_vmess_connection(vmess_link, dest_url)
        result['auth_method'] = auth_method
        return jsonify(result)
    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Endpoint not found'}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({'error': 'Internal server error'}), 500
    
    return app


def run_server():
    """Run the Flask server"""
    app = create_app()
    app.run(
        host=Config.SERVER_HOST,
        port=Config.SERVER_PORT,
        debug=Config.DEBUG
    )


if __name__ == '__main__':
    run_server() 