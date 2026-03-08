# clipboard_manager/main.py
import signal
import sys
from gui.app import launch_gui


window_ref = {}
monitor_ref = {}

def show_gui():
    """Show the GUI window"""
    if "win" not in window_ref or not window_ref["win"]:
        # Launch GUI if not already running
        win = launch_gui()
        window_ref["win"] = win
        print("GUI launched")
    else:
        # Show existing window
        window_ref["win"].present()
        print("GUI shown")

def signal_handler(signum, frame):
    """Handle signals"""
    if signum == signal.SIGUSR1:
        # Show GUI when Win+V is pressed
        show_gui()
    elif signum in (signal.SIGINT, signal.SIGTERM):
        print("\nShutting down WinClip...")
        if "monitor" in monitor_ref:
            monitor_ref["monitor"].stop()
        sys.exit(0)


if __name__ == "__main__":
    print("WinClip starting...")

    # Register signal handlers
    signal.signal(signal.SIGUSR1, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    if len(sys.argv) > 1 and sys.argv[1] == "--gui":
        win = launch_gui()
        print("GUI launched, main window reference stored")
    else:
        launch_gui()  # For now, always launch GUI. Background mode can be added later.

