#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Configuration Manager
Handles storing and retrieving camera configurations
"""

import os
import json
import logging
import time
import cv2

class ConfigManager:
    """Manages camera configurations"""
    
    def __init__(self, config_file="camera_config.json"):
        """Initialize with the configuration file path"""
        self.config_file = config_file
        self.config = self.load_config()
        
    def load_config(self):
        """Load configuration from file"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError) as e:
                logging.error(f"Failed to read config file: {e}")
                return self.get_default_config()
        else:
            # Create a default configuration
            config = self.get_default_config()
            self.save_config()
            return config
            
    def save_config(self):
        """Save configuration to file"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=4)
            return True
        except IOError as e:
            logging.error(f"Failed to write config file: {e}")
            return False
            
    def get_default_config(self):
        """Get default configuration"""
        # Default configuration with 48 disabled cameras
        return {
            "cameras": [
                {
                    "enabled": False,
                    "source_type": "rtsp",  # 'rtsp' or 'local'
                    "url": "",
                    "device": 0,
                    "name": f"Camera {i+1}"
                } for i in range(48)
            ]
        }
        
    def get_camera_config(self, camera_index):
        """Get configuration for a specific camera"""
        if 0 <= camera_index < len(self.config["cameras"]):
            return self.config["cameras"][camera_index]
        else:
            # Return a default camera config if the index is out of range
            return {
                "enabled": False,
                "source_type": "rtsp",
                "url": "",
                "device": 0,
                "name": f"Camera {camera_index+1}"
            }
            
    def set_camera_config(self, camera_index, camera_config):
        """Set configuration for a specific camera"""
        if 0 <= camera_index < len(self.config["cameras"]):
            self.config["cameras"][camera_index] = camera_config
            self.save_config()
            return True
        return False
        
    def test_camera_connection(self, camera_index, config):
        """Test connection to a camera with the given configuration"""
        try:
            if config["source_type"] == "rtsp":
                if not config["url"]:
                    return False, "RTSP URL is empty"
                
                # Try to open the RTSP stream
                cap = cv2.VideoCapture(config["url"])
                success = cap.isOpened()
                
                if success:
                    # Try to read a frame
                    ret, frame = cap.read()
                    success = ret
                
                # Release the capture
                cap.release()
                
                if not success:
                    return False, "Failed to connect to RTSP stream"
                    
                return True, "Connection successful"
                
            else:  # Local camera
                device_id = config["device"]
                
                # Try to open the local camera
                cap = cv2.VideoCapture(device_id)
                success = cap.isOpened()
                
                if success:
                    # Try to read a frame
                    ret, frame = cap.read()
                    success = ret
                
                # Release the capture
                cap.release()
                
                if not success:
                    return False, f"Failed to connect to local camera device {device_id}"
                    
                return True, "Connection successful"
                
        except Exception as e:
            return False, f"Error testing connection: {str(e)}"