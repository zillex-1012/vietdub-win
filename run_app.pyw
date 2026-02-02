"""
VietDub Desktop Launcher
Uses HTTP health check for reliable server detection
"""
import sys
import os
import webbrowser
import time
import threading
import traceback
import urllib.request
import urllib.error

# Global variable to capture error
startup_error = None

def get_app_folder():
    """Get folder where app.py is located"""
    if getattr(sys, 'frozen', False):
        return sys._MEIPASS
    return os.path.dirname(os.path.abspath(__file__))

def server_ready(port):
    """Check if Streamlit server is actually ready via HTTP health check"""
    try:
        url = f"http://localhost:{port}/_stcore/health"
        response = urllib.request.urlopen(url, timeout=2)
        return response.status == 200
    except:
        return False

def run_streamlit_server(app_path, port):
    """Run Streamlit server"""
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
        ]
        
        stcli.main()
        
    except SystemExit as e:
        if e.code != 0:
            startup_error = f"Streamlit exited with code {e.code}"
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
    
    # Wait for server using HTTP health check (max 90 seconds)
    for i in range(45):  # 45 attempts x 2 seconds = 90 seconds max
        # Check for startup error
        if startup_error:
            show_message("VietDub - Lỗi khởi động", startup_error)
            return
        
        # Check if thread died unexpectedly
        if not server_thread.is_alive():
            error_msg = startup_error if startup_error else "Server stopped unexpectedly"
            show_message("VietDub - Lỗi", error_msg)
            return
        
        # HTTP health check - confirms server is ACTUALLY ready
        if server_ready(port):
            webbrowser.open(url)
            
            # Keep app running
            try:
                while server_thread.is_alive():
                    time.sleep(1)
            except KeyboardInterrupt:
                pass
            return
        
        time.sleep(2)  # Check every 2 seconds
    
    # Timeout
    error_msg = "Server không khởi động được sau 90 giây.\n\n"
    if startup_error:
        error_msg += startup_error
    show_message("VietDub - Timeout", error_msg)

if __name__ == '__main__':
    main()
