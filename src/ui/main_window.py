from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                           QPushButton, QLabel, QMessageBox, QMenu, QAction,
                           QFileDialog, QTabWidget, QSplitter, QToolBar,
                           QStatusBar, QTreeView, QFileSystemModel, QDialog,
                           QLineEdit, QCheckBox, QComboBox, QTextEdit, QScrollBar)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon, QFont, QKeySequence, QSyntaxHighlighter, QTextCharFormat, QColor
import os
import re
from pygments import highlight
from pygments.lexers import get_lexer_by_name, guess_lexer
from pygments.formatters import get_formatter_by_name

class CodeHighlighter(QSyntaxHighlighter):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.highlighting_rules = []
        self.setup_rules()

    def setup_rules(self):
        # Common keywords for multiple languages
        keywords = {
            'python': [
                "and", "as", "assert", "break", "class", "continue", "def",
                "del", "elif", "else", "except", "False", "finally", "for",
                "from", "global", "if", "import", "in", "is", "lambda", "None",
                "nonlocal", "not", "or", "pass", "raise", "return", "True",
                "try", "while", "with", "yield"
            ],
            'javascript': [
                "break", "case", "catch", "class", "const", "continue", "debugger",
                "default", "delete", "do", "else", "export", "extends", "finally",
                "for", "function", "if", "import", "in", "instanceof", "new", "return",
                "super", "switch", "this", "throw", "try", "typeof", "var", "void",
                "while", "with", "yield"
            ],
            'html': [
                "html", "head", "body", "div", "span", "p", "a", "img", "script",
                "style", "link", "meta", "title", "h1", "h2", "h3", "h4", "h5", "h6"
            ]
        }

        # Set up colors with brighter colors for better visibility on black
        keyword_format = QTextCharFormat()
        keyword_format.setForeground(QColor("#569CD6"))  # Bright blue for keywords

        string_format = QTextCharFormat()
        string_format.setForeground(QColor("#CE9178"))  # Bright orange for strings

        comment_format = QTextCharFormat()
        comment_format.setForeground(QColor("#6A9955"))  # Bright green for comments

        number_format = QTextCharFormat()
        number_format.setForeground(QColor("#B5CEA8"))  # Bright light green for numbers

        # Add rules for each language
        for lang, lang_keywords in keywords.items():
            for word in lang_keywords:
                pattern = f"\\b{word}\\b"
                self.highlighting_rules.append((pattern, keyword_format))

        # Common patterns for all languages
        self.highlighting_rules.extend([
            ('".*"', string_format),  # Double quoted strings
            ("'.*'", string_format),  # Single quoted strings
            ("#.*", comment_format),  # Python comments
            ("//.*", comment_format),  # Single line comments
            ("/\\*.*\\*/", comment_format),  # Multi-line comments
            ("\\b\\d+\\b", number_format),  # Numbers
        ])

    def highlightBlock(self, text):
        for pattern, format in self.highlighting_rules:
            for match in re.finditer(pattern, text):
                start = match.start()
                length = match.end() - start
                self.setFormat(start, length, format)

class CodeEditor(QTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_editor()
        self.current_file = None
        self.highlighter = CodeHighlighter(self.document())
        self.setup_scroll_buttons()

    def setup_editor(self):
        # Set the default font
        font = QFont("Consolas", 10)
        self.setFont(font)
        
        # Set tab width
        self.setTabStopWidth(40)
        
        # Enable line wrap
        self.setLineWrapMode(QTextEdit.NoWrap)
        
        # Set dark gray theme colors
        self.setStyleSheet("""
            QTextEdit {
                background-color: #1E1E1E;
                color: #D4D4D4;
                border: none;
                selection-background-color: #264F78;
                selection-color: #FFFFFF;
            }
            QScrollBar:vertical {
                background-color: #1E1E1E;
                width: 14px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background-color: #424242;
                min-height: 20px;
                border-radius: 7px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #4F4F4F;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: none;
            }
        """)

    def setup_scroll_buttons(self):
        # Create scroll buttons
        self.scroll_up_btn = QPushButton("▲", self)
        self.scroll_down_btn = QPushButton("▼", self)
        
        # Style the buttons
        button_style = """
            QPushButton {
                background-color: #252526;
                color: #D4D4D4;
                border: 1px solid #333333;
                border-radius: 3px;
                padding: 2px;
                min-width: 20px;
                max-width: 20px;
                min-height: 20px;
                max-height: 20px;
            }
            QPushButton:hover {
                background-color: #2D2D2D;
            }
        """
        self.scroll_up_btn.setStyleSheet(button_style)
        self.scroll_down_btn.setStyleSheet(button_style)
        
        # Connect buttons to scroll functions
        self.scroll_up_btn.clicked.connect(self.scroll_up)
        self.scroll_down_btn.clicked.connect(self.scroll_down)
        
        # Position the buttons
        self.scroll_up_btn.move(self.width() - 25, 5)
        self.scroll_down_btn.move(self.width() - 25, self.height() - 25)
        
        # Show the buttons
        self.scroll_up_btn.show()
        self.scroll_down_btn.show()

    def scroll_up(self):
        self.verticalScrollBar().setValue(
            self.verticalScrollBar().value() - self.verticalScrollBar().singleStep()
        )

    def scroll_down(self):
        self.verticalScrollBar().setValue(
            self.verticalScrollBar().value() + self.verticalScrollBar().singleStep()
        )

    def resizeEvent(self, event):
        super().resizeEvent(event)
        # Update button positions when window is resized
        self.scroll_up_btn.move(self.width() - 25, 5)
        self.scroll_down_btn.move(self.width() - 25, self.height() - 25)

class FindDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Find")
        self.setModal(True)
        layout = QVBoxLayout(self)
        
        # Find text
        self.find_text = QLineEdit()
        layout.addWidget(self.find_text)
        
        # Options
        self.case_sensitive = QCheckBox("Case sensitive")
        self.whole_word = QCheckBox("Whole word")
        layout.addWidget(self.case_sensitive)
        layout.addWidget(self.whole_word)
        
        # Buttons
        button_layout = QHBoxLayout()
        self.find_button = QPushButton("Find")
        self.find_button.clicked.connect(self.accept)
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(self.find_button)
        button_layout.addWidget(self.cancel_button)
        layout.addLayout(button_layout)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle("Code Editor")
        self.setMinimumSize(1200, 800)
        
        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QHBoxLayout(central_widget)
        
        # Create file explorer
        self.file_explorer = QTreeView()
        self.file_model = QFileSystemModel()
        self.file_model.setRootPath("")
        self.file_explorer.setModel(self.file_model)
        self.file_explorer.setRootIndex(self.file_model.index(""))
        self.file_explorer.setMinimumWidth(200)
        self.file_explorer.clicked.connect(self.open_file)
        
        # Create editor area
        self.editor_tabs = QTabWidget()
        self.editor_tabs.setTabsClosable(True)
        self.editor_tabs.tabCloseRequested.connect(self.close_tab)
        
        # Create splitter
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(self.file_explorer)
        splitter.addWidget(self.editor_tabs)
        splitter.setStretchFactor(1, 1)
        layout.addWidget(splitter)
        
        # Create toolbar
        self.create_toolbar()
        
        # Create status bar
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.statusBar.showMessage("Ready")
        
        # Create menu bar
        self.create_menubar()
        
        # Setup keyboard shortcuts
        self.setup_shortcuts()
        
    def create_toolbar(self):
        toolbar = QToolBar()
        toolbar.setIconSize(QSize(16, 16))
        self.addToolBar(toolbar)
        
        # New file action
        new_action = QAction("New", self)
        new_action.triggered.connect(self.new_file)
        new_action.setShortcut(QKeySequence.New)
        toolbar.addAction(new_action)
        
        # Open file action
        open_action = QAction("Open", self)
        open_action.triggered.connect(self.open_file_dialog)
        open_action.setShortcut(QKeySequence.Open)
        toolbar.addAction(open_action)
        
        # Save file action
        save_action = QAction("Save", self)
        save_action.triggered.connect(self.save_file)
        save_action.setShortcut(QKeySequence.Save)
        toolbar.addAction(save_action)
        
        toolbar.addSeparator()
        
        # Cut action
        cut_action = QAction("Cut", self)
        cut_action.triggered.connect(self.cut)
        cut_action.setShortcut(QKeySequence.Cut)
        toolbar.addAction(cut_action)
        
        # Copy action
        copy_action = QAction("Copy", self)
        copy_action.triggered.connect(self.copy)
        copy_action.setShortcut(QKeySequence.Copy)
        toolbar.addAction(copy_action)
        
        # Paste action
        paste_action = QAction("Paste", self)
        paste_action.triggered.connect(self.paste)
        paste_action.setShortcut(QKeySequence.Paste)
        toolbar.addAction(paste_action)
        
        toolbar.addSeparator()
        
        # Find action
        find_action = QAction("Find", self)
        find_action.triggered.connect(self.show_find_dialog)
        find_action.setShortcut(QKeySequence.Find)
        toolbar.addAction(find_action)
        
        # Replace action
        replace_action = QAction("Replace", self)
        replace_action.triggered.connect(self.show_replace_dialog)
        replace_action.setShortcut(QKeySequence.Replace)
        toolbar.addAction(replace_action)
        
    def create_menubar(self):
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("File")
        
        new_action = QAction("New", self)
        new_action.triggered.connect(self.new_file)
        new_action.setShortcut(QKeySequence.New)
        file_menu.addAction(new_action)
        
        open_action = QAction("Open", self)
        open_action.triggered.connect(self.open_file_dialog)
        open_action.setShortcut(QKeySequence.Open)
        file_menu.addAction(open_action)
        
        save_action = QAction("Save", self)
        save_action.triggered.connect(self.save_file)
        save_action.setShortcut(QKeySequence.Save)
        file_menu.addAction(save_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        exit_action.setShortcut(QKeySequence.Quit)
        file_menu.addAction(exit_action)
        
        # Edit menu
        edit_menu = menubar.addMenu("Edit")
        
        cut_action = QAction("Cut", self)
        cut_action.triggered.connect(self.cut)
        cut_action.setShortcut(QKeySequence.Cut)
        edit_menu.addAction(cut_action)
        
        copy_action = QAction("Copy", self)
        copy_action.triggered.connect(self.copy)
        copy_action.setShortcut(QKeySequence.Copy)
        edit_menu.addAction(copy_action)
        
        paste_action = QAction("Paste", self)
        paste_action.triggered.connect(self.paste)
        paste_action.setShortcut(QKeySequence.Paste)
        edit_menu.addAction(paste_action)
        
        edit_menu.addSeparator()
        
        find_action = QAction("Find", self)
        find_action.triggered.connect(self.show_find_dialog)
        find_action.setShortcut(QKeySequence.Find)
        edit_menu.addAction(find_action)
        
        replace_action = QAction("Replace", self)
        replace_action.triggered.connect(self.show_replace_dialog)
        replace_action.setShortcut(QKeySequence.Replace)
        edit_menu.addAction(replace_action)
        
        # View menu
        view_menu = menubar.addMenu("View")
        
        # Theme selection
        theme_menu = view_menu.addMenu("Theme")
        themes = ["Light", "Dark"]
        for theme in themes:
            action = QAction(theme, self)
            action.triggered.connect(lambda checked, t=theme: self.set_theme(t))
            theme_menu.addAction(action)
            
    def setup_shortcuts(self):
        # Add any additional keyboard shortcuts here
        pass
        
    def show_find_dialog(self):
        dialog = FindDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            self.find_text(dialog.find_text.text(), 
                         dialog.case_sensitive.isChecked(),
                         dialog.whole_word.isChecked())
                         
    def show_replace_dialog(self):
        # Similar to find dialog but with replace functionality
        pass
        
    def find_text(self, text, case_sensitive=False, whole_word=False):
        current_editor = self.editor_tabs.currentWidget()
        if current_editor:
            cursor = current_editor.document().find(text, current_editor.textCursor())
            if not cursor.isNull():
                current_editor.setTextCursor(cursor)
            
    def set_theme(self, theme):
        if theme == "Dark":
            self.setStyleSheet("""
                QMainWindow, QWidget {
                    background-color: #1E1E1E;
                    color: #D4D4D4;
                }
                QTabWidget::pane {
                    border: 1px solid #333333;
                    background-color: #1E1E1E;
                }
                QTabBar::tab {
                    background-color: #252526;
                    color: #D4D4D4;
                    padding: 8px 12px;
                    border: 1px solid #333333;
                }
                QTabBar::tab:selected {
                    background-color: #2D2D2D;
                }
                QTreeView {
                    background-color: #1E1E1E;
                    color: #D4D4D4;
                    border: 1px solid #333333;
                }
                QTreeView::item:selected {
                    background-color: #2D2D2D;
                }
                QStatusBar {
                    background-color: #1E1E1E;
                    color: #D4D4D4;
                }
                QToolBar {
                    background-color: #1E1E1E;
                    border: none;
                }
                QMenuBar {
                    background-color: #1E1E1E;
                    color: #D4D4D4;
                }
                QMenuBar::item:selected {
                    background-color: #2D2D2D;
                }
                QMenu {
                    background-color: #1E1E1E;
                    color: #D4D4D4;
                }
                QMenu::item:selected {
                    background-color: #2D2D2D;
                }
                QPushButton {
                    background-color: #252526;
                    color: #D4D4D4;
                    border: 1px solid #333333;
                    padding: 5px;
                }
                QPushButton:hover {
                    background-color: #2D2D2D;
                }
                QLineEdit {
                    background-color: #252526;
                    color: #D4D4D4;
                    border: 1px solid #333333;
                    padding: 5px;
                }
                QScrollBar:vertical {
                    background-color: #1E1E1E;
                    width: 14px;
                    margin: 0px;
                }
                QScrollBar::handle:vertical {
                    background-color: #424242;
                    min-height: 20px;
                    border-radius: 7px;
                }
                QScrollBar::handle:vertical:hover {
                    background-color: #4F4F4F;
                }
                QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                    height: 0px;
                }
                QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                    background: none;
                }
                QSplitter::handle {
                    background-color: #333333;
                }
                QSplitter::handle:horizontal {
                    width: 2px;
                }
                QSplitter::handle:vertical {
                    height: 2px;
                }
            """)
        else:
            self.setStyleSheet("")
            
    def new_file(self):
        editor = CodeEditor()
        self.editor_tabs.addTab(editor, "Untitled")
        self.editor_tabs.setCurrentWidget(editor)
        
    def open_file_dialog(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Open File",
            "",
            "All Files (*.*);;Python Files (*.py);;Text Files (*.txt)"
        )
        if file_name:
            self.open_file_by_path(file_name)
            
    def open_file(self, index):
        file_path = self.file_model.filePath(index)
        if not self.file_model.isDir(index):
            self.open_file_by_path(file_path)
            
    def open_file_by_path(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            editor = CodeEditor()
            editor.setText(content)
            editor.current_file = file_path
            
            # Add tab with file name
            self.editor_tabs.addTab(editor, os.path.basename(file_path))
            self.editor_tabs.setCurrentWidget(editor)
            
            self.statusBar.showMessage(f"Opened {file_path}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not open file: {str(e)}")
            
    def save_file(self):
        current_editor = self.editor_tabs.currentWidget()
        if not current_editor:
            return
            
        current_tab = self.editor_tabs.currentIndex()
        file_name = self.editor_tabs.tabText(current_tab)
        
        if file_name == "Untitled":
            file_name, _ = QFileDialog.getSaveFileName(
                self,
                "Save File",
                "",
                "All Files (*.*);;Python Files (*.py);;Text Files (*.txt)"
            )
            if not file_name:
                return
                
        try:
            with open(file_name, 'w', encoding='utf-8') as f:
                f.write(current_editor.toPlainText())
                
            current_editor.current_file = file_name
            self.editor_tabs.setTabText(current_tab, os.path.basename(file_name))
            self.statusBar.showMessage(f"Saved {file_name}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not save file: {str(e)}")
            
    def close_tab(self, index):
        self.editor_tabs.removeTab(index)
        
    def cut(self):
        current_editor = self.editor_tabs.currentWidget()
        if current_editor:
            current_editor.cut()
            
    def copy(self):
        current_editor = self.editor_tabs.currentWidget()
        if current_editor:
            current_editor.copy()
            
    def paste(self):
        current_editor = self.editor_tabs.currentWidget()
        if current_editor:
            current_editor.paste() 