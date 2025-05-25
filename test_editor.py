import sys
import os
from PyQt5.QtWidgets import QApplication
from src.ui.main_window import MainWindow

def test_editor():
    # Create the application
    app = QApplication(sys.argv)
    
    # Create the main window
    window = MainWindow()
    
    # Set the window size and position
    window.setGeometry(100, 100, 1200, 800)
    
    # Show the window
    window.show()
    
    # Open test files
    test_dir = os.path.join(os.path.dirname(__file__), 'test_files')
    test_files = [
        os.path.join(test_dir, 'test.py'),
        os.path.join(test_dir, 'test.html'),
        os.path.join(test_dir, 'test.js')
    ]
    
    for file_path in test_files:
        if os.path.exists(file_path):
            window.open_file_by_path(file_path)
    
    # Run the application
    sys.exit(app.exec_())

if __name__ == '__main__':
    test_editor() 