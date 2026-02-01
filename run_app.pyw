"""
VietDub Desktop Launcher
Simple, stable approach - launches Streamlit and opens browser
No console window, no pywebview complexity
"""
import subprocess
import sys
import os
import webbrowser
import time
import socket

def get_base_path():
    """Get the application base path"""
    if getattr(sys, 'frozen', False):
        return sys._MEIPASS  # PyInstaller temp folder
    return os.path.dirname(os.path.abspath(__file__))

def get_app_path():
    """Get the folder where exe is located (for app.py)"""
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))

def wait_for_server(port, timeout=120):
    """Wait for Streamlit server to start"""
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex(('127.0.0.1', port))
            sock.close()
            if result == 0:
                return True
        except:
            pass
        time.sleep(1)
    return False

def main():
    # Setup paths
    app_folder = get_app_path()
    os.chdir(app_folder)
    
    app_py = os.path.join(app_folder, 'app.py')
    port = 8501
    url = f"http://localhost:{port}"
    
    # Environment
    env = os.environ.copy()
    env['STREAMLIT_SERVER_PORT'] = str(port)
    env['STREAMLIT_SERVER_HEADLESS'] = 'true'
    env['STREAMLIT_BROWSER_GATHER_USAGE_STATS'] = 'false'
    env['STREAMLIT_BROWSER_SERVER_ADDRESS'] = 'localhost'
    
    # Hide console on Windows
    startupinfo = None
    creationflags = 0
    if sys.platform == 'win32':
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        startupinfo.wShowWindow = subprocess.SW_HIDE
        creationflags = subprocess.CREATE_NO_WINDOW
    
    # Launch Streamlit using the bundled streamlit module directly
    # We use runpy to run streamlit as a module
    import runpy
    import threading
    
    def run_streamlit():
        sys.argv = [
            'streamlit', 'run', app_py,
            '--server.port', str(port),
            '--server.headless', 'true',
            '--browser.gatherUsageStats', 'false',
            '--browser.serverAddress', 'localhost',
            '--global.developmentMode', 'false',
        ]
        try:
            runpy.run_module('streamlit', run_name='__main__', alter_sys=True)
        except SystemExit:
            pass
    
    # Start Streamlit in background thread
    t = threading.Thread(target=run_streamlit, daemon=True)
    t.start()
    
    # Wait for server and open browser
    if wait_for_server(port, timeout=120):
        webbrowser.open(url)
        # Keep app running
        try:
            while t.is_alive():
                time.sleep(1)
        except KeyboardInterrupt:
            pass
    else:
        # Show error on Windows
        if sys.platform == 'win32':
            import ctypes
            ctypes.windll.user32.MessageBoxW(
                0, 
                "Không thể khởi động server. Vui lòng thử lại hoặc liên hệ hỗ trợ.",
                "VietDub - Lỗi", 
                0x10  # MB_ICONERROR
            )

if __name__ == '__main__':
    main()
