#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Icons for the application
"""

import os
import math
from PyQt5.QtGui import QIcon, QPainter, QColor, QPen, QBrush
from PyQt5.QtCore import Qt, QSize, QRect, QPoint
from PyQt5.QtSvg import QSvgRenderer
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QPixmap

def get_asset_path(filename):
    """Get the full path to an asset file"""
    assets_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(assets_dir, filename)

def get_logo_icon():
    """Get the app logo icon"""
    logo_path = get_asset_path('logo.svg')
    if os.path.exists(logo_path):
        return QIcon(logo_path)
    else:
        # Create a default icon if SVG is not found
        pixmap = QPixmap(64, 64)
        pixmap.fill(Qt.transparent)
        
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Draw camera icon
        painter.setPen(QPen(QColor(50, 150, 250), 2))
        painter.setBrush(QBrush(QColor(50, 150, 250, 100)))
        
        # Camera body
        painter.drawRect(QRect(10, 15, 40, 30))
        
        # Camera lens
        painter.setBrush(QBrush(QColor(30, 100, 200)))
        painter.drawEllipse(QRect(20, 20, 20, 20))
        
        painter.end()
        
        return QIcon(pixmap)

def get_arrow_icon(direction):
    """Get an arrow icon for the given direction"""
    # Create a pixmap
    pixmap = QPixmap(32, 32)
    pixmap.fill(Qt.transparent)
    
    # Create a painter
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.Antialiasing)
    
    # Set pen and brush
    painter.setPen(Qt.NoPen)
    painter.setBrush(QBrush(QColor(180, 180, 220)))
    
    # Define common measurements
    center_x = 16
    center_y = 16
    
    # Calculate points based on direction
    if direction == "left":
        # Arrow pointing left
        points = [
            QPoint(24, 6),   # Top right
            QPoint(8, 16),   # Middle left (point)
            QPoint(24, 26),  # Bottom right
            QPoint(24, 20),  # Bottom indent
            QPoint(18, 16),  # Middle indent
            QPoint(24, 12)   # Top indent
        ]
    elif direction == "right":
        # Arrow pointing right
        points = [
            QPoint(8, 6),    # Top left
            QPoint(24, 16),  # Middle right (point)
            QPoint(8, 26),   # Bottom left
            QPoint(8, 20),   # Bottom indent
            QPoint(14, 16),  # Middle indent
            QPoint(8, 12)    # Top indent
        ]
    elif direction == "up":
        # Arrow pointing up
        points = [
            QPoint(6, 24),   # Bottom left
            QPoint(16, 8),   # Middle top (point)
            QPoint(26, 24),  # Bottom right
            QPoint(20, 24),  # Right indent
            QPoint(16, 18),  # Middle indent
            QPoint(12, 24)   # Left indent
        ]
    elif direction == "down":
        # Arrow pointing down
        points = [
            QPoint(6, 8),    # Top left
            QPoint(16, 24),  # Middle bottom (point)
            QPoint(26, 8),   # Top right
            QPoint(20, 8),   # Right indent
            QPoint(16, 14),  # Middle indent
            QPoint(12, 8)    # Left indent
        ]
    
    # Draw filled polygon
    painter.drawPolygon(points)
    
    # Add a subtle outline
    painter.setPen(QPen(QColor(140, 140, 190), 1))
    painter.drawPolyline(points)
    
    painter.end()
    
    return QIcon(pixmap)

def get_config_icon():
    """Get a configuration/gear icon"""
    # Create a pixmap
    pixmap = QPixmap(24, 24)
    pixmap.fill(Qt.transparent)
    
    # Create a painter
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.Antialiasing)
    
    # Set pen and brush
    painter.setPen(QPen(QColor(220, 220, 220), 1))
    painter.setBrush(QBrush(QColor(180, 180, 180)))
    
    # Draw gear
    center_x = 12
    center_y = 12
    outer_radius = 10
    inner_radius = 5
    tooth_count = 8
    
    # Draw outer circle with teeth
    path = []
    for i in range(tooth_count * 2):
        angle = 2 * math.pi * i / (tooth_count * 2)
        radius = outer_radius if i % 2 == 0 else outer_radius - 3
        x = center_x + radius * math.cos(angle)
        y = center_y + radius * math.sin(angle)
        path.append(QPoint(int(x), int(y)))
    
    painter.drawPolygon(path)
    
    # Draw inner circle
    painter.setBrush(QBrush(QColor(50, 50, 50)))
    painter.drawEllipse(QPoint(center_x, center_y), inner_radius, inner_radius)
    
    painter.end()
    
    return QIcon(pixmap)

def get_back_icon():
    """Get a back/return icon"""
    # Create a pixmap
    pixmap = QPixmap(24, 24)
    pixmap.fill(Qt.transparent)
    
    # Create a painter
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.Antialiasing)
    
    # Set pen
    painter.setPen(QPen(QColor(220, 220, 220), 2))
    
    # Draw back arrow
    points = [
        QPoint(16, 6),
        QPoint(8, 12),
        QPoint(16, 18),
        QPoint(8, 12),
        QPoint(18, 12)
    ]
    painter.drawLines(points)
    
    painter.end()
    
    return QIcon(pixmap)

def sin(x):
    """Simple sine function"""
    return math.sin(x)

def cos(x):
    """Simple cosine function"""
    return math.cos(x)