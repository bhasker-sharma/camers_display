#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Multi-Camera Monitoring Application
Main Entry Point
"""

import sys
import logging

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt

from ui.camera_grid import CameraGridWindow

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def main():
    """Main entry point for the application"""
    # Create application
    app = QApplication(sys.argv)
    
    # Set application name and organization
    app.setApplicationName("Tuyere Camera Monitoring System")
    app.setOrganizationName("TIPL")
    
    # Create the main window
    window = CameraGridWindow()
    
    # Show the window
    window.show()
    
    # Run the application event loop
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()