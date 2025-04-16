# PC Automation System

A Python-based PC automation system that can read the screen, control input devices, and execute user-specified tasks.

## Overview

This system provides a web interface to control your computer. It can:
- Capture screen content
- Extract text from the screen using OCR
- Control mouse movements and clicks
- Type text and press keyboard shortcuts
- Open applications
- Execute complex tasks through natural language commands

## Running Modes

### Simulation Mode (Default in Replit)

By default, the application runs in simulation mode, which doesn't actually control your computer but simulates the actions. This is ideal for:
- Testing the interface
- Demonstrating the functionality
- Running in environments without GUI access (like Replit)

### Actual Control Mode (Local Installation)

To use the system to actually control your computer, you need to install and run it locally:

1. **Requirements**:
   - Python 3.6 or higher
   - X11 display server (for Linux/Unix)
   - Windows or macOS GUI

2. **Installation**:
   ```bash
   # Clone this repository
   git clone <repository-url>
   cd pc-automation-system
   
   # Create virtual environment
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   
   # Install dependencies
   pip install -r requirements.txt
   
   # Additional Requirements:
   # - For OCR: Install Tesseract OCR (https://github.com/tesseract-ocr/tesseract)
   # - For Linux: Install X11 dependencies (sudo apt-get install python3-tk python3-dev)
   ```

3. **Running**:
   ```bash
   python app.py
   ```
   
   This will start the web interface at http://localhost:5000

## Dependencies

- **Core**:
  - Flask (web interface)
  - PyAutoGUI (mouse and keyboard control)
  - Pillow (image processing)
  - OpenCV (computer vision)
  - Pytesseract (OCR)

- **Development**:
  - pytest (testing)
  - flake8 (linting)

## Usage

1. Open the web interface in your browser
2. Use the various control panels to interact with your computer
3. Try the task execution feature with natural language commands like:
   - "open chrome"
   - "click at 500, 300"
   - "type Hello, world!"
   - "press ctrl+c"
   - "read screen"

## Security Notice

This application provides full control of your computer through a web interface. Use it responsibly and be aware of the following:

- Only run it on trusted networks
- Consider adding authentication if needed
- Be careful with what commands you execute

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.