# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['index.py'],
    pathex=[],
    binaries=[],
    datas=[('/Library/Frameworks/Python.framework/Versions/3.11/lib/python3.11/site-packages/eel/eel.js', 'eel'), ('static', 'static')],
    hiddenimports=['bottle_websocket'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='index',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['icon.ico'],
)
app = BUNDLE(
    exe,
    name='index.app',
    icon='icon.ico',
    bundle_identifier=None,
)
