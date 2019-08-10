# -*- mode: python ; coding: utf-8 -*-

import sys

sys.setrecursionlimit(5000)

block_cipher = None

a = Analysis(['iftd_monitor.py',
              'DataConnection.py',
              'forzen_dir.py',
              'iftd_monitor_view.py',
              'para_info.py',
              'setting_dialog.py'],
             pathex=['E:\\IFTD_MONITOR\\src_code'],
             binaries=[],
             datas=[('E:\\IFTD_MONITOR\\src_code\\icons', 'icons')],
             hiddenimports=[],
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
          [],
          exclude_binaries=True,
          name='iftd_monitor',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='iftd_monitor')
