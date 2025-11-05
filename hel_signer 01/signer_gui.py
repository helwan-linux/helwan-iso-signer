#!/usr/bin/env python3
"""
signer_gui.py
PyQt5 GUI application to wrap the ISO signing logic, with added application icon.
"""
import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QLineEdit, QPushButton, QTextEdit, QLabel, QFileDialog, QMessageBox
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QIcon  # <--- NEW IMPORT

# Import the core signing logic functions
from signer_logic import execute_signing_process

# --- Threading Class for Non-Blocking Operation ---
class SignerThread(QThread):
    log_signal = pyqtSignal(str)
    finished_signal = pyqtSignal(tuple) # (report, dest_dir)
    error_signal = pyqtSignal(str)

    def __init__(self, iso_path):
        super().__init__()
        self.iso_path = iso_path

    def run(self):
        try:
            report, dest_dir = execute_signing_process(
                self.iso_path,
                log_callback=self.log_signal.emit
            )
            self.finished_signal.emit((report, str(dest_dir)))
        except Exception as e:
            self.error_signal.emit(str(e))
            self.log_signal.emit(f"ERROR: Process failed: {e}")


# --- Main Application Window ---
class SignerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Helwan ISO Signer (PyQt5)")
        self.setGeometry(100, 100, 800, 600)
        
        # 🌟 NEW: Set the window icon (appears in the title bar and taskbar)
        icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'signer_icon.png')
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        # Note: Setting the application icon is done outside the class (see if __name__ == '__main__')

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        
        self.signer_thread = None

        self.init_ui()

    def init_ui(self):
        # 1. ISO Path Input Row
        iso_layout = QHBoxLayout()
        self.iso_path_input = QLineEdit()
        self.iso_path_input.setPlaceholderText("Select the ISO file path...")
        self.browse_button = QPushButton("Browse ISO")
        self.browse_button.clicked.connect(self.browse_iso)
        
        iso_layout.addWidget(QLabel("ISO File:"))
        iso_layout.addWidget(self.iso_path_input)
        iso_layout.addWidget(self.browse_button)
        self.layout.addLayout(iso_layout)
        
        # 2. Sign Button
        self.sign_button = QPushButton("🚀 Sign and Generate Release Files")
        self.sign_button.setFixedHeight(40)
        self.sign_button.clicked.connect(self.start_signing)
        self.layout.addWidget(self.sign_button)

        # 3. Log Output Area
        self.layout.addWidget(QLabel("Output Log / Report:"))
        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        self.layout.addWidget(self.log_output)
        
        # 4. Final Output Path Display
        output_layout = QHBoxLayout()
        self.output_label = QLabel("Output Folder:")
        self.output_path_display = QLineEdit()
        self.output_path_display.setReadOnly(True)
        self.output_path_display.setStyleSheet("background-color: #f0f0f0;")
        
        self.open_folder_button = QPushButton("Open Folder")
        self.open_folder_button.setEnabled(False)
        self.open_folder_button.clicked.connect(self.open_output_folder)
        
        output_layout.addWidget(self.output_label)
        output_layout.addWidget(self.output_path_display)
        output_layout.addWidget(self.open_folder_button)
        self.layout.addLayout(output_layout)

    # --- (browse_iso, start_signing, log_to_gui, on_signing_finished, on_signing_error, open_output_folder methods remain unchanged) ---
    def browse_iso(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, 
            "Select ISO File to Sign", 
            "", 
            "ISO Files (*.iso);;All Files (*)"
        )
        if file_path:
            self.iso_path_input.setText(file_path)
            self.log_output.clear()
            self.output_path_display.clear()
            self.open_folder_button.setEnabled(False)

    def start_signing(self):
        iso_path = self.iso_path_input.text()
        
        if not iso_path or not os.path.isfile(iso_path):
            QMessageBox.warning(self, "Invalid File", "Please select a valid ISO file before starting.")
            return

        self.sign_button.setEnabled(False)
        self.browse_button.setEnabled(False)
        self.log_output.clear()
        self.log_output.append("--- Starting ISO Signing Process ---")
        self.output_path_display.clear()
        self.open_folder_button.setEnabled(False)
        
        self.signer_thread = SignerThread(iso_path)
        self.signer_thread.log_signal.connect(self.log_to_gui)
        self.signer_thread.finished_signal.connect(self.on_signing_finished)
        self.signer_thread.error_signal.connect(self.on_signing_error)
        self.signer_thread.start()

    def log_to_gui(self, message):
        self.log_output.append(message)

    def on_signing_finished(self, results):
        report, dest_dir = results
        
        self.log_output.append("\n" + "="*50)
        self.log_output.append("✅ **OPERATION COMPLETED SUCCESSFULLY!**")
        self.log_output.append("="*50)
        self.log_output.append(report)
        
        self.output_path_display.setText(dest_dir)
        
        self.sign_button.setEnabled(True)
        self.browse_button.setEnabled(True)
        self.open_folder_button.setEnabled(True)

    def on_signing_error(self, error_message):
        QMessageBox.critical(self, "Signing Error", f"The signing process failed: {error_message}")
        
        self.sign_button.setEnabled(True)
        self.browse_button.setEnabled(True)
        self.open_folder_button.setEnabled(False)

    def open_output_folder(self):
        folder_path = self.output_path_display.text()
        if not folder_path or not os.path.isdir(folder_path):
             QMessageBox.warning(self, "Error", "Output folder path is invalid.")
             return
             
        if sys.platform == "win32":
            os.startfile(folder_path)
        elif sys.platform == "darwin": # macOS
            subprocess.Popen(["open", folder_path])
        else: # linux
            subprocess.Popen(["xdg-open", folder_path])


if __name__ == '__main__':
    try:
        app = QApplication(sys.argv)
        
        # 🌟 NEW: Set the application icon (Crucial for proper taskbar/launcher display on some OSes)
        icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'signer_icon.png')
        if os.path.exists(icon_path):
            app.setWindowIcon(QIcon(icon_path)) 
        
        ex = SignerApp()
        ex.show()
        sys.exit(app.exec_())
    except ImportError:
        print("ERROR: PyQt5 is not installed. Please run: pip install PyQt5")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
