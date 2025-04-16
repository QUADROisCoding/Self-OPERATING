# Installation Guide for PC Automation System

Follow these steps to install and run the PC Automation System on your local machine with full control capabilities.

## Prerequisites

- Python 3.6 or higher
- Admin/sudo privileges (for installing system dependencies)
- GUI environment (Windows, macOS, or Linux with X server)

## Step-by-Step Installation

### 1. Clone or Download the Repository

```bash
git clone https://github.com/yourusername/pc-automation-system.git
cd pc-automation-system
```

Or download and extract the ZIP file.

### 2. Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Required Python Packages

```bash
pip install flask gunicorn pillow pyautogui psutil opencv-python numpy pytesseract
```

### 4. Install System Dependencies

#### For Windows:
- No additional dependencies required

#### For macOS:
```bash
brew install tesseract
```

#### For Linux (Ubuntu/Debian):
```bash
sudo apt-get update
sudo apt-get install python3-tk python3-dev scrot tesseract-ocr
sudo apt-get install libxtst-dev libpng-dev libjpeg-dev
```

### 5. Configure Environment

By default, the application will detect whether it can use real PC control or needs to run in simulation mode.

To force simulation mode (even if real control is possible):
```bash
# Windows
set FORCE_SIMULATION_MODE=true

# macOS/Linux
export FORCE_SIMULATION_MODE=true
```

### 6. Run the Application

```bash
python app.py
```

The web interface will be available at: http://localhost:5000

## Troubleshooting

### PyAutoGUI Issues

If you encounter errors with PyAutoGUI:

- **Windows**: Make sure you're not running as administrator
- **macOS**: Grant accessibility permissions in System Preferences > Security & Privacy > Accessibility
- **Linux**: Make sure X server is running and accessible

### Tesseract OCR Issues

If OCR is not working:

- Make sure Tesseract is correctly installed
- Try setting the path to Tesseract executable:
  ```python
  pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Windows example
  ```

## Headless Environments

This application requires a GUI environment to perform actual PC control. If running in a headless environment (like a server), it will automatically fall back to simulation mode.

## Security Considerations

- This application gives web-based control to your computer
- Only run it on secured networks
- Consider adding authentication if exposing beyond localhost