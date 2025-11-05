#!/usr/bin/env python3
"""
signer_gui.py
PyQt5 GUI application to wrap the ISO signing logic.
Features: English UI, Output dir selector, SHA512, SHA3-512, BLAKE2b, Global Progress Bar, and Verify tab.
"""
import sys
import os
import subprocess
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QLineEdit, QPushButton, QTextEdit, QLabel, QFileDialog, QMessageBox,
    QProgressBar, QTabWidget, QCheckBox, QGroupBox, QGridLayout
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QDir
from PyQt5.QtGui import QIcon

# Import the core signing logic functions
from signer_logic import execute_signing_process, verify_iso_signature

# --- Threading Class for Non-Blocking Operation ---
class SignerThread(QThread):
    log_signal = pyqtSignal(str)
    progress_signal = pyqtSignal(int)
    finished_signal = pyqtSignal(tuple) # (report, dest_dir)
    error_signal = pyqtSignal(str)

    def __init__(self, iso_path, output_dir, hash_algs):
        super().__init__()
        self.iso_path = iso_path
        self.output_dir = output_dir
        self.hash_algs = hash_algs

    def run(self):
        try:
            report, dest_dir = execute_signing_process(
                self.iso_path,
                self.output_dir,
                self.hash_algs,
                log_callback=self.log_signal.emit,
                progress_callback=self.progress_signal.emit
            )
            self.finished_signal.emit((report, str(dest_dir)))
        except Exception as e:
            self.error_signal.emit(str(e))
            self.log_signal.emit(f"ERROR: Process failed: {e}")

# Thread for Verification
class VerifyThread(QThread):
    log_signal = pyqtSignal(str)
    finished_signal = pyqtSignal(bool)
    error_signal = pyqtSignal(str)
    
    def __init__(self, iso_path, sig_path):
        super().__init__()
        self.iso_path = iso_path
        self.sig_path = sig_path

    def run(self):
        try:
            result = verify_iso_signature(self.iso_path, self.sig_path, self.log_signal.emit)
            self.finished_signal.emit(result)
        except Exception as e:
            self.error_signal.emit(str(e))
            self.log_signal.emit(f"ERROR: Verification failed: {e}")


# --- Main Application Window ---
class SignerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Helwan ISO Signer & Verifier")
        self.setGeometry(100, 100, 800, 700)
        
        icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'signer_icon.png')
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
            
        self.tab_widget = QTabWidget()
        self.setCentralWidget(self.tab_widget)

        self.init_sign_tab()
        self.init_verify_tab()

        self.tab_widget.addTab(self.sign_tab, "🚀 Sign ISO")
        self.tab_widget.addTab(self.verify_tab, "🔍 Verify ISO")
        
        self.signer_thread = None
        self.verify_thread = None
        
    # --- Sign Tab Setup ---
    def init_sign_tab(self):
        self.sign_tab = QWidget()
        self.sign_layout = QVBoxLayout(self.sign_tab)
        
        # 1. ISO Path Input Row
        self.iso_path_input = QLineEdit()
        self.iso_path_input.setPlaceholderText("Select the ISO file path...")
        self.browse_iso_button = QPushButton("Browse ISO")
        self.browse_iso_button.clicked.connect(self.browse_iso_file)
        
        iso_layout = QHBoxLayout()
        iso_layout.addWidget(QLabel("ISO File:"))
        iso_layout.addWidget(self.iso_path_input)
        iso_layout.addWidget(self.browse_iso_button)
        self.sign_layout.addLayout(iso_layout)
        
        # 2. Output Directory Input Row
        self.output_dir_input = QLineEdit(QDir.currentPath() + "/release")
        self.browse_output_button = QPushButton("Browse Output Dir")
        self.browse_output_button.clicked.connect(self.browse_output_dir)
        
        output_layout = QHBoxLayout()
        output_layout.addWidget(QLabel("Output Root Directory:"))
        output_layout.addWidget(self.output_dir_input)
        output_layout.addWidget(self.browse_output_button)
        self.sign_layout.addLayout(output_layout)
        
        # 3. Hash Options Group (UPDATED to include SHA3-512 and BLAKE2b)
        hash_group = QGroupBox("Select Hash Algorithms")
        hash_layout = QGridLayout(hash_group)
        
        self.hash_sha256 = QCheckBox("SHA256 (Recommended)")
        self.hash_sha256.setChecked(True)
        self.hash_sha512 = QCheckBox("SHA512")
        self.hash_sha1 = QCheckBox("SHA1")
        self.hash_md5 = QCheckBox("MD5 (Legacy)")
        
        # NEW ALGORITHMS ADDED
        self.hash_sha3_512 = QCheckBox("SHA3-512")
        self.hash_blake2b = QCheckBox("BLAKE2b (Fast)")
        
        hash_layout.addWidget(self.hash_sha256, 0, 0)
        hash_layout.addWidget(self.hash_sha512, 0, 1)
        hash_layout.addWidget(self.hash_sha3_512, 0, 2)
        hash_layout.addWidget(self.hash_blake2b, 0, 3)
        hash_layout.addWidget(self.hash_sha1, 1, 0)
        hash_layout.addWidget(self.hash_md5, 1, 1)
        
        hash_group.setLayout(hash_layout)
        self.sign_layout.addWidget(hash_group)
        
        # 4. Progress Bar (Global Progress)
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        self.progress_label = QLabel("Overall Process Progress:") 
        self.sign_layout.addWidget(self.progress_label)
        self.sign_layout.addWidget(self.progress_bar)

        # 5. Sign Button
        self.sign_button = QPushButton("🚀 Sign and Generate Release Files")
        self.sign_button.setFixedHeight(40)
        self.sign_button.clicked.connect(self.start_signing)
        self.sign_layout.addWidget(self.sign_button)

        # 6. Log Output Area
        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        self.sign_layout.addWidget(QLabel("Output Log / Report:"))
        self.sign_layout.addWidget(self.log_output)
        
        # 7. Final Output Path Display
        output_row_layout = QHBoxLayout()
        self.output_path_display = QLineEdit()
        self.output_path_display.setReadOnly(True)
        self.output_path_display.setStyleSheet("background-color: #f0f0f0;")
        
        self.open_folder_button = QPushButton("Open Folder")
        self.open_folder_button.setEnabled(False)
        self.open_folder_button.clicked.connect(self.open_output_folder)
        
        output_row_layout.addWidget(QLabel("Final Output Path:"))
        output_row_layout.addWidget(self.output_path_display)
        output_row_layout.addWidget(self.open_folder_button)
        self.sign_layout.addLayout(output_row_layout)
        
    # --- Verify Tab Setup ---
    def init_verify_tab(self):
        self.verify_tab = QWidget()
        self.verify_layout = QVBoxLayout(self.verify_tab)
        
        self.verify_iso_input = QLineEdit()
        self.verify_iso_input.setPlaceholderText("Select the ISO file to verify...")
        self.verify_iso_button = QPushButton("Browse ISO")
        self.verify_iso_button.clicked.connect(lambda: self.browse_file(self.verify_iso_input, "ISO Files (*.iso)"))
        
        iso_layout = QHBoxLayout()
        iso_layout.addWidget(QLabel("ISO File:"))
        iso_layout.addWidget(self.verify_iso_input)
        iso_layout.addWidget(self.verify_iso_button)
        self.verify_layout.addLayout(iso_layout)
        
        self.verify_sig_input = QLineEdit()
        self.verify_sig_input.setPlaceholderText("Select the signature file (.sig.asc or .sig)...")
        self.verify_sig_button = QPushButton("Browse Signature")
        self.verify_sig_button.clicked.connect(lambda: self.browse_file(self.verify_sig_input, "Signature Files (*.asc *.sig)"))
        
        sig_layout = QHBoxLayout()
        sig_layout.addWidget(QLabel("Signature File:"))
        sig_layout.addWidget(self.verify_sig_input)
        sig_layout.addWidget(self.verify_sig_button)
        self.verify_layout.addLayout(sig_layout)
        
        self.verify_button = QPushButton("🔍 Start Verification")
        self.verify_button.setFixedHeight(40)
        self.verify_button.clicked.connect(self.start_verification)
        self.verify_layout.addWidget(self.verify_button)
        
        self.verify_log_output = QTextEdit()
        self.verify_log_output.setReadOnly(True)
        self.verify_layout.addWidget(QLabel("Verification Log:"))
        self.verify_layout.addWidget(self.verify_log_output)
        
        self.verify_layout.addStretch(1)


    # --- Common File Browsing Helper ---
    def browse_file(self, line_edit, file_filter):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select File", "", file_filter)
        if file_path:
            line_edit.setText(file_path)

    def browse_iso_file(self):
        self.browse_file(self.iso_path_input, "ISO Files (*.iso)")
        self.log_output.clear()
        self.output_path_display.clear()
        self.open_folder_button.setEnabled(False)
        self.progress_bar.setValue(0)
        
    def browse_output_dir(self):
        dir_path = QFileDialog.getExistingDirectory(self, "Select Output Directory", self.output_dir_input.text())
        if dir_path:
            self.output_dir_input.setText(dir_path)

    # --- Sign Functions (UPDATED to collect new hashes) ---
    def start_signing(self):
        iso_path = self.iso_path_input.text()
        output_dir = self.output_dir_input.text()
        
        hash_algs = []
        if self.hash_sha256.isChecked(): hash_algs.append('SHA256')
        if self.hash_sha512.isChecked(): hash_algs.append('SHA512')
        if self.hash_sha3_512.isChecked(): hash_algs.append('SHA3_512') # NEW
        if self.hash_blake2b.isChecked(): hash_algs.append('BLAKE2B')     # NEW
        if self.hash_sha1.isChecked(): hash_algs.append('SHA1')
        if self.hash_md5.isChecked(): hash_algs.append('MD5')

        if not iso_path or not os.path.isfile(iso_path):
            QMessageBox.warning(self, "Invalid File", "Please select a valid ISO file before starting.")
            return
        if not output_dir:
            QMessageBox.warning(self, "Invalid Directory", "Please specify a valid output directory.")
            return
        if not hash_algs:
            QMessageBox.warning(self, "Hash Error", "Please select at least one hash algorithm.")
            return

        # Disable controls during operation
        self.sign_button.setEnabled(False)
        self.browse_iso_button.setEnabled(False)
        self.browse_output_button.setEnabled(False)
        self.progress_bar.setValue(0)
        
        self.log_output.clear()
        self.log_output.append("--- Starting ISO Signing Process ---")
        self.output_path_display.clear()
        self.open_folder_button.setEnabled(False)
        
        # Initialize and start the thread
        self.signer_thread = SignerThread(iso_path, output_dir, hash_algs)
        self.signer_thread.log_signal.connect(self.log_to_gui)
        self.signer_thread.progress_signal.connect(self.progress_bar.setValue)
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
        self.progress_bar.setValue(100)
        
        # Re-enable controls
        self.sign_button.setEnabled(True)
        self.browse_iso_button.setEnabled(True)
        self.browse_output_button.setEnabled(True)
        self.open_folder_button.setEnabled(True)

    def on_signing_error(self, error_message):
        QMessageBox.critical(self, "Signing Error", f"The signing process failed: {error_message}")
        self.progress_bar.setValue(0)
        
        # Re-enable controls
        self.sign_button.setEnabled(True)
        self.browse_iso_button.setEnabled(True)
        self.browse_output_button.setEnabled(True)
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
            
    # --- Verify Functions (Unchanged) ---
    def start_verification(self):
        iso_path = self.verify_iso_input.text()
        sig_path = self.verify_sig_input.text()
        
        if not iso_path or not os.path.isfile(iso_path):
            QMessageBox.warning(self, "Input Error", "Please select a valid ISO file for verification.")
            return
        if not sig_path or not os.path.isfile(sig_path):
            QMessageBox.warning(self, "Input Error", "Please select a valid signature file.")
            return
            
        self.verify_button.setEnabled(False)
        self.verify_log_output.clear()
        self.verify_log_output.append("--- Starting Signature Verification ---")
        
        self.verify_thread = VerifyThread(iso_path, sig_path)
        self.verify_thread.log_signal.connect(self.verify_log_output.append)
        self.verify_thread.finished_signal.connect(self.on_verification_finished)
        self.verify_thread.error_signal.connect(self.on_verification_error)
        self.verify_thread.start()
        
    def on_verification_finished(self, result):
        if result:
            self.verify_log_output.append("\n✅ **VERIFICATION SUCCESSFUL! The file is authentic and intact.**")
            QMessageBox.information(self, "Success", "Signature verification passed!")
        else:
            self.verify_log_output.append("\n❌ **VERIFICATION FAILED! The file may be corrupt or tampered with.**")
            QMessageBox.critical(self, "Failure", "Signature verification failed!")
            
        self.verify_button.setEnabled(True)
        
    def on_verification_error(self, error_message):
        QMessageBox.critical(self, "Verification Error", f"Verification process encountered a critical error: {error_message}")
        self.verify_button.setEnabled(True)


if __name__ == '__main__':
    try:
        app = QApplication(sys.argv)
        # Icon setup
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
