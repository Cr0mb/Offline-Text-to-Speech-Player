# Offline-Text-to-Speech-Player
This is a simple offline Text-to-Speech (TTS) desktop application built with Python, Tkinter, pyttsx3, and pygame. It allows users to convert written text into spoken audio without requiring an internet connection.

## Features
- Fully offline text-to-speech conversion

- Play, pause, and resume controls

- Clean graphical user interface using Tkinter

- Scrollable text input area

- Temporary audio files are automatically cleaned up after playback

- "Download" option to permanently save audio file

## Requirements
- Python 3.7 or newer
```
pip install pyttsx3 pygame tkinter
```

## Notes
- Only one audio playback is supported at a time

- Ensure your system audio is not muted or in use by another application

- The application deletes generated audio files after playback ends or is stopped - must press "download" to save permanently.

![image](https://github.com/user-attachments/assets/c2b9afa2-0e17-4225-a145-128ff5c54d39)
