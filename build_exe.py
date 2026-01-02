import PyInstaller.__main__
import shutil
import os

def build():
    # clean previous
    if os.path.exists('dist'): shutil.rmtree('dist')
    if os.path.exists('build'): shutil.rmtree('build')

    print("Building ProjectK.exe...")
    
    PyInstaller.__main__.run([
        'ProjectK.py',
        '--name=ProjectK',
        '--onefile',
        '--noconsole',
        '--collect-all=customtkinter',
        '--clean',
    ])
    
    print("Build complete. Check 'dist' folder.")

if __name__ == "__main__":
    build()
