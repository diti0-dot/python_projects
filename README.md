Wsl_open
# Voice-Activated WSL Launcher (Windows)

This Python script listens for the phrase "wake up" and triggers a set of actions: it plays a startup audio, a welcome voice, and opens a WSL shortcut. It is designed to run in the background and auto-start when the device is unlocked.

## What It Does

- Uses microphone to detect "wake up"
- Plays two `.wav` audio files
- Launches a WSL `.lnk` shortcut from Desktop
- Times out after 5 minutes if not triggered

## Required Files

- `startup_music.wav` and `welcome_voice.wav` at `C:\welcome_system\`
- `WSL.lnk` shortcut on Desktop

## Python Dependencies

Install required packages:

```bash
pip install SpeechRecognition pyaudio
````


## Run on Unlock

1. Open Task Scheduler
2. Create a new task
3. Trigger: On workstation unlock
4. Action: Start the `.bat` file
5. General: Check "Run with highest privileges"

## Code Overview

* `__init__`: Initializes recognizer, mic, and control variables
* `play_wav()`: Plays `.wav` audio using winsound
* `open_wsl()`: Launches WSL shortcut
* `trigger()`: Coordinates audio and WSL launch
* `listen_for_wake_word()`: Listens for "wake up"
* `run()`: Starts the listening loop and exits on success

