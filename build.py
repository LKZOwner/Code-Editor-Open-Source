import PyInstaller.__main__
import os

def build_exe():
    # Get the current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Define the paths
    main_script = os.path.join(current_dir, 'src', 'main.py')
    icon_path = os.path.join(current_dir, 'resources', 'icon.ico')
    
    # PyInstaller arguments
    args = [
        main_script,
        '--name=CodeEditor',
        '--onefile',
        '--windowed',
        '--clean',
        '--add-data=src;src',
        '--hidden-import=PyQt5',
        '--hidden-import=pygments',
    ]
    
    # Add icon if it exists
    if os.path.exists(icon_path):
        args.append(f'--icon={icon_path}')
    
    # Run PyInstaller
    PyInstaller.__main__.run(args)

if __name__ == '__main__':
    build_exe() 