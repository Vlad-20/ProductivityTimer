# ProductivityTimer

A simple timer that *actually* tells you where your time went. It tracks your work time, but more importantly, it tracks your "just a second" pause time.

## The Big Idea

Ever set a 25-minute timer, paused it to grab a coffee and come back 15 minutes later? Your timer still says 25:00, but your focus is gone and your "session" was secretly 40 minutes long.

This app should fix that.

It was inspired by [this video](https://www.youtube.com/watch?v=JWwBcy0eFBg), but with a key feature: **a pause-time tracker**. It logs every second you spend in 'pause' mode, so when your session is over, you see two things:

1. **Effective Time**: How long you were actually working.

2. **Pause Time**: How long you were procrastinating (or, you know, "on break").

The final log gives you the total session time (Work + Pause) for an honest look at your focus.

## How to Run this App

This app is built with Python 3 and its built-in `tkinter` library, so you don't need to install any special packages.

1. **Clone the Repository**: Get the files onto your machine.

```
git clone https://github.com/Vlad-20/ProductivityTimer.git
```


2. **Navigate to the Directory**:

```
cd ProductivityTimer
```


3. **Run the App**:

```
python3 productivity_timer.py
```

*(**Note**: If you're on a minimal Linux distro, you might need to install the `tkinter` module separately with `sudo apt-get install python3-tk`)*

## How to Use the App (Tutorial)

Using the app is a simple 3-step process:

**Step 1: Setup Your Session**

On the main window, you have two tasks:

- **Set Time**: Enter your desired work time in `HH:MM:SS` format. (Note: MM and SS must be 59 or less).

- **Set Log File**: Click "Browse" and choose a folder. The app will automatically suggest the name `productivity_log.txt` for you.

**Step 2: Run the Timer**

Hit **Start**. A new, clean window will appear showing your countdown. You have two options:

- **Pause**: This stops your main countdown and starts a counter tracking your pause time. Click "Resume" (the same button) to get back to work.

- **Stop**: This ends the session immediately.

**Step 3**: Review Your Log

When you hit "Stop" (or the timer finishes naturally), the app does two things:

1. It instantly saves your session data to the productivity_log.txt file you chose.

2. It sends you back to the main screen, ready for your next session.

Your log file will look something like this, giving you the complete picture of your session:

```
==============================
Session Logged: 2025-11-05 18:30:00
Initial Time Set:   00:45:00
Effective Time Run: 00:32:10
Total Time Paused:  00:08:15
Total Session Time: 00:40:25
==============================
```

