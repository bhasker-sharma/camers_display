#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Camera View Widget
Displays a single camera feed
"""

import cv2
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QSizePolicy
from PyQt5.QtCore import Qt, QTimer, pyqtSignal
from PyQt5.QtGui import QImage, QPixmap, QPainter, QPen, QColor

class CameraView(QWidget):
    """Widget to display a single camera feed"""
    
    # Signal emitted when this camera view is clicked
    clicked = pyqtSignal(int)
    
    def __init__(self, camera_index, camera_manager):
        super().__init__()
        
        self.camera_index = camera_index
        self.camera_manager = camera_manager
        
        # Initialize UI
        self.init_ui()
        
        # Start update timer
        self.update_timer = QTimer(self)
        self.update_timer.timeout.connect(self.update_frame)
        self.update_timer.start(33)  # ~30 fps
        
    def init_ui(self):
        """Initialize the user interface"""
        # Set up layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Create label to display camera feed
        self.camera_label = QLabel()
        self.camera_label.setAlignment(Qt.AlignCenter)
        self.camera_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.camera_label.setStyleSheet("""
            QLabel {
                background-color: #222;
                border: 1px solid #444;
                color: white;
            }
        """)
        layout.addWidget(self.camera_label)
        
        # Set fixed aspect ratio and minimum size
        self.setMinimumSize(240, 180)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        # Show placeholder initially
        self.show_placeholder()
        
    def set_camera_index(self, index):
        """Set camera index and update display"""
        self.camera_index = index
    
    def update_frame(self):
        """Update the camera frame"""
        if not self.isVisible():
            return
            
        # Check if camera is connected
        if self.camera_manager.is_camera_connected(self.camera_index):
            # Get current frame
            frame = self.camera_manager.get_frame(self.camera_index)
            
            if frame is not None:
                # Convert to RGB format
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                
                # Convert to QImage
                height, width, channels = frame_rgb.shape
                q_image = QImage(frame_rgb.data, width, height, width * channels, QImage.Format_RGB888)
                
                # Convert to QPixmap and scale to fit
                pixmap = QPixmap.fromImage(q_image)
                pixmap = pixmap.scaled(self.camera_label.width(), self.camera_label.height(), 
                                      Qt.KeepAspectRatio, Qt.SmoothTransformation)
                
                # Display the image
                self.camera_label.setPixmap(pixmap)
                return
                
        # If no frame is available or camera is disconnected, show placeholder
        self.show_placeholder()
            
    def show_placeholder(self):
        """Show placeholder when no camera is available"""
        # Get camera configuration
        config = self.camera_manager.config_manager.get_camera_config(self.camera_index)
        
        # Create a placeholder pixmap
        pixmap = QPixmap(self.camera_label.width(), self.camera_label.height())
        pixmap.fill(QColor(40, 40, 40))
        
        # Create a painter to draw on the pixmap
        painter = QPainter(pixmap)
        painter.setPen(QPen(QColor(200, 200, 200)))
        
        # Draw camera name and status
        font = painter.font()
        font.setPointSize(10)
        painter.setFont(font)
        
        camera_name = config.get('name', f"Camera {self.camera_index + 1}")
        
        if config.get('enabled', False):
            status_text = "Connecting..."
        else:
            status_text = "Disabled"
            
        # Draw the text
        painter.drawText(pixmap.rect(), Qt.AlignCenter, 
                        f"{camera_name}\n{status_text}")
        
        # End painting
        painter.end()
        
        # Display the placeholder
        self.camera_label.setPixmap(pixmap)
        
    def mousePressEvent(self, event):
        """Handle mouse click event"""
        self.clicked.emit(self.camera_index)
        super().mousePressEvent(event)
        
    def sizeHint(self):
        """Suggested size for the widget"""
        return self.minimumSize()