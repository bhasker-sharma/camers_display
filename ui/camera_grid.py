#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Camera Grid Window
Displays a grid of camera feeds and handles navigation between screens
"""

import math
from PyQt5.QtWidgets import (QMainWindow, QWidget, QGridLayout, QVBoxLayout,
                           QHBoxLayout, QLabel, QPushButton, QSizePolicy)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QIcon, QPixmap

from ui.camera_view import CameraView
from ui.config_dialog import ConfigDialog
from core.camera_manager import CameraManager
from core.config_manager import ConfigManager
from assets.icons import get_logo_icon, get_arrow_icon, get_config_icon, get_back_icon
from assets.stylesheet import get_stylesheet

class CameraGridWindow(QMainWindow):
    """Main window class that shows the grid of camera feeds"""
    
    def __init__(self):
        super().__init__()
        
        # Initialize configuration manager
        self.config_manager = ConfigManager()
        
        # Initialize camera manager
        self.camera_manager = CameraManager(self.config_manager)
        
        # Current screen (0 or 1)
        self.current_screen = 0
        
        # Current mode (0 = grid view, 1 = single camera view)
        self.mode = 0
        
        # Currently focused camera (for single view mode)
        self.focused_camera = 0
        
        # Initialize UI
        self.init_ui()
        
        # Start update timer (30 FPS)
        self.update_timer = QTimer(self)
        self.update_timer.timeout.connect(self.update_camera_display)
        self.update_timer.start(33)  # ~30 fps
        
    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("Tuyere Camera Monitoring System")
        self.setWindowIcon(get_logo_icon())
        
        # Set window size
        self.resize(1280, 720)
        
        # Apply stylesheet
        self.setStyleSheet(get_stylesheet())
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)
        
        # Navigation bar
        self.navbar = QWidget()
        self.navbar_layout = QHBoxLayout(self.navbar)
        self.navbar_layout.setContentsMargins(0, 0, 0, 0)
        self.create_navbar()
        main_layout.addWidget(self.navbar)
        
        # Container for camera views
        self.camera_container = QWidget()
        self.camera_layout = QGridLayout(self.camera_container)
        self.camera_layout.setContentsMargins(0, 0, 0, 0)
        self.camera_layout.setSpacing(5)
        main_layout.addWidget(self.camera_container)
        
        # Create camera views for grid
        self.camera_views = []
        for i in range(24):
            view = CameraView(i, self.camera_manager)
            view.clicked.connect(self.on_camera_clicked)
            self.camera_views.append(view)
            
        # Initial update of camera display
        self.update_camera_display()
        
    def create_navbar(self):
        """Create the navigation bar at the top"""
        # Clear existing widgets
        while self.navbar_layout.count():
            item = self.navbar_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
                
        if self.mode == 0:  # Grid view
            # Title
            title_label = QLabel("TIPL")
            title_label.setObjectName("navbar-title")
            self.navbar_layout.addWidget(title_label)
            
            # Screen label
            screen_label = QLabel(f"Screen {self.current_screen + 1}")
            screen_label.setObjectName("screen-label")
            self.navbar_layout.addWidget(screen_label)
            
            self.navbar_layout.addStretch()
            
            # Previous screen button
            prev_button = QPushButton()
            prev_button.setIcon(get_arrow_icon("left"))
            prev_button.setToolTip("Previous Screen")
            prev_button.setObjectName("nav-button")
            prev_button.clicked.connect(self.on_prev_clicked)
            self.navbar_layout.addWidget(prev_button)
            
            # Next screen button
            next_button = QPushButton()
            next_button.setIcon(get_arrow_icon("right"))
            next_button.setToolTip("Next Screen")
            next_button.setObjectName("nav-button")
            next_button.clicked.connect(self.on_next_clicked)
            self.navbar_layout.addWidget(next_button)
            
            # Configuration button
            config_button = QPushButton()
            config_button.setIcon(get_config_icon())
            config_button.setToolTip("Configure Cameras")
            config_button.setObjectName("nav-button")
            config_button.clicked.connect(self.on_config_clicked)
            self.navbar_layout.addWidget(config_button)
            
        else:  # Single camera view
            # Back button
            back_button = QPushButton()
            back_button.setIcon(get_back_icon())
            back_button.setToolTip("Back to Grid View")
            back_button.setObjectName("nav-button")
            back_button.clicked.connect(self.on_back_clicked)
            self.navbar_layout.addWidget(back_button)
            
            # Camera title
            camera_index = self.focused_camera
            config = self.config_manager.get_camera_config(camera_index)
            title_label = QLabel(config.get('name', f"Camera {camera_index + 1}"))
            title_label.setObjectName("navbar-title")
            self.navbar_layout.addWidget(title_label)
            
            self.navbar_layout.addStretch()
            
            # Previous camera button
            prev_button = QPushButton()
            prev_button.setIcon(get_arrow_icon("left"))
            prev_button.setToolTip("Previous Camera")
            prev_button.setObjectName("nav-button")
            prev_button.clicked.connect(lambda: self.on_camera_clicked(
                (self.focused_camera - 1) % 48))
            self.navbar_layout.addWidget(prev_button)
            
            # Next camera button
            next_button = QPushButton()
            next_button.setIcon(get_arrow_icon("right"))
            next_button.setToolTip("Next Camera")
            next_button.setObjectName("nav-button")
            next_button.clicked.connect(lambda: self.on_camera_clicked(
                (self.focused_camera + 1) % 48))
            self.navbar_layout.addWidget(next_button)
            
            # Configuration button
            config_button = QPushButton()
            config_button.setIcon(get_config_icon())
            config_button.setToolTip("Configure Camera")
            config_button.setObjectName("nav-button")
            config_button.clicked.connect(self.on_config_clicked)
            self.navbar_layout.addWidget(config_button)
        
    def update_camera_display(self):
        """Update the camera display based on current screen and mode"""
        # Clear layout
        while self.camera_layout.count():
            item = self.camera_layout.takeAt(0)
            if item.widget():
                item.widget().setParent(None)
                
        if self.mode == 0:  # Grid view
            # Fixed grid dimensions - 6 columns, 4 rows
            rows, cols = 4, 6
            
            # Add views to layout
            for i in range(24):
                row = i // cols
                col = i % cols
                
                # Calculate actual camera index
                camera_index = i + self.current_screen * 24
                
                # Update camera index
                self.camera_views[i].set_camera_index(camera_index)
                
                # Add to layout with stretch factors to maintain uniform size
                self.camera_layout.addWidget(self.camera_views[i], row, col)
                
            # Set stretch factors to ensure uniform cell sizes
            for i in range(rows):
                self.camera_layout.setRowStretch(i, 1)
            for i in range(cols):
                self.camera_layout.setColumnStretch(i, 1)
                
        else:  # Single camera view
            # Create a single camera view if needed
            if not hasattr(self, 'single_view'):
                self.single_view = CameraView(self.focused_camera, self.camera_manager)
                
            # Update camera index
            self.single_view.set_camera_index(self.focused_camera)
            
            # Add to layout and make it take the full space
            self.camera_layout.addWidget(self.single_view, 0, 0, 4, 6)  # Span all rows and columns
            
            # Make sure the camera view expands to fill the available space
            self.single_view.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            
            # Set stretch factors to ensure the view takes full space
            self.camera_layout.setRowStretch(0, 1)
            self.camera_layout.setColumnStretch(0, 1)
    
    def calculate_grid_dimensions(self, num_cameras):
        """Calculate grid dimensions"""
        # Fixed dimensions - 6 columns, 4 rows
        return 4, 6
            
    def on_camera_clicked(self, camera_index):
        """Handle camera click to expand to full view"""
        self.focused_camera = camera_index
        self.mode = 1  # Single camera view
        
        # Update UI
        self.create_navbar()
        self.update_camera_display()
        
    def on_prev_clicked(self):
        """Handle click of previous button"""
        # Ensure we're on the first screen (showing cameras 1-24)
        self.current_screen = 0
        
        # Update UI
        self.create_navbar()
        self.update_camera_display()
        
    def on_next_clicked(self):
        """Handle click of next button"""
        # Ensure we're on the second screen (showing cameras 25-48)
        self.current_screen = 1
        
        # Update UI
        self.create_navbar()
        self.update_camera_display()
        
    def on_back_clicked(self):
        """Handle click of back button to return to grid view"""
        self.mode = 0  # Grid view
        
        # Update UI
        self.create_navbar()
        self.update_camera_display()
        
    def on_config_clicked(self):
        """Open configuration dialog"""
        dialog = ConfigDialog(self.config_manager, self)
        if dialog.exec_():
            # Reload camera configuration
            self.camera_manager.reload_config()
            
    def closeEvent(self, event):
        """Handle window close event"""
        # Stop all camera threads
        self.camera_manager.stop_all_cameras()