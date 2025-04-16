#!/usr/bin/env python3
"""
Run script for PC Automation System without building an executable.
This is a simple alternative for users who have trouble with PyInstaller.
"""

import sys
import os
import subprocess
import webbrowser
from pathlib import Path

def check_requirements():
    """Check if the required dependencies are installed"""
    requirements = [
        'flask',
        'pillow',
        'pyautogui',
        'opencv-python',
        'numpy',
        'pytesseract'
    ]
    
    missing = []
    
    for req in requirements:
        try:
            __import__(req.replace('-', '_'))
        except ImportError:
            missing.append(req)
    
    if missing:
        print(f"Missing dependencies: {', '.join(missing)}")
        print("Installing missing dependencies...")
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install'] + missing)
            print("All dependencies installed successfully.")
        except Exception as e:
            print(f"Failed to install dependencies: {e}")
            print("\nPlease install them manually with:")
            print(f"pip install {' '.join(missing)}")
            sys.exit(1)

def run_app():
    """Run the PC Automation System without building an executable"""
    app_script = Path('app.py')
    if not app_script.exists():
        print(f"Error: {app_script} not found in the current directory.")
        sys.exit(1)
    
    # Define the URL where the app will be accessible
    url = "http://localhost:5000"
    
    print("\nStarting PC Automation System...")
    print(f"The application will be available at: {url}")
    
    # Open web browser after a short delay
    def open_browser():
        import time
        # Wait for the server to start
        time.sleep(2)
        print("Opening web browser...")
        webbrowser.open(url)
    
    # Start the browser in a separate thread
    import threading
    browser_thread = threading.Thread(target=open_browser)
    browser_thread.daemon = True
    browser_thread.start()
    
    # Start the Flask application
    try:
        # Run the Flask app directly
        subprocess.check_call([sys.executable, str(app_script)])
    except KeyboardInterrupt:
        print("\nPC Automation System stopped by user.")
    except Exception as e:
        print(f"\nError running the application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    print("PC Automation System - Direct Run")
    print("================================")
    
    check_requirements()
    run_app()