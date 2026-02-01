"""
VietDub Desktop Launcher
Entry point for PyInstaller - runs Streamlit app inside a native window using pywebview
"""
import sys
import os
import socket
import threading
import time
import webview
from streamlit.web.cli import main as st_cli

def find_free_port():
    """Find a free port to run Streamlit on"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return s.getsockname()[1]

def get_base_path():
    """Get the base path for the application"""
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))

def start_streamlit(port, app_path):
    """Start Streamlit server in a separate thread"""
    sys.argv = [
        "streamlit",
        "run",
        app_path,
        f"--server.port={port}",
        "--server.headless=true",
        "--browser.gatherUsageStats=false",
        "--global.developmentMode=false",
        "--server.connnectionless=true"
    ]
    # Suppress stdout/stderr
    sys.stdout = open(os.devnull, 'w')
    sys.stderr = open(os.devnull, 'w')
    
    st_cli()

def wait_for_server(port, timeout=30):
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
        time.sleep(0.5)
    return False

def main():
    base_path = get_base_path()
    os.chdir(base_path)
    app_path = os.path.join(base_path, 'app.py')
    
    # Use dynamic port
    port = find_free_port()
    url = f"http://127.0.0.1:{port}"
    
    # Start Streamlit in a thread
    t = threading.Thread(target=start_streamlit, args=(port, app_path))
    t.daemon = True
    t.start()
    
    # Wait for server
    if wait_for_server(port):
        # Create native window
        webview.create_window(
            "VietDub - AI Video Dubbing",
            url=url,
            width=1280,
            height=800,
            resizable=True,
            confirm_close=True
        )
        # Start webview GUI
        webview.start(private_mode=False)
    else:
        # Fallback or error handling
        import ctypes
        ctypes.windll.user32.MessageBoxW(0, "Failed to start Streamlit server", "Error", 0)

if __name__ == '__main__':
    main()
