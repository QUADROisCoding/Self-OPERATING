# PC Automation System - Executable Build Guide

This guide provides details on how to build the PC Automation System executable and what to do if you encounter issues with PyInstaller.

## Building the Executable

The `build_executable.py` script uses PyInstaller to package the application into a single executable file that runs without requiring Python or any dependencies to be pre-installed.

### Prerequisites

- Python 3.6 or higher
- PyInstaller (`pip install pyinstaller`)
- All dependencies installed (`pip install -r requirements.txt`)

### Standard Build Process

1. Run the build script:
   ```
   python build_executable.py
   ```

2. The script will:
   - Check if PyInstaller is installed
   - Detect your operating system and set appropriate settings
   - Build the executable using PyInstaller
   - Create a distribution package in the `dist_package` directory

3. Once the build is complete, the executable will be located in:
   - `dist/PC_Automation_System.exe` (Windows)
   - `dist/PC_Automation_System.app` (macOS)
   - `dist/PC_Automation_System` (Linux)

## Troubleshooting

### Common Issues

#### 1. PyInstaller Not Found

If you receive an error about PyInstaller not being found:

```
FileNotFoundError: [WinError 2] The system cannot find the file specified
```

Try these solutions:

a. Install PyInstaller manually:
   ```
   pip install pyinstaller
   ```

b. Use the module syntax:
   ```
   python -m PyInstaller --onefile --windowed app.py
   ```

c. Add the PyInstaller directory to your PATH environment variable

#### 2. Missing Dependencies

If you encounter errors about missing dependencies:

a. Make sure all requirements are installed:
   ```
   pip install -r requirements.txt
   ```

b. Install the specific missing package:
   ```
   pip install <package_name>
   ```

#### 3. Permission Errors

If you encounter permission errors on Windows:

a. Run the command prompt as Administrator
b. Try using a virtual environment

### Alternative: Running Without an Executable

If you're having persistent issues with PyInstaller, you can run the application directly with Python:

1. Use the included `run_without_executable.py` script:
   ```
   python run_without_executable.py
   ```

2. This script will:
   - Check and install required dependencies
   - Start the Flask server
   - Open a browser window to the application

3. Your PC Automation System will be accessible at:
   ```
   http://localhost:5000
   ```

## Platform-Specific Notes

### Windows

- Make sure you have Visual C++ Redistributable installed
- Some anti-virus software may flag PyInstaller-generated executables

### macOS

- You may need to grant permissions for screen recording and accessibility
- On newer macOS versions, you may need to allow the app in Security & Privacy settings

### Linux

- X server access is required for screen capture and input control
- You may need to install additional system dependencies:
  ```
  sudo apt-get install python3-tk python3-dev scrot
  ```

## Need More Help?

If you continue experiencing issues with building or running the executable, refer to:

1. PyInstaller documentation: https://pyinstaller.org/en/stable/
2. Flask deployment guide: https://flask.palletsprojects.com/en/2.0.x/deploying/
3. PC Automation System GitHub repository (if available)
4. The included README.md file