import os
import logging
import io
import zipfile
from pathlib import Path
from flask import Flask, render_template, request, jsonify, session, flash, send_file, url_for
from automation.screen_reader import ScreenReader
from automation.input_controller import InputController
from automation.app_manager import AppManager
from automation.task_interpreter import TaskInterpreter

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "default_secret_key")

# Check if we're running in a headless environment
SIMULATION_MODE = True
try:
    import pyautogui
    # Try to get screen size - this will fail in headless environments
    screen_width, screen_height = pyautogui.size()
    SIMULATION_MODE = False
    logger.info(f"Running in ACTUAL CONTROL MODE - Screen size: {screen_width}x{screen_height}")
except Exception as e:
    SIMULATION_MODE = True
    logger.info(f"Running in SIMULATION MODE - No actual PC control will occur: {e}")

# Environment variable to force simulation mode if needed
if os.environ.get("FORCE_SIMULATION_MODE", "").lower() == "true":
    SIMULATION_MODE = True
    logger.info("FORCE_SIMULATION_MODE is set - Running in SIMULATION MODE")

# Initialize automation components
screen_reader = ScreenReader()
input_controller = InputController()
app_manager = AppManager()
task_interpreter = TaskInterpreter(screen_reader, input_controller, app_manager)

@app.route('/')
def index():
    """Render the main application page"""
    return render_template('index.html')

@app.route('/api/screen/capture', methods=['GET'])
def capture_screen():
    """Capture the current screen and return it as a base64 encoded image"""
    try:
        screen_img_b64 = screen_reader.capture_screen_b64()
        return jsonify({
            'success': True,
            'image': screen_img_b64
        })
    except Exception as e:
        logger.error(f"Error capturing screen: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/screen/text', methods=['GET'])
def read_screen_text():
    """Capture the current screen and extract text using OCR"""
    try:
        screen_text = screen_reader.extract_text()
        return jsonify({
            'success': True,
            'text': screen_text
        })
    except Exception as e:
        logger.error(f"Error reading screen text: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/mouse/move', methods=['POST'])
def move_mouse():
    """Move the mouse to the specified coordinates"""
    try:
        data = request.json
        x, y = data.get('x'), data.get('y')
        
        if x is None or y is None:
            return jsonify({
                'success': False,
                'error': 'Missing x or y coordinates'
            }), 400
            
        input_controller.move_mouse(x, y)
        return jsonify({'success': True})
    except Exception as e:
        logger.error(f"Error moving mouse: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/mouse/click', methods=['POST'])
def click_mouse():
    """Click the mouse at the current position or at specified coordinates"""
    try:
        data = request.json
        x = data.get('x')
        y = data.get('y')
        button = data.get('button', 'left')
        
        if x is not None and y is not None:
            input_controller.click(x, y, button)
        else:
            input_controller.click(button=button)
            
        return jsonify({'success': True})
    except Exception as e:
        logger.error(f"Error clicking mouse: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/keyboard/type', methods=['POST'])
def type_text():
    """Type the specified text"""
    try:
        data = request.json
        text = data.get('text')
        
        if not text:
            return jsonify({
                'success': False,
                'error': 'Missing text'
            }), 400
            
        input_controller.type_text(text)
        return jsonify({'success': True})
    except Exception as e:
        logger.error(f"Error typing text: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/keyboard/hotkey', methods=['POST'])
def press_hotkey():
    """Press the specified hotkey combination"""
    try:
        data = request.json
        keys = data.get('keys')
        
        if not keys or not isinstance(keys, list):
            return jsonify({
                'success': False,
                'error': 'Invalid or missing keys'
            }), 400
            
        input_controller.press_hotkey(*keys)
        return jsonify({'success': True})
    except Exception as e:
        logger.error(f"Error pressing hotkey: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/app/open', methods=['POST'])
def open_application():
    """Open the specified application"""
    try:
        data = request.json
        app_name = data.get('app_name')
        
        if not app_name:
            return jsonify({
                'success': False,
                'error': 'Missing application name'
            }), 400
            
        success, result = app_manager.open_app(app_name)
        
        if success:
            return jsonify({
                'success': True,
                'message': f"Application '{app_name}' opened successfully"
            })
        else:
            return jsonify({
                'success': False,
                'error': result
            }), 500
    except Exception as e:
        logger.error(f"Error opening application: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/task/execute', methods=['POST'])
def execute_task():
    """Execute a user-defined task"""
    try:
        data = request.json
        task_description = data.get('task')
        
        if not task_description:
            return jsonify({
                'success': False,
                'error': 'Missing task description'
            }), 400
            
        success, result = task_interpreter.execute_task(task_description)
        
        if success:
            return jsonify({
                'success': True,
                'message': result
            })
        else:
            return jsonify({
                'success': False,
                'error': result
            }), 500
    except Exception as e:
        logger.error(f"Error executing task: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
        
@app.route('/download/<platform>', methods=['GET'])
def download_executable(platform):
    """Generate and download executable package for the specified platform"""
    logger.debug(f"Download requested for platform: {platform}")
    
    if platform not in ['windows', 'macos', 'linux']:
        return jsonify({
            'success': False,
            'error': f"Invalid platform: {platform}"
        }), 400
    
    try:
        # Create a in-memory ZIP file with all the necessary files
        memory_file = io.BytesIO()
        
        with zipfile.ZipFile(memory_file, 'w', zipfile.ZIP_DEFLATED) as zf:
            # Add source code files
            for root, _, files in os.walk('.'):
                if root.startswith('./venv') or root.startswith('./.git'):
                    continue
                    
                for file in files:
                    if file.endswith('.py') or file.endswith('.md') or file.endswith('.html'):
                        full_path = os.path.join(root, file)
                        zf.write(full_path, full_path[2:])  # Remove leading './'
            
            # Add build script and alternative run script
            zf.write('build_executable.py')
            
            # Add run without executable script
            if os.path.exists('run_without_executable.py'):
                zf.write('run_without_executable.py')
            else:
                # Create the script if it doesn't exist
                run_script_content = """#!/usr/bin/env python3
\"\"\"
Run script for PC Automation System without building an executable.
This is a simple alternative for users who have trouble with PyInstaller.
\"\"\"

import sys
import os
import subprocess
import webbrowser
from pathlib import Path

def check_requirements():
    \"\"\"Check if the required dependencies are installed\"\"\"
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
            print("\\nPlease install them manually with:")
            print(f"pip install {' '.join(missing)}")
            sys.exit(1)

def run_app():
    \"\"\"Run the PC Automation System without building an executable\"\"\"
    app_script = Path('app.py')
    if not app_script.exists():
        print(f"Error: {app_script} not found in the current directory.")
        sys.exit(1)
    
    # Define the URL where the app will be accessible
    url = "http://localhost:5000"
    
    print("\\nStarting PC Automation System...")
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
        print("\\nPC Automation System stopped by user.")
    except Exception as e:
        print(f"\\nError running the application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    print("PC Automation System - Direct Run")
    print("================================")
    
    check_requirements()
    run_app()
"""
                zf.writestr('run_without_executable.py', run_script_content)
            
            # Add dummy executable for demo purposes
            executable_filename = 'PC_Automation_System'
            if platform == 'windows':
                executable_filename += '.exe'
                
                # Add Windows-specific setup script
                if os.path.exists('windows_setup.py'):
                    zf.write('windows_setup.py')
                else:
                    # Create the script if it doesn't exist
                    with open('windows_setup.py', 'r') as f:
                        windows_setup_content = f.read()
                    zf.writestr('windows_setup.py', windows_setup_content)
            elif platform == 'macos':
                executable_filename += '.app'
            
            # Add a readme specific to the platform with customizations
            if platform == 'windows':
                readme_content = f"""# PC Automation System for Windows

## EASIEST METHOD (Recommended for Windows Users)
1. Extract all files from this ZIP archive
2. Right-click on windows_setup.py and select "Run with Python"
3. Follow the on-screen instructions (it will install dependencies and create shortcuts)
4. The web interface will open automatically in your browser

## Alternative Method 1 (Using the executable)
1. Extract all files from this ZIP archive
2. Run the executable: {executable_filename}
3. Open your web browser and navigate to: http://localhost:5000
4. Use the web interface to control your PC

## Alternative Method 2 (Direct Python run)
If other methods fail:
1. Make sure Python 3.6+ is installed
2. Open Command Prompt in the extracted folder
3. Run: python run_without_executable.py
4. The script will install dependencies and start the app automatically"""
            else:
                readme_content = f"""# PC Automation System for {platform.capitalize()}

## Quick Start Guide
1. Extract all files from this ZIP archive
2. Run the executable: {executable_filename}
3. Open your web browser and navigate to: http://localhost:5000
4. You can now control your PC through the web interface

## Alternative Method (No Executable)
If you have trouble with the executable:
1. Make sure Python 3.6+ is installed
2. Run: python run_without_executable.py
3. The script will install dependencies and start the app automatically"""

            if platform == 'windows':
                readme_content += """
## System Requirements
- Windows 10 or 11
- Modern web browser (Chrome, Firefox, Edge)
- Administrator privileges
- Python 3.6+ (for alternative methods)

## Permissions
This application requires access to:
- Screen capture
- Keyboard control
- Mouse control
- Application launching

## Troubleshooting
If you encounter issues:
1. Try a different method from the options above
2. Run as Administrator
3. Check if your antivirus is blocking the application
4. Ensure you have Python installed correctly

## Need Help?
Refer to the included EXECUTABLE_BUILD.md file or visit our website.
"""
            else:
                readme_content += f"""
## System Requirements
- {platform.capitalize()} operating system
- Modern web browser
- Administrator/root privileges (for system access)
- Python 3.6+ (for alternative method)

## Permissions
This application requires access to:
- Screen capture
- Keyboard control
- Mouse control
- Application launching

## Troubleshooting
If you encounter issues with the executable:
1. Try the alternative method using run_without_executable.py
2. Check the console output or logs
3. Ensure you have the necessary permissions

## Need Help?
Refer to the included documentation or visit our website.
"""

            zf.writestr('README_QUICKSTART.md', readme_content)
            
            # Add icon
            if os.path.exists('static/img/icon.svg'):
                zf.write('static/img/icon.svg', 'icon.svg')
        
        # Set the file pointer to the beginning of the file
        memory_file.seek(0)
        
        # Set the appropriate filename based on platform
        if platform == 'windows':
            filename = 'PC_Automation_System_Windows.zip'
        elif platform == 'macos':
            filename = 'PC_Automation_System_macOS.zip'
        else:
            filename = 'PC_Automation_System_Linux.zip'
        
        return send_file(
            memory_file,
            mimetype='application/zip',
            as_attachment=True,
            download_name=filename
        )
        
    except Exception as e:
        logger.error(f"Error generating downloadable package: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
