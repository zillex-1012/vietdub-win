"""
VietDub Desktop Launcher
Runs Streamlit in MAIN thread (required for signal handlers)
Opens browser from background thread
"""
import sys
import os
import webbrowser
import time
import threading
import urllib.request

def get_app_folder():
    """Get folder where app.py is located"""
    if getattr(sys, 'frozen', False):
        return sys._MEIPASS
    return os.path.dirname(os.path.abspath(__file__))

def server_ready(port):
    """Check if Streamlit server is ready via HTTP health check"""
    try:
        url = f"http://localhost:{port}/_stcore/health"
        response = urllib.request.urlopen(url, timeout=2)
        return response.status == 200
    except:
        return False

def open_browser_when_ready(port, url):
    """Background thread: wait for server and open browser"""
    for _ in range(45):  # Max 90 seconds
        if server_ready(port):
            webbrowser.open(url)
            return
        time.sleep(2)
    
    # Timeout - show error
    try:
        import ctypes
        ctypes.windll.user32.MessageBoxW(
            0, 
            "Server không khởi động được sau 90 giây.", 
            "VietDub - Timeout", 
            0x10
        )
    except:
        pass

def show_error(message):
    """Show error message box"""
    try:
        import ctypes
        ctypes.windll.user32.MessageBoxW(0, message, "VietDub - Lỗi", 0x10)
    except:
        print(f"Error: {message}")

def main():
    app_folder = get_app_folder()
    os.chdir(app_folder)
    
    app_py = os.path.join(app_folder, 'app.py')
    port = 8501
    url = f"http://localhost:{port}"
    
    # Check app.py exists
    if not os.path.exists(app_py):
        show_error(f"Không tìm thấy file app.py!\n\nĐường dẫn: {app_py}")
        return
    
    # Set environment
    os.environ['STREAMLIT_SERVER_PORT'] = str(port)
    os.environ['STREAMLIT_SERVER_HEADLESS'] = 'true'
    os.environ['STREAMLIT_BROWSER_GATHER_USAGE_STATS'] = 'false'
    os.environ['STREAMLIT_BROWSER_SERVER_ADDRESS'] = 'localhost'
    
    # Start browser opener in BACKGROUND thread
    browser_thread = threading.Thread(
        target=open_browser_when_ready,
        args=(port, url),
        daemon=True
    )
    browser_thread.start()
    
    # Run Streamlit in MAIN thread (required for signal handlers)
    try:
        from streamlit.web import cli as stcli
        
        sys.argv = [
            'streamlit', 'run', app_py,
            '--server.port', str(port),
            '--server.headless', 'true',
            '--browser.gatherUsageStats', 'false',
            '--browser.serverAddress', 'localhost',
            '--global.developmentMode', 'false',
        ]
        
        stcli.main()
        
    except Exception as e:
        show_error(f"Lỗi khởi động Streamlit:\n\n{type(e).__name__}: {str(e)}")

if __name__ == '__main__':
    main()
