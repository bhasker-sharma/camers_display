#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Stylesheet for the application
"""

def get_stylesheet():
    """Return the application stylesheet"""
    return """
        /* Global styles */
        QMainWindow, QDialog {
            background-color: #2a2a2a;
            color: #e0e0e0;
        }
        
        QLabel {
            color: #e0e0e0;
        }
        
        QWidget {
            color: #e0e0e0;
        }
        
        QPushButton {
            background-color: #3a3a3a;
            color: #e0e0e0;
            border: 1px solid #505050;
            border-radius: 4px;
            padding: 5px 10px;
            min-height: 20px;
        }
        
        QPushButton:hover {
            background-color: #454545;
            border: 1px solid #606060;
        }
        
        QPushButton:pressed {
            background-color: #353535;
        }
        
        QPushButton:checked {
            background-color: #4a6da7;
            border: 1px solid #6080c0;
        }
        
        QLineEdit, QSpinBox, QComboBox {
            background-color: #3a3a3a;
            color: #e0e0e0;
            border: 1px solid #505050;
            border-radius: 4px;
            padding: 3px;
            selection-background-color: #4a6da7;
        }
        
        QComboBox::drop-down {
            border: 0px;
            width: 20px;
        }
        
        QComboBox::down-arrow {
            image: url(dropdown.png);
            width: 12px;
            height: 12px;
        }
        
        QGroupBox {
            border: 1px solid #505050;
            border-radius: 4px;
            margin-top: 10px;
            padding-top: 10px;
        }
        
        QGroupBox::title {
            subcontrol-origin: margin;
            subcontrol-position: top center;
            padding: 0 5px;
            color: #e0e0e0;
        }
        
        /* Navigation bar */
        #navbar-title {
            font-size: 14pt;
            font-weight: bold;
            color: #e0e0e0;
        }
        
        #screen-label {
            font-size: 12pt;
            color: #a0a0a0;
        }
        
        #nav-button {
            background-color: #3a3a3a;
            border: 1px solid #505050;
            border-radius: 4px;
            padding: 5px;
            min-width: 30px;
            min-height: 30px;
        }
        
        #nav-button:hover {
            background-color: #454545;
            border: 1px solid #606060;
        }
        
        /* Camera view */
        QLabel[objectName="camera-view"] {
            background-color: #1a1a1a;
            border: 1px solid #303030;
            color: #808080;
        }
    """