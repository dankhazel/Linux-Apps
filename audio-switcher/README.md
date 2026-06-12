# Audio Switcher

A lightweight system tray application for quickly switching between PipeWire audio output devices on Linux.

## Features

- 🔊 Quick audio output switching from system tray
- 🎵 Real-time device detection
- ⚡ Lightweight and fast
- 🎨 Clean, minimal UI with PyQt5
- 🚀 Autostart support

## Requirements

- Python 3.6+
- PyQt5
- PipeWire (with pactl)
- Linux (GNOME, KDE, XFCE, etc.)

## Installation

### Automatic Installation

```bash
cd audio-switcher
chmod +x install.sh
./install.sh
```

This will:
- Install Python dependencies
- Make the app executable
- Create an autostart entry

### Manual Installation

```bash
# Install dependencies
sudo apt install python3 python3-pip python3-pyqt5 pipewire

# Install Python packages
pip3 install -r requirements.txt

# Make executable
chmod +x audio_switcher.py

# Run the app
./audio_switcher.py
```

## Usage

1. **Start the app:**
   ```bash
   ./audio_switcher.py
   ```

2. **From System Tray:**
   - Click the tray icon to see available audio outputs
   - Select a device to switch to it
   - Right-click for menu options (including Exit)

3. **Autostart:**
   The installation script automatically creates a `.desktop` file for autostart. The app will launch on next login.

## Troubleshooting

### "pactl: command not found"
Install PipeWire audio tools:
```bash
sudo apt install pipewire pipewire-audio-client-libraries
```

### "ModuleNotFoundError: No module named 'PyQt5'"
Install PyQt5:
```bash
pip3 install PyQt5
```

### App doesn't appear in tray
- Check if your desktop environment supports system tray
- Try running from terminal to see any error messages
- Make sure the script is executable: `chmod +x audio_switcher.py`

### Devices not showing
- Verify PipeWire is running: `pactl info`
- Check if you have audio devices: `pactl list sinks`

## License

MIT
