"""
VietDub Desktop Launcher
Entry point for PyInstaller - runs Streamlit app without console window

This file uses .pyw extension to suppress console on Windows.
PyInstaller will compile this into run_app.exe
"""
import subprocess
import sys
import os
import webbrowser
import time
import socket

def find_free_port():
    """Find a free port to run Streamlit on"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return s.getsockname()[1]

def get_base_path():
    """Get the base path for the application (works for both dev and frozen)"""
    if getattr(sys, 'frozen', False):
        # Running as compiled executable
        return os.path.dirname(sys.executable)
    else:
        # Running as script
        return os.path.dirname(os.path.abspath(__file__))

def main():
    base_path = get_base_path()
    os.chdir(base_path)
    
    # Find free port
    port = find_free_port()
    url = f"http://localhost:{port}"
    
    # Set environment to prevent Streamlit welcome message
    env = os.environ.copy()
    env['STREAMLIT_BROWSER_GATHER_USAGE_STATS'] = 'false'
    env['STREAMLIT_SERVER_HEADLESS'] = 'true'
    env['STREAMLIT_SERVER_PORT'] = str(port)
    
    # Path to app.py
    app_path = os.path.join(base_path, 'app.py')
    
    # Determine python executable
    if getattr(sys, 'frozen', False):
        # When frozen, use the bundled Python
        python_exe = os.path.join(base_path, 'python.exe')
        if not os.path.exists(python_exe):
            python_exe = sys.executable
    else:
        python_exe = sys.executable
    
    # Launch Streamlit
    # CREATE_NO_WINDOW flag (0x08000000) hides the console
    CREATE_NO_WINDOW = 0x08000000
    
    process = subprocess.Popen(
        [python_exe, '-m', 'streamlit', 'run', app_path,
         f'--server.port={port}',
         '--server.headless=true',
         '--browser.gatherUsageStats=false',
         '--global.developmentMode=false'],
        env=env,
        creationflags=CREATE_NO_WINDOW if sys.platform == 'win32' else 0,
        cwd=base_path,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    
    # Wait a moment then open browser
    time.sleep(2)
    webbrowser.open(url)
    
    # Keep the process running
    try:
        process.wait()
    except KeyboardInterrupt:
        process.terminate()

if __name__ == '__main__':
    main()
