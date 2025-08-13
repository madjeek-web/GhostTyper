# === LIBRARY IMPORT ===
import keyboard  # Allows monitoring and simulating keyboard strokes
import time  # Handles timing (pauses between actions)
from datetime import datetime  # Provides current time for encryption
import random  # Generates random values for paranoia mode
import win32api  # Windows interface (process management)
import win32con  # Contains Windows constants (access rights)
import win32process  # Advanced process manipulation
import win32security  # Windows permissions management
import wmi  # Spyware detection (keyloggers)

# === MAIN CONFIGURATION ===
STEALTH_MODE = True   # True = invisible program (no visible window)
PARANOIA_MODE = True  # True = sends random fake keystrokes
ANTI_KEYLOGGER = True # True = automatically kills known keyloggers

# === TEMPORAL ENCRYPTION FUNCTION ===
def get_time_key():
    """Generates an encryption key based on current time
       Returns a number between 0 and 255 that changes every second"""
    now = datetime.now()  # Gets exact time
    # Converts time to seconds and applies modulo 256
    return (now.hour * 3600 + now.minute * 60 + now.second) % 256

# === KEY TRANSFORMATION FUNCTION ===
def get_shifted_char(c):
    """Transforms each typed key according to the temporal key
       c = original character (a-z, A-Z, 0-9)
       Returns the encrypted character"""
    shift = get_time_key()  # Gets current time key
    
    if c.isalpha():  # If it's a letter
        # Determines whether uppercase or lowercase
        base = ord('a') if c.islower() else ord('A')
        # Applies shift and loops through the alphabet
        return chr((ord(c) - base + shift) % 26 + base)
    
    elif c.isdigit():  # If it's a digit
        # Applies shift and loops from 0 to 9
        return str((int(c) + shift) % 10)
    
    return c  # Returns unchanged character if non-alphanumeric

# === ANTI-KEYLOGGER FUNCTION ===
def kill_keyloggers():
    """Detects and kills suspicious processes"""
    c = wmi.WMI()  # Connects to Windows management API
    
    # List of common malicious process names
    blacklist = ["keylogger", "logkeys", "spytech", "ahk"]
    
    # Scans all running processes
    for proc in c.Win32_Process():
        # Checks if name matches spyware
        if any(name in proc.Name.lower() for name in blacklist):
            try:
                # Forces process termination
                process = win32api.OpenProcess(
                    win32con.PROCESS_TERMINATE,  # Permission to kill process
                    0,  # Don't inherit permissions
                    proc.ProcessId  # ID of process to terminate
                )
                win32api.TerminateProcess(process, 0)  # Kills process
            except:
                pass  # If error occurs, continues without crashing

# === PARANOIA MODE (FAKE KEYSTROKES) ===
def random_typing():
    """Sends random keystrokes to confuse keyloggers"""
    while PARANOIA_MODE:  # Runs in loop while mode is active
        # Waits random delay between 5 and 30 seconds
        time.sleep(random.randint(5, 30))
        # Generates between 1 and 5 random characters
        fake_chars = ''.join(
            random.choice('abcdefghijklmnopqrstuvwxyz1234567890')
            for _ in range(random.randint(1, 5))
        # Sends fake keystrokes
        keyboard.write(fake_chars)

# === KEY CAPTURE ===
def on_key_event(e):
    """Function called on each keystroke"""
    if e.event_type == keyboard.KEY_DOWN:  # If it's a key press
        # Gets encrypted version of the key
        encrypted_char = get_shifted_char(e.name)
        # Sends encrypted key instead of original
        keyboard.write(encrypted_char)
        return False  # Prevents sending real key
    return True  # Allows other keyboard events

# === PROGRAM ENTRY POINT ===
if __name__ == "__main__":
    import threading  # Allows running multiple tasks in parallel
    
    # Activates keylogger cleaning (if configured)
    if ANTI_KEYLOGGER:
        # Runs in background in separate thread
        threading.Thread(target=kill_keyloggers, daemon=True).start()
    
    # Activates paranoia mode (if configured)
    if PARANOIA_MODE:
        # Runs in another thread
        threading.Thread(target=random_typing, daemon=True).start()
    
    # Activates keyboard monitoring
    keyboard.hook(on_key_event)
    
    # Keeps program running indefinitely
    keyboard.wait()


# Key Points to Remember:

# Libraries: Each import has specific purpose (keyboard, security, etc.)
# Functions:
# get_time_key() → Creates unique time-based key
# get_shifted_char() → Transforms keys in real-time
# kill_keyloggers() → Protects against spies
# random_typing() → Confuses loggers
# Threads: Allows doing multiple things simultaneously
# Configuration: Modifiable at top of file


# This code is commented: each section explains its own functionality! 🚀
