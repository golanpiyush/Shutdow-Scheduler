import time
import os
import sys
import platform
from datetime import datetime
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from colorama import just_fix_windows_console, init, Fore
import threading
from PIL import Image, ImageDraw
import pystray
import psutil

# Setup console colors
just_fix_windows_console()
init(autoreset=True)


def is_laptop():
    return psutil.sensors_battery() is not None

def is_windows():
    return platform.system().lower() == "windows"


# Windows & Linux actions
ACTION_COMMANDS = {
    "-rs": ("Restart", "shutdown /r /t 0" if is_windows() else "reboot"),
    "-s":  ("Sleep", "rundll32.exe powrprof.dll,SetSuspendState 0,1,0" if is_windows() else "systemctl suspend"),
    "-l":  ("Lock", "rundll32.exe user32.dll,LockWorkStation" if is_windows() else "gnome-screensaver-command -l"),
    "-sd": ("Shutdown", "shutdown /s /t 0" if is_windows() else "shutdown now"),
}

completer = WordCompleter(list(ACTION_COMMANDS.keys()) + ["-h"], ignore_case=True)


def show_help():
    print(Fore.CYAN + "\nAvailable Commands:\n")
    for cmd, (desc, _) in ACTION_COMMANDS.items():
        print(Fore.YELLOW + f"  {cmd:<5} → {desc}")
    time.sleep(0.5)
    print(Fore.CYAN + "\nUsage Example:")
    print(Fore.WHITE + "  > 0.1 -l 0.2 -s 0.1 -rs\n")
    print(Fore.CYAN + "This means:")
    print(Fore.WHITE + "  → Lock in 6 mins, Sleep at 18 mins, Restart at 24 mins\n")
    print(Fore.RED + " P.S → The script records the logs in shutdown.log file.\n")
    time.sleep(1)

def format_time(seconds_left):
    hrs = seconds_left // 3600
    mins = (seconds_left % 3600) // 60
    secs = seconds_left % 60
    return f"{hrs:02}:{mins:02}:{secs:02}"

def log_action(action):
    with open("shutdowns.log", "a") as f:
        f.write(f"Auto {action} at {datetime.now().strftime('%Y-%m-%d ::: %H:%M:%S')}\n")

def create_tray_icon():
    image = Image.new("RGB", (64, 64), (0, 0, 0))
    draw = ImageDraw.Draw(image)
    draw.ellipse((16, 16, 48, 48), fill="red")

    def on_quit(icon, item):
        print("\n[TRAY]: Exiting app.")
        icon.stop()
        os._exit(0)

    menu = pystray.Menu(pystray.MenuItem("Quit", on_quit))
    icon = pystray.Icon("Shutdown Scheduler", image, "Shutdown Scheduler", menu)
    icon.run()

def parse_input_sequence():
    max_hours = 6 if is_laptop() else 10
    max_seconds = max_hours * 3600

    while True:
        user_input = prompt("> ", completer=completer).strip()

        if user_input.lower() == "-h":
            show_help()
            continue

        parts = user_input.split()

        if len(parts) % 2 != 0:
            print(Fore.RED + "[ERROR]: Invalid format. Use: <hours> <command> ...\n")
            continue

        schedule = []
        cumulative = 0
        valid = True

        for i in range(0, len(parts), 2):
            try:
                delay = float(parts[i])
                command = parts[i + 1].lower()

                if command == "-h":
                    print(Fore.YELLOW + "[INFO]: '-h' is only used to display help.\n")
                    valid = False
                    break

                if command not in ACTION_COMMANDS:
                    print(Fore.RED + f"[ERROR]: Unknown command: {command}\n")
                    valid = False
                    break

                seconds = int(delay * 3600)
                cumulative += seconds

                if cumulative > max_seconds:
                    print(Fore.RED + f"[ERROR]: Total delay cannot exceed {max_hours} hours on this system.\n")
                    valid = False
                    break

                schedule.append((cumulative, command))

            except ValueError:
                print(Fore.RED + f"[ERROR]: Invalid time value: {parts[i]}\n")
                valid = False
                break

        if valid:
            return schedule, cumulative


def perform_action(command):
    action_text, system_command = ACTION_COMMANDS[command]
    log_action(action_text)
    print(Fore.RED + f"\n[WARNING]: Use CTRL+C to prevent system from {action_text} now.\n")

    time.sleep(5)
    os.system(system_command)


def countdown_and_execute(schedule, total_time):
    print(Fore.GREEN + f"\n[SYSTEM]: Schedule loaded.")
    for seconds, command in schedule:
        action_name = ACTION_COMMANDS[command][0]
        print(Fore.YELLOW + f"[NOTICE]: → System will auto {action_name} in {format_time(seconds)}\n")

    trigger_map = dict(schedule)
    time_elapsed = 0

    while time_elapsed <= total_time:
        if time_elapsed in trigger_map:
            perform_action(trigger_map[time_elapsed])
            time.sleep(1)

        remaining = total_time - time_elapsed
        next_command = next((cmd for sec, cmd in schedule if sec >= time_elapsed), None)
        next_action = ACTION_COMMANDS[next_command][0] if next_command else "Complete"

        sys.stdout.write(Fore.WHITE + f"\r[SYSTEM]: Time left to {next_action}: {format_time(remaining)}")
        sys.stdout.flush()
        time.sleep(1)
        time_elapsed += 1

    print(Fore.GREEN + "\n\nAll scheduled tasks completed.")


# Main
if __name__ == "__main__":
    threading.Thread(target=create_tray_icon, daemon=True).start()

    try:
        print(Fore.CYAN + "Enter sequence like: 2 -s 4 -rs 1 -sd")
        schedule, total_time = parse_input_sequence()
        countdown_and_execute(schedule, total_time)

    except KeyboardInterrupt:
        print(Fore.YELLOW + "\nExecution cancelled by user.")
        time.sleep(2)
