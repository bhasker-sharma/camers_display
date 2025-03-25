#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Camera Manager
Handles camera connections and video streaming
"""

import threading
import time
import cv2
import logging
import queue
import numpy as np
from PyQt5.QtCore import QObject, pyqtSignal

class CameraThread(threading.Thread):
    """Thread for capturing frames from a camera"""
    
    def __init__(self, camera_index, config):
        """Initialize the camera thread"""
        super().__init__()
        self.daemon = True  # Thread will close when program exits
        
        self.camera_index = camera_index
        self.config = config
        self.running = False
        self.connected = False
        
        # Queue to store recent frames
        self.frame_queue = queue.Queue(maxsize=2)
        
        # Last frame captured
        self.latest_frame = None
        
        # Connection timeout (in seconds)
        self.timeout = 5
        
    def run(self):
        """Main thread function"""
        self.running = True
        
        # Skip if camera is disabled
        if not self.config.get('enabled', False):
            logging.info(f"Camera {self.camera_index + 1} is disabled.")
            return
            
        # Create video capture based on source type
        if self.config.get('source_type') == 'rtsp':
            # RTSP stream
            url = self.config.get('url', '')
            if not url:
                logging.error(f"Camera {self.camera_index + 1}: RTSP URL is empty.")
                return
                
            # Configure capture with appropriate settings for RTSP
            cap = cv2.VideoCapture(url)
            cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)  # Minimize buffering for lower latency
            
        else:
            # Local camera
            device_id = self.config.get('device', 0)
            cap = cv2.VideoCapture(device_id)
        
        # Check if camera opened successfully
        if not cap.isOpened():
            logging.error(f"Camera {self.camera_index + 1}: Failed to open camera.")
            return
            
        # Connection successful
        self.connected = True
        logging.info(f"Camera {self.camera_index + 1}: Connected successfully.")
        
        # Read frames in a loop
        read_failures = 0
        while self.running:
            try:
                # Read a frame
                ret, frame = cap.read()
                
                if not ret:
                    read_failures += 1
                    # Retry for a few times before giving up
                    if read_failures > 5:
                        logging.warning(f"Camera {self.camera_index + 1}: Connection lost.")
                        self.connected = False
                        break
                    time.sleep(0.5)
                    continue
                    
                # Reset failure counter on successful read
                read_failures = 0
                
                # Store the frame
                self.latest_frame = frame
                
                # Also try to put in queue (non-blocking to avoid freezing if queue is full)
                try:
                    self.frame_queue.put(frame, block=False)
                except queue.Full:
                    # Just skip if the queue is full (clear the oldest frame)
                    try:
                        self.frame_queue.get(block=False)
                        self.frame_queue.put(frame, block=False)
                    except queue.Empty:
                        pass
                
                # Small sleep to avoid high CPU usage
                time.sleep(0.03)  # ~30 fps
                
            except Exception as e:
                logging.error(f"Camera {self.camera_index + 1}: Error reading frame: {e}")
                time.sleep(1)  # Pause before retrying
        
        # Clean up
        cap.release()
        self.connected = False
        logging.info(f"Camera {self.camera_index + 1}: Disconnected.")
        
    def get_frame(self):
        """Get the current frame"""
        # Use the frame from the queue if available (more recent)
        try:
            return self.frame_queue.get(block=False)
        except queue.Empty:
            # Otherwise use the latest frame we have
            return self.latest_frame
            
    def stop(self):
        """Stop the camera thread"""
        self.running = False
        # Wait for the thread to finish (with timeout)
        if self.is_alive():
            self.join(timeout=1.0)


class CameraManager(QObject):
    """Manages all camera connections and provides frames"""
    
    # Signal emitted when camera connection status changes
    camera_status_changed = pyqtSignal(int, bool)
    
    def __init__(self, config_manager):
        """Initialize the camera manager"""
        super().__init__()
        
        self.config_manager = config_manager
        
        # Dictionary to store camera threads by index
        self.camera_threads = {}
        
        # Load configurations and start threads
        self.reload_config()
        
    def reload_config(self):
        """Reload camera configurations and restart threads"""
        # Stop all running threads
        self.stop_all_cameras()
        
        # Clear the threads dictionary
        self.camera_threads.clear()
        
        # Start threads for all enabled cameras
        for i in range(48):  # 48 cameras max
            config = self.config_manager.get_camera_config(i)
            if config.get('enabled', False):
                # Start a thread for this camera
                thread = CameraThread(i, config)
                thread.start()
                self.camera_threads[i] = thread
                logging.info(f"Started thread for camera {i + 1}")
            else:
                logging.info(f"Camera {i + 1} is disabled, not starting thread")
                
    def get_frame(self, camera_index):
        """Get the latest frame from a camera"""
        if camera_index in self.camera_threads and self.camera_threads[camera_index].connected:
            return self.camera_threads[camera_index].get_frame()
        return None
        
    def is_camera_connected(self, camera_index):
        """Check if a camera is connected"""
        return (camera_index in self.camera_threads and 
                self.camera_threads[camera_index].connected)
    
    def stop_camera(self, camera_index):
        """Stop a specific camera thread"""
        if camera_index in self.camera_threads:
            self.camera_threads[camera_index].stop()
            del self.camera_threads[camera_index]
            logging.info(f"Stopped thread for camera {camera_index + 1}")
    
    def stop_all_cameras(self):
        """Stop all camera threads"""
        for camera_index in list(self.camera_threads.keys()):
            self.stop_camera(camera_index)
        logging.info("Stopped all camera threads")