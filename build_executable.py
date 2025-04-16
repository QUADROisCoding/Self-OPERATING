#!/usr/bin/env python3
"""
Build script for creating standalone executables of the PC Automation System.
This script uses PyInstaller to package the application into a single executable file.
"""

import os
import sys
import shutil
import platform
import subprocess
from pathlib import Path

def detect_os():
    """Detect the operating system and return the appropriate settings"""
    system = platform.system().lower()
    
    if system == 'windows':
        return {
            'name': 'Windows',
            'exe_ext': '.exe',
            'icon': 'icon.ico',
            'add_args': []
        }
    elif system == 'darwin':
        return {
            'name': 'macOS',
            'exe_ext': '.app',
            'icon': 'icon.icns',
            'add_args': ['--target-architecture', 'universal2']
        }
    elif system == 'linux':
        return {
            'name': 'Linux',
            'exe_ext': '',
            'icon': 'icon.png',
            'add_args': []
        }
    else:
        print(f"Unsupported OS: {system}")
        sys.exit(1)

def check_requirements():
    """Check if the required dependencies are installed"""
    try:
        import PyInstaller
        print("PyInstaller is installed.")
    except ImportError:
        print("PyInstaller is not installed. Installing...")
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pyinstaller'])
            print("PyInstaller has been installed.")
        except Exception as e:
            print(f"Failed to install PyInstaller automatically: {e}")
            print("\nPlease install PyInstaller manually with the command:")
            print("pip install pyinstaller")
            sys.exit(1)

def build_executable():
    """Build the executable file"""
    os_info = detect_os()
    print(f"Building executable for {os_info['name']}...")
    
    # Ensure dist directory exists and is empty
    dist_dir = Path('dist')
    if dist_dir.exists():
        shutil.rmtree(dist_dir)
    dist_dir.mkdir(exist_ok=True)
    
    # Application name
    app_name = "PC_Automation_System"
    
    # Check if icon exists, create a placeholder if it doesn't
    icon_path = Path(os_info['icon'])
    if not icon_path.exists():
        print(f"Icon file {icon_path} not found. Creating placeholder...")
        # For Windows, create a placeholder icon
        if os_info['name'] == 'Windows':
            with open('icon.ico', 'wb') as f:
                # You would need a real icon file here
                f.write(b'Placeholder for icon file')
    
    # Use Python module approach for PyInstaller - this is more reliable
    print("Using Python module approach for PyInstaller (python -m PyInstaller)")
    
    # Build the command
    cmd = [
        sys.executable,
        '-m',
        'PyInstaller',
        '--onefile',
        '--windowed',
        '--name', app_name,
        '--noconfirm',
        '--clean',
    ]
    
    # Add icon if it exists
    if icon_path.exists():
        cmd.extend(['--icon', str(icon_path)])
    
    # Add OS-specific arguments
    cmd.extend(os_info['add_args'])
    
    # Add the main script
    cmd.append('app.py')
    
    print(f"Running command: {' '.join(str(c) for c in cmd)}")
    
    # Execute the command
    try:
        subprocess.check_call(cmd)
    except Exception as e:
        print(f"\nError running PyInstaller: {e}")
        print("\nHere are some troubleshooting steps:")
        print("1. Make sure PyInstaller is installed: pip install pyinstaller")
        print("2. Try running PyInstaller directly: python -m PyInstaller --onefile --windowed app.py")
        print("3. Check the EXECUTABLE_BUILD.md file for more detailed instructions")
        print("\nOR use the alternative method without building an executable:")
        print("python run_without_executable.py")
        sys.exit(1)
    
    # Output the result
    exe_path = dist_dir / f"{app_name}{os_info['exe_ext']}"
    if exe_path.exists():
        print(f"\nBuild successful! Executable created at: {exe_path}")
        print(f"Size: {exe_path.stat().st_size / (1024*1024):.2f} MB")
    else:
        print(f"\nBuild failed. Executable not found at expected path: {exe_path}")
        sys.exit(1)
    
    return exe_path

def create_distribution_package(exe_path):
    """Create a distribution package for the executable"""
    os_info = detect_os()
    
    # Create a distribution directory
    dist_pkg_dir = Path('dist_package')
    if dist_pkg_dir.exists():
        shutil.rmtree(dist_pkg_dir)
    dist_pkg_dir.mkdir(exist_ok=True)
    
    # Copy the executable
    dest_path = dist_pkg_dir / exe_path.name
    shutil.copy2(exe_path, dest_path)
    
    # Copy run_without_executable.py script
    if Path('run_without_executable.py').exists():
        shutil.copy2('run_without_executable.py', dist_pkg_dir)
    
    # Copy README and other documentation
    for doc_file in ['README.md', 'LICENSE', 'EXECUTABLE_BUILD.md']:
        if Path(doc_file).exists():
            shutil.copy2(doc_file, dist_pkg_dir)
    
    # Create a quick start guide
    with open(dist_pkg_dir / 'QUICK_START.txt', 'w') as f:
        f.write(f"""PC Automation System - Quick Start Guide
=======================================

Method 1: Using the Executable
-----------------------------
1. Run the executable: {exe_path.name}
2. Allow any permissions requested by your OS
3. Open your browser and go to: http://localhost:5000
4. Use the web interface to control your PC

Method 2: Running Without Executable (If Method 1 Fails)
-------------------------------------------------------
1. Make sure Python 3.6+ is installed on your system
2. Open a command prompt or terminal
3. Navigate to the directory containing these files
4. Run: python run_without_executable.py
5. The script will install dependencies and start the app automatically

For more troubleshooting information, see EXECUTABLE_BUILD.md
""")
    
    print(f"\nDistribution package created in: {dist_pkg_dir}")

if __name__ == "__main__":
    print("PC Automation System - Executable Builder")
    print("=========================================")
    
    check_requirements()
    exe_path = build_executable()
    create_distribution_package(exe_path)
    
    print("\nDone! The standalone executable is ready to be distributed.")
    print("Users can run it without installing any dependencies.")