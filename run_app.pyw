"""
VietDub Desktop Launcher
Final stable version - direct Streamlit CLI call
"""
import sys
import os
import webbrowser
import time
import socket
import threading

def get_app_folder():
    """Get folder where VietDub.exe is located"""
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
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
    try:
        # Import Streamlit's CLI directly
        from streamlit.web import cli as stcli
        
        # Set sys.argv as if running from command line
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
        
        # Run Streamlit
        stcli.main()
        
    except SystemExit:
        pass  # Streamlit calls sys.exit on shutdown
    except Exception as e:
        # Log error for debugging
        error_log = os.path.join(get_app_folder(), 'vietdub_error.log')
        with open(error_log, 'w') as f:
            f.write(f"Streamlit error: {str(e)}\n")
            import traceback
            f.write(traceback.format_exc())

def show_error(message):
    """Show error message box on Windows"""
    try:
        import ctypes
        ctypes.windll.user32.MessageBoxW(0, message, "VietDub - Lỗi", 0x10)
    except:
        pass

def main():
    # Setup
    app_folder = get_app_folder()
    os.chdir(app_folder)
    
    app_py = os.path.join(app_folder, 'app.py')
    port = 8501
    url = f"http://localhost:{port}"
    
    # Check if app.py exists
    if not os.path.exists(app_py):
        show_error(f"Không tìm thấy file app.py tại:\n{app_py}")
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
    
    # Wait for server to be ready
    if wait_for_server(port, timeout=120):
        # Open browser
        webbrowser.open(url)
        
        # Keep app running until thread dies
        try:
            while server_thread.is_alive():
                time.sleep(1)
        except KeyboardInterrupt:
            pass
    else:
        show_error(
            "Không thể khởi động server.\n\n"
            "Vui lòng kiểm tra file vietdub_error.log trong thư mục cài đặt."
        )

if __name__ == '__main__':
    main()
