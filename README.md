# Shutdown-Scheduler
A cross-platform Python-based **Shutdown Scheduler** with a terminal interface, intelligent suggestions, system tray icon, and customizable timed power actions (like Sleep, Lock, Restart, and Shutdown). Ideal for managing your system’s power efficiently, especially when leaving tasks to run unattended.

---

## ✨ Features

* ✅ Cross-platform (Windows & Linux)
* 🕓 Chain multiple timed commands like sleep, lock, shutdown etc.
* 🌙 Laptop-aware time limit
* 🧠 Smart input parsing (e.g., `0.5 -l 1 -s 1 -rs`)
* 🟢 Interactive prompt with tab completion
* 📌 System tray icon for background presence
* 📁 Automatic logging to `shutdowns.log`
* ⚙️ Uses native system commands

---

## 🧑‍💻 Example Usage

```bash
> 0.1 -l 0.2 -s 0.1 -rs

🕒 This means:
Lock in 6 minutes

Sleep in 18 minutes

Restart in 24 minutes
```
| Command | Description           |
| ------- | --------------------- |
| `-l`    | 🔒 Lock the system    |
| `-s`    | 🌙 Sleep the system   |
| `-rs`   | 🔁 Restart the system |
| `-sd`   | ⏹ Shutdown the system |
| `-h`    | 🆘 Show help          |


### 📦 Requirements
Install dependencies using pip:
```
pip install prompt_toolkit colorama psutil pillow pystray
```

### 🖥 Platform Compatibility
✅ Windows: Uses rundll32 and shutdown.exe

✅ Linux: Uses systemctl, shutdown, and gnome-screensaver-command

```Battery detection used to distinguish laptops vs desktops to limit maximum schedule hours (6 hrs for laptops, 10 hrs for desktops)```

-----
### 🛠 How It Works

Starts a system tray icon in the background with a “Quit” menu.
Prompts the user for input in the format:
<hours> <command> [<hours> <command>] ...
Validates sequence and enforces max cumulative time limit.

Displays a real-time countdown to the next action.

Executes each action at the scheduled time using native system calls.

Logs all actions to shutdowns.log.

### 🧾 Logging
Every action is logged in the shutdowns.log file in the same directory with a timestamp.

Example:
```Auto Lock at 2025-05-17 ::: 21:44:12```
-----
### 💡 Tips
Use decimal values for hours like 0.25 (15 mins), 1.5 (90 mins)

Use -h at any time to view help and command syntax

Kill from tray icon if running silently

CTRL+C during countdown to cancel execution

### 🧊 System Tray
A minimal icon appears in your system tray upon launch.

Right-click and choose "Quit" to stop the scheduler and exit the app.

Useful when the app is minimized or running in the background.
------
### 🧪 Future Improvements (Ideas)
 GUI version with drag-and-drop time sliders

 JSON-based config for recurring tasks

 Sound alarm or toast notifications before execution

 Multi-user profile support

### 🧑‍💻 Author
**(Piyush Golan)
**
### 📜 License
MIT License — free to use, modify, and share.
