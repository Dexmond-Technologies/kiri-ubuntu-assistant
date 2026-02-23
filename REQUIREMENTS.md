# Kiri Voice Assistant Requirements

This program requires the following packages to function properly. 
When packaged as a .deb file, tell people to install it using `gdebi` (e.g., `sudo gdebi kiri.deb`). This will automatically install the program along with all these listed dependencies.

## Core Python & Audio Dependencies
- python3
- python3-speechrecognition
- python3-pyttsx3
- python3-pyaudio (needed for microphone input)
- espeak (needed by pyttsx3 for text-to-speech engines on Linux)
- flac (often required by speech_recognition for audio processing)
- transformers (needed for Conversational AI fallback)
- torch (needed for Conversational AI fallback)

## System Utilities
- alsa-utils (provides `amixer` for volume control commands)
- policykit-1 (provides `pkexec` for system shutdown/reboot/update)
- libglib2.0-bin (provides `gio` to empty the trash)

## GNOME & Desktop Applications (Called by Voice Commands)
- gnome-terminal
- gnome-screensaver
- gnome-system-monitor
- nautilus
- thunderbird
- gimp
- gnome-calculator
- google-chrome-stable
- gnome-control-center
- gedit
- gnome-calendar
- gnome-weather
- gnome-maps
- totem
- rhythmbox
- eog
- cheese
- gnome-screenshot
- libreoffice
- gnome-software
- gnome-disk-utility (provides `gnome-disks`)
- evince

## Running from Source (Manual Installation)
If you are downloading the source code directly and running `kiri.py` without a `.deb` package, you will need to install the dependencies manually.

First, install the system dependencies using APT:
```bash
sudo apt update
sudo apt install python3 python3-pip python3-pyaudio espeak flac alsa-utils policykit-1 libglib2.0-bin
```

Then, install the required Python packages using pip:
```bash
pip install SpeechRecognition pyttsx3 transformers torch --break-system-packages
```

Ensure all GNOME utilities you intend to use are installed on your system (most come pre-installed on Ubuntu).
