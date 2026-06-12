#!/bin/bash

# Audio Switcher Installation Script
# Installs audio-switcher and its dependencies

set -e

echo "Installing audio-switcher..."

# Check for required commands
echo "Checking dependencies..."

command -v python3 >/dev/null 2>&1 || { echo "python3 is required but not installed."; exit 1; }
command -v pactl >/dev/null 2>&1 || { echo "pactl (PipeWire) is required but not installed."; exit 1; }
command -v pip3 >/dev/null 2>&1 || { echo "pip3 is required but not installed."; exit 1; }

echo "✓ All dependencies found"

# Install Python packages
echo "Installing Python packages..."
pip3 install -r requirements.txt

# Make the script executable
echo "Making audio_switcher.py executable..."
chmod +x audio_switcher.py

# Create autostart directory if it doesn't exist
mkdir -p ~/.config/autostart

# Create .desktop file for autostart
echo "Creating .desktop file for autostart..."
cat > ~/.config/autostart/audio-switcher.desktop << 'EOF'
[Desktop Entry]
Type=Application
Name=Audio Switcher
Comment=PipeWire Audio Output Switcher
Exec=$HOME/Linux-Apps/audio-switcher/audio_switcher.py
Icon=audio-card
Terminal=false
Categories=Utility;Audio;
StartupNotify=false
EOF

echo "✓ Installation complete!"
echo ""
echo "Audio Switcher has been installed successfully."
echo "It will start automatically on next login."
echo ""
echo "To start it now, run: ./audio_switcher.py"
