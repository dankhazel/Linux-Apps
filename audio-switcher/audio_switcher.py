#!/usr/bin/env python3

import sys
import subprocess
from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu
from PyQt5.QtGui import QIcon, QColor
from PyQt5.QtCore import Qt, QTimer

class AudioSwitcher:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.setup_tray()
        
    def setup_tray(self):
        """Setup system tray icon and menu"""
        self.tray = QSystemTrayIcon()
        self.tray.setIcon(self.create_icon())
        
        self.menu = QMenu()
        self.refresh_devices()
        
        self.menu.addSeparator()
        exit_action = self.menu.addAction("Exit")
        exit_action.triggered.connect(self.app.quit)
        
        self.tray.setContextMenu(self.menu)
        self.tray.show()
        
        # Refresh devices every 2 seconds
        timer = QTimer()
        timer.timeout.connect(self.refresh_devices)
        timer.start(2000)
    
    def create_icon(self):
        """Create a simple speaker icon"""
        from PyQt5.QtGui import QPixmap, QPainter
        pixmap = QPixmap(64, 64)
        pixmap.fill(QColor(255, 255, 255, 0))
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(20, 16, 24, 32, QColor(0, 120, 215))
        painter.end()
        return QIcon(pixmap)
    
    def get_audio_devices(self):
        """Get list of PipeWire audio output devices"""
        try:
            result = subprocess.run(
                ['pactl', 'list', 'sinks'],
                capture_output=True,
                text=True,
                check=True
            )
            
            devices = {}
            current_device = None
            
            for line in result.stdout.split('\n'):
                if line.startswith('Sink #'):
                    current_device = line.split('#')[1].strip()
                elif 'device.description' in line and current_device:
                    desc = line.split('"')[1]
                    devices[current_device] = desc
            
            return devices
        except Exception as e:
            print(f"Error getting devices: {e}")
            return {}
    
    def get_default_device(self):
        """Get the default audio output device"""
        try:
            result = subprocess.run(
                ['pactl', 'info'],
                capture_output=True,
                text=True,
                check=True
            )
            
            for line in result.stdout.split('\n'):
                if 'Default Sink:' in line:
                    return line.split(':')[1].strip()
            return None
        except Exception as e:
            print(f"Error getting default device: {e}")
            return None
    
    def switch_device(self, device_id):
        """Switch to a specific audio device"""
        try:
            subprocess.run(
                ['pactl', 'set-default-sink', device_id],
                check=True
            )
        except Exception as e:
            print(f"Error switching device: {e}")
    
    def refresh_devices(self):
        """Refresh the device list in the menu"""
        devices = self.get_audio_devices()
        default = self.get_default_device()
        
        # Clear existing actions (except separator and exit)
        while self.menu.actions() and self.menu.actions()[0].text() != '':
            self.menu.removeAction(self.menu.actions()[0])
        
        if not devices:
            self.menu.addAction("No devices found")
            return
        
        # Add device actions
        for device_id, description in devices.items():
            action = self.menu.addAction(description)
            
            # Mark default device with checkmark
            if device_id == default:
                action.setCheckable(True)
                action.setChecked(True)
            
            # Create lambda to capture device_id
            action.triggered.connect(
                lambda checked=False, d=device_id: self.switch_device(d)
            )
    
    def run(self):
        """Run the application"""
        sys.exit(self.app.exec_())

if __name__ == '__main__':
    switcher = AudioSwitcher()
    switcher.run()
