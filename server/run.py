#!/usr/bin/env python3
"""
VMess Monitoring Web Server
A simple web server for testing VMess connections via API
"""

import os
from server.config import Config


def run_development():
    """Run the Flask development server"""
    from server.app import run_server
    print("Starting VMess Monitoring Web Server (Development)...")
    run_server()


def run_production():
    """Run with gunicorn for production"""
    import subprocess
    
    # Build gunicorn command
    cmd = [
        "gunicorn",
        "--bind", Config.GUNICORN_BIND,
        "--workers", str(Config.GUNICORN_WORKERS),
        "--timeout", str(Config.GUNICORN_TIMEOUT),
        "--access-logfile", "-",
        "--error-logfile", "-",
        "server.wsgi:app"
    ]
    
    print("Starting VMess Monitoring Web Server (Production)...")
    print(f"Workers: {Config.GUNICORN_WORKERS}")
    print(f"Timeout: {Config.GUNICORN_TIMEOUT}s")
    print(f"Bind: {Config.GUNICORN_BIND}")
    
    # Run gunicorn
    subprocess.run(cmd)


if __name__ == '__main__':
    # Check if we're in development or production mode
    if os.getenv('FLASK_ENV') == 'development' or Config.DEBUG:
        run_development()
    else:
        run_production() 