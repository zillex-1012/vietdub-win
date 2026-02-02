"""
VietDub Desktop Launcher
Final stable version - shows errors directly in message box
"""
import sys
import os
import webbrowser
import time
import socket
import threading
import traceback

# Global variable to capture error
startup_error = None

def get_app_folder():
    """Get folder where app.py is located (PyInstaller extracts to _MEIPASS)"""
    if getattr(sys, 'frozen', False):
        # PyInstaller extracts bundled files to this temp folder
        return sys._MEIPASS
    return os.path.dirname(os.path.abspath(__file__))

def wait_for_server(port, timeout=120):
    """Wait for Streamlit server to start"""
    start = time.time()
    while time.time() - start < timeout:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            if sock.connect_ex(('127.0.0.1', port)) == 0:
                sock.close()
                return True
            sock.close()
        except:
            pass
        time.sleep(1)
    return False

def run_streamlit_server(app_path, port):
    """Run Streamlit server in current thread"""
    global startup_error
    try:
        from streamlit.web import cli as stcli
        
        sys.argv = [
            'streamlit', 'run', app_path,
            '--server.port', str(port),
            '--server.headless', 'true',
            '--browser.gatherUsageStats', 'false',
            '--browser.serverAddress', 'localhost',
            '--global.developmentMode', 'false',
            '--server.enableCORS', 'false',
            '--server.enableXsrfProtection', 'false',
        ]
        
        stcli.main()
        
    except SystemExit:
        pass
    except Exception as e:
        startup_error = f"{type(e).__name__}: {str(e)}\n\n{traceback.format_exc()}"

def show_message(title, message, is_error=True):
    """Show message box on Windows"""
    try:
        import ctypes
        icon = 0x10 if is_error else 0x40
        ctypes.windll.user32.MessageBoxW(0, message, title, icon)
    except:
        print(f"{title}: {message}")

def main():
    global startup_error
    
    app_folder = get_app_folder()
    os.chdir(app_folder)
    
    app_py = os.path.join(app_folder, 'app.py')
    port = 8501
    url = f"http://localhost:{port}"
    
    # Check app.py exists
    if not os.path.exists(app_py):
        show_message("VietDub - Lỗi", f"Không tìm thấy file app.py!\n\nĐường dẫn: {app_py}")
        return
    
    # Set environment
    os.environ['STREAMLIT_SERVER_PORT'] = str(port)
    os.environ['STREAMLIT_SERVER_HEADLESS'] = 'true'
    os.environ['STREAMLIT_BROWSER_GATHER_USAGE_STATS'] = 'false'
    
    # Start Streamlit in background thread
    server_thread = threading.Thread(
        target=run_streamlit_server, 
        args=(app_py, port),
        daemon=True
    )
    server_thread.start()
    
    # Wait for server (max 60 seconds, check error every 5 seconds)
    waited = 0
    while waited < 60:
        if startup_error:
            show_message("VietDub - Lỗi khởi động", startup_error)
            return
        
        if wait_for_server(port, timeout=5):
            webbrowser.open(url)
            try:
                while server_thread.is_alive():
                    time.sleep(1)
            except KeyboardInterrupt:
                pass
            return
        
        waited += 5
    
    # Timeout - show error
    error_msg = "Không thể khởi động server sau 60 giây.\n\n"
    if startup_error:
        error_msg += startup_error
    else:
        error_msg += "Server không phản hồi. Vui lòng thử khởi động lại."
    
    show_message("VietDub - Lỗi", error_msg)

if __name__ == '__main__':
    main()
