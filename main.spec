# -*- mode: python -*-
 
block_cipher = None
 
 
a = Analysis(['main.py','resources_rc.py','customnWidget.py','main_ui.py','publicFunc.py','publicThread.py','updateFileForm_ui.py'],
             pathex=[''],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
       

#######!!!注意点1：加载自己的资源文件#####################
def extra_datas(mydir):
    def rec_glob(p, files):
        import os
        import glob
        for d in glob.glob(p):
            if os.path.isfile(d):
                files.append(d)
            rec_glob("%s/*" % d, files)
    files = []
    rec_glob("%s/*" % mydir, files)
    extra_datas = []
    for f in files:
        file_name = os.path.basename(f)
        extra_datas.append((f, f, 'DATA'))
 
    return extra_datas
# append the 'Resources' dir
a.datas += extra_datas('assets')  ###这里是自己的资源文件夹   
a.datas += extra_datas('文件范例')  ###这里是自己的资源文件夹 
a.datas += extra_datas('data')  ###这里是自己的资源文件夹



################################################
       
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
 
exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='传输网智能诊断工具',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='.\\assets\\main.ico'
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='传输网智能诊断工具',
)
