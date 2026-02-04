# -*- mode: python ; coding: utf-8 -*-
"""
VietDub PyInstaller Spec File
Build: pyinstaller visub.spec --noconfirm
"""

import sys
import os
from PyInstaller.utils.hooks import collect_data_files, collect_submodules, copy_metadata

block_cipher = None

# === DATA FILES ===
datas = [
    ('app.py', '.'),
    ('config.py', '.'),
    ('core', 'core'),
    ('utils', 'utils'),
    ('components', 'components'),
]

# Collect package data
datas += collect_data_files('streamlit')
datas += collect_data_files('altair')
datas += collect_data_files('pydeck')
datas += collect_data_files('moviepy')
datas += collect_data_files('imageio')
datas += collect_data_files('imageio_ffmpeg')

# CRITICAL: Copy metadata for packages that need it
datas += copy_metadata('streamlit')
datas += copy_metadata('altair')
datas += copy_metadata('pandas')
datas += copy_metadata('numpy')
datas += copy_metadata('pydeck')
datas += copy_metadata('validators')
datas += copy_metadata('packaging')
datas += copy_metadata('importlib_metadata')
datas += copy_metadata('imageio')
datas += copy_metadata('imageio_ffmpeg')
datas += copy_metadata('moviepy')
datas += copy_metadata('decorator')
datas += copy_metadata('tqdm')
datas += copy_metadata('proglog')

# === HIDDEN IMPORTS ===
hiddenimports = [
    # Streamlit core
    'streamlit',
    'streamlit.web.cli',
    'streamlit.web.bootstrap',
    'streamlit.runtime.scriptrunner',
    'streamlit.runtime.caching',
    'streamlit.components.v1',
    
    # Streamlit dependencies  
    'altair',
    'validators',
    'pydeck',
    'watchdog',
    'watchdog.observers',
    'watchdog.events',
    'tornado',
    'tornado.web',
    'tornado.websocket',
    
    # Data/ML
    'pandas',
    'numpy',
    'PIL',
    'PIL.Image',
    
    # Whisper & Torch
    'whisper',
    'torch',
    'torchaudio',
    'numba',
    'llvmlite',
    
    # Media
    'moviepy',
    'moviepy.editor',
    'pydub',
    'ffmpeg',
    'yt_dlp',
    
    # Network
    'requests',
    'urllib3',
    
    # Packaging (required by streamlit)
    'packaging',
    'packaging.version',
    'packaging.specifiers',
    'packaging.requirements',
    'importlib_metadata',
]

# Add all submodules
hiddenimports += collect_submodules('streamlit')
hiddenimports += collect_submodules('altair')
hiddenimports += collect_submodules('tornado')
hiddenimports += collect_submodules('moviepy')
hiddenimports += collect_submodules('imageio')
hiddenimports += collect_submodules('imageio_ffmpeg')

# === ANALYSIS ===
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
        'IPython',
        'jupyter',
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
    console=False,  # NO CONSOLE WINDOW
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
