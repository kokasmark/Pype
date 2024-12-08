# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['Test\\app.py'],
    pathex=['C:\\Users\\met4y\\Desktop\\Pype'],
    binaries=[],
    datas=[('Test\\frontend', 'frontend'), ('Test\\frontend\\assets', 'assets')],
    hiddenimports=['pkg_resources', 'pkg_resources.extern'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [('-OO', None, 'OPTION')],
    name='app',
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
    icon=['Test\\frontend\\favicon.ico'],
)
