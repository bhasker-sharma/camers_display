#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Configuration Dialog
Allows user to configure camera RTSP URLs
"""

from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
                           QPushButton, QComboBox, QGridLayout, QGroupBox,
                           QMessageBox, QSpinBox, QFormLayout)
from PyQt5.QtCore import Qt

class ConfigDialog(QDialog):
    """Dialog for configuring camera settings"""
    
    def __init__(self, config_manager, parent=None):
        super().__init__(parent)
        
        self.config_manager = config_manager
        
        # Initialize UI
        self.init_ui()
        
        # Load current configuration
        self.load_config()

    def init_ui(self):
        """Initialize user interface"""
        self.setWindowTitle("Configure Cameras")
        self.resize(600, 300)
        
        # Main layout
        layout = QVBoxLayout(self)
        
        # Camera selection
        select_group = QGroupBox("Select Camera")
        select_layout = QFormLayout()
        
        self.camera_spinner = QSpinBox()
        self.camera_spinner.setRange(1, 48)
        self.camera_spinner.setValue(1)
        self.camera_spinner.valueChanged.connect(self.on_camera_selected)
        select_layout.addRow("Camera Number:", self.camera_spinner)
        
        select_group.setLayout(select_layout)
        layout.addWidget(select_group)
        
        # Camera configuration
        config_group = QGroupBox("Camera Configuration")
        config_layout = QFormLayout()
        
        self.enabled_checkbox = QPushButton("Enable Camera")
        self.enabled_checkbox.setCheckable(True)
        self.enabled_checkbox.setChecked(True)
        config_layout.addRow("Status:", self.enabled_checkbox)
        
        # Add camera name field
        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("Enter a custom name for this camera")
        config_layout.addRow("Camera Name:", self.name_edit)
        
        self.source_combo = QComboBox()
        self.source_combo.addItems(["RTSP Stream", "Local Camera"])
        self.source_combo.currentIndexChanged.connect(self.on_source_changed)
        config_layout.addRow("Source Type:", self.source_combo)
        
        self.url_edit = QLineEdit()
        self.url_edit.setPlaceholderText("rtsp://username:password@ip_address:port/stream")
        config_layout.addRow("RTSP URL:", self.url_edit)
        
        self.device_spinner = QSpinBox()
        self.device_spinner.setRange(0, 10)
        self.device_spinner.setValue(0)
        self.device_spinner.setVisible(False)
        config_layout.addRow("Device Number:", self.device_spinner)
        
        config_group.setLayout(config_layout)
        layout.addWidget(config_group)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        test_button = QPushButton("Test Connection")
        test_button.clicked.connect(self.on_test_clicked)
        button_layout.addWidget(test_button)
        
        button_layout.addStretch()
        
        save_button = QPushButton("Save")
        save_button.clicked.connect(self.on_save_clicked)
        button_layout.addWidget(save_button)
        
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(cancel_button)
        
        layout.addLayout(button_layout)

    def load_config(self):
        """Load the configuration for the currently selected camera"""
        camera_index = self.camera_spinner.value() - 1
        config = self.config_manager.get_camera_config(camera_index)
        
        self.enabled_checkbox.setChecked(config.get('enabled', False))
        
        # Load custom camera name
        default_name = f"Camera {camera_index + 1}"
        self.name_edit.setText(config.get('name', default_name))
        
        source_type = config.get('source_type', 'rtsp')
        self.source_combo.setCurrentIndex(0 if source_type == 'rtsp' else 1)
        
        self.url_edit.setText(config.get('url', ''))
        self.device_spinner.setValue(config.get('device', 0))

    def on_camera_selected(self):
        """Handle camera selection change"""
        self.load_config()

    def on_source_changed(self, index):
        """Handle source type change"""
        is_rtsp = (index == 0)
        self.url_edit.setVisible(is_rtsp)
        self.device_spinner.setVisible(not is_rtsp)

    def on_test_clicked(self):
        """Test the camera connection"""
        camera_index = self.camera_spinner.value() - 1
        
        # Create config from current UI values
        config = {
            'enabled': self.enabled_checkbox.isChecked(),
            'name': self.name_edit.text(),  # Add the custom camera name
            'source_type': 'rtsp' if self.source_combo.currentIndex() == 0 else 'local',
            'url': self.url_edit.text(),
            'device': self.device_spinner.value()
        }
        
        # Test the connection
        success, message = self.config_manager.test_camera_connection(camera_index, config)
        
        # Show result
        if success:
            QMessageBox.information(self, "Connection Test", "Connection successful!")
        else:
            QMessageBox.warning(self, "Connection Test", f"Connection failed: {message}")

    def on_save_clicked(self):
        """Save the camera configuration"""
        camera_index = self.camera_spinner.value() - 1
        
        # Create config from current UI values
        config = {
            'enabled': self.enabled_checkbox.isChecked(),
            'name': self.name_edit.text(),  # Add the custom camera name
            'source_type': 'rtsp' if self.source_combo.currentIndex() == 0 else 'local',
            'url': self.url_edit.text(),
            'device': self.device_spinner.value()
        }
        
        # Validate configuration
        if config['enabled']:
            if config['source_type'] == 'rtsp' and not config['url']:
                QMessageBox.warning(self, "Invalid Configuration", 
                                  "RTSP URL is required for RTSP source type.")
                return
        
        # Save configuration
        self.config_manager.set_camera_config(camera_index, config)
        
        # Accept dialog
        self.accept()