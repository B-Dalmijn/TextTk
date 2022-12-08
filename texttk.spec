import os
import sys
sys.setrecursionlimit(5000)
from PyInstaller.utils.hooks import collect_data_files, collect_dynamic_libs # this is very helpful

__here__ = os.getcwd()
env_path = os.path.dirname(sys.executable)
dlls = os.path.join(env_path, 'DLLs')

paths = [
    __here__,
    env_path,
    dlls,
]

block_cipher = None

a = Analysis(
    ['src/texttk/main.py'],
    pathex=[f"{__here__}\\src\\texttk", dlls],
    binaries=[],
    datas=[("src/texttk/resources","resources")],
    hiddenimports=[],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False
    )
pyz = PYZ(
    a.pure,
    a.zipped_data,
    cipher=block_cipher
    )
exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='TextTk',
    icon='src/texttk/resources/icon.ico',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False
    )
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=False,
    upx_exclude=[],
    name='TextTk'
    )