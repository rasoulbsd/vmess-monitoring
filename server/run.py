#!/usr/bin/env python3
"""
VMess Monitoring Web Server
A simple web server for testing VMess connections via API
"""

from server.app import run_server


if __name__ == '__main__':
    print("Starting VMess Monitoring Web Server...")
    run_server() 