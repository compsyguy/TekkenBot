# -*- mode: python -*-

block_cipher = None


a = Analysis(['name', 'TekkenBotPrime', 'GUI_TekkenBotPrime.py'],
             pathex=['C:\\Users\\Evan\\Downloads\\tekken\\TekkenBot-master2\\TekkenBot-master'],
             binaries=[],
             datas=[('TekkenData', 'TekkenData')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='name',
          debug=False,
          strip=False,
          upx=True,
          console=False , icon='TekkenData\\tekken_bot.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='name')
