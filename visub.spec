# -*- mode: python ; coding: utf-8 -*-
"""
VietDub PyInstaller Spec File
Build command: pyinstaller visub.spec --noconfirm
"""

import sys
import os
from PyInstaller.utils.hooks import collect_data_files, collect_submodules, copy_metadata

block_cipher = None

# Collect all necessary data files
datas = [
    ('app.py', '.'),
    ('config.py', '.'),
    ('core', 'core'),
    ('utils', 'utils'),
    ('components', 'components'),
]

# Collect hidden imports for complex packages
hiddenimports = [
    # GUI Wrapper
    'webview',
    'clr',
    'System.Windows.Forms',
    'System.Threading',
    
    # Streamlit and its dependencies
    'streamlit',
    'streamlit.web.cli',
    'streamlit.runtime.scriptrunner',
    'streamlit.web.bootstrap',
    'altair',
    'validators',
    'gitpython',
    'pydeck',
    'watchdog',
    
    # Whisper and ML
    'whisper',
    'torch',
    'torchaudio',
    'numpy',
    'numba',
    'llvmlite',
    
    # Media processing
    'moviepy',
    'moviepy.editor',
    'moviepy.video.io.VideoFileClip',
    'moviepy.audio.io.AudioFileClip',
    'pydub',
    'ffmpeg',
    
    # Networking
    'requests',
    'urllib3',
    'yt_dlp',
    
    # Data handling
    'pandas',
    'PIL',
    'PIL.Image',
]

# Add all streamlit submodules
hiddenimports += collect_submodules('streamlit')
hiddenimports += collect_submodules('altair')

# Collect data files from packages
datas += collect_data_files('streamlit')
datas += collect_data_files('altair')
datas += collect_data_files('webview')
datas += copy_metadata('streamlit')

a = Analysis(
    ['run_app.pyw'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'matplotlib',
        'tkinter',
        'PyQt5',
        'PySide2',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='VietDub',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,  # No console window!
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='assets/icon.ico' if os.path.exists('assets/icon.ico') else None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='VietDub',
)
