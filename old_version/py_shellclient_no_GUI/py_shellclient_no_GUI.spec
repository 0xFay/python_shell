# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['py_shellclient_no_GUI.py'],
             pathex=['D:\\项目\\python_shell\\py_shellclient_no_GUI'],
             binaries=[],
             datas=[],
             hiddenimports=['win32api'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='py_shellclient_no_GUI',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True )
