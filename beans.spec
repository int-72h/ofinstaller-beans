# -*- mode: python ; coding: utf-8 -*-


block_cipher = None

import os
from platform import system
import glob

def data_generator():
    datas = []
    datas.append(('Binaries/ca-certificates.crt', '.'))
    if system() == 'Windows':
        datas.append(('Binaries/butler.exe', '.'))
        datas.append(('Binaries/aria2c.exe', '.'))
        datas.append(('Binaries/ca-certificates.crt', '.'))
    else:
        datas.append(('Binaries/butler', '.'))
        datas.append(('Binaries/aria2c', '.'))
        datas.append(('Binaries/ca-certificates.crt', '.'))

    for p in glob.iglob("locale/**/*.mo", recursive=True):
        datas.append((p,os.path.dirname(p)))

    return datas

a = Analysis(
    ['beans.py'],
    pathex=[],
    binaries=[],
    datas=data_generator(),
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['matplotlib', 'jedi', 'numpy', 'babel', 'typeshed'],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='beans',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    uac_admin=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='beans.ico',
)
