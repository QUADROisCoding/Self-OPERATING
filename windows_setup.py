#!/usr/bin/env python3
"""
Windows Setup Script for PC Automation System
A simple, direct way to run the PC Automation System on Windows
without requiring PyInstaller.
"""

import os
import sys
import subprocess
import webbrowser
import time
import threading
import shutil
from pathlib import Path

def print_header():
    """Print the header information"""
    print("==================================================")
    print("    PC Automation System - Windows Setup Script    ")
    print("==================================================")
    print("This script will help you set up and run the PC Automation System.")
    print("No executable building required!")
    print()

def check_python_version():
    """Check that Python is the correct version"""
    print("Checking Python version...")
    major = sys.version_info.major
    minor = sys.version_info.minor
    
    if major < 3 or (major == 3 and minor < 6):
        print(f"Error: Python 3.6+ is required. You have Python {major}.{minor}")
        print("Please install a newer version of Python from https://www.python.org/downloads/")
        input("Press Enter to exit...")
        sys.exit(1)
    
    print(f"✓ Python {major}.{minor} detected (OK)")
    print()

def create_desktop_shortcut():
    """Create a desktop shortcut for the application"""
    try:
        # Get the desktop path
        desktop_path = Path.home() / "Desktop"
        
        if not desktop_path.exists():
            print("Could not locate Desktop folder.")
            return False
        
        # Get the current script directory
        script_dir = Path(__file__).resolve().parent
        
        # Create the batch file in the script directory first
        batch_path = script_dir / "Run_PC_Automation.bat"
        batch_content = f"""@echo off
echo Starting PC Automation System...
cd /d "{script_dir}"
python "{script_dir / 'run_without_executable.py'}"
"""
        
        with open(batch_path, 'w') as f:
            f.write(batch_content)
        
        # Create a shortcut to the batch file on the desktop
        shortcut_path = desktop_path / "PC Automation System.lnk"
        
        # Windows-specific import
        try:
            import win32com.client
            shell = win32com.client.Dispatch("WScript.Shell")
            shortcut = shell.CreateShortCut(str(shortcut_path))
            shortcut.Targetpath = str(batch_path)
            shortcut.WorkingDirectory = str(script_dir)
            shortcut.IconLocation = str(script_dir / "icon.ico")
            shortcut.save()
            print("✓ Desktop shortcut created successfully.")
            return True
        except ImportError:
            print("Note: Could not create shortcut (win32com module not available).")
            print(f"✓ Batch file created at: {batch_path}")
            print("   You can manually copy this to your desktop if desired.")
            return False
    except Exception as e:
        print(f"Note: Could not create desktop shortcut: {e}")
        return False

def install_dependencies():
    """Install required dependencies"""
    print("Checking and installing required dependencies...")
    requirements = [
        'flask',
        'pillow',
        'pyautogui',
        'opencv-python',
        'numpy',
        'pytesseract',
        'pywin32'  # For creating the shortcut
    ]
    
    missing = []
    
    for req in requirements:
        try:
            if req == 'pywin32':
                # Special case for pywin32
                try:
                    import win32com.client
                except ImportError:
                    missing.append(req)
            else:
                __import__(req.replace('-', '_'))
        except ImportError:
            missing.append(req)
    
    if missing:
        print(f"Installing missing dependencies: {', '.join(missing)}")
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install'] + missing)
            print("✓ All dependencies installed successfully.")
        except Exception as e:
            print(f"Warning: Failed to install some dependencies: {e}")
            print("\nPlease try installing them manually with:")
            print(f"pip install {' '.join(missing)}")
            choice = input("Continue anyway? (Y/n): ")
            if choice.lower() == 'n':
                sys.exit(1)
    else:
        print("✓ All dependencies are already installed.")
    
    print()

def run_application():
    """Run the PC Automation System"""
    print("Starting PC Automation System...")
    url = "http://localhost:5000"
    
    # Check if app.py exists
    app_script = Path('app.py')
    if not app_script.exists():
        print(f"Error: {app_script} not found in the current directory.")
        input("Press Enter to exit...")
        sys.exit(1)
    
    # Function to open browser
    def open_browser():
        time.sleep(2)  # Give Flask time to start
        print(f"Opening web browser to {url}")
        webbrowser.open(url)
    
    # Start browser in a separate thread
    browser_thread = threading.Thread(target=open_browser)
    browser_thread.daemon = True
    browser_thread.start()
    
    # Start Flask
    print(f"Web interface will be available at: {url}")
    print("Press Ctrl+C to stop the server.")
    print()
    
    try:
        subprocess.check_call([sys.executable, str(app_script)])
    except KeyboardInterrupt:
        print("\nPC Automation System stopped.")
    except Exception as e:
        print(f"\nError running the application: {e}")
        input("Press Enter to exit...")
        sys.exit(1)

def main():
    """Main function"""
    print_header()
    check_python_version()
    install_dependencies()
    
    # Ask if user wants to create a desktop shortcut
    print("Would you like to create a desktop shortcut for easy access?")
    choice = input("Create desktop shortcut? (Y/n): ")
    
    if choice.lower() != 'n':
        create_desktop_shortcut()
    
    print("\nSetup complete! Starting PC Automation System...\n")
    
    run_application()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nSetup cancelled by user.")
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        input("Press Enter to exit...")