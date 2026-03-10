# clipboard_manager/main.py
import sys
from app.app import start_app


if __name__ == "__main__":
    print("WinClip starting...")

    mode = sys.argv[1] if len(sys.argv) > 1 else "--show"

    if mode == "--daemon":
        start_app(hide_gui=True)
    elif mode in {"--show", "--gui"}:
        start_app(hide_gui=False)
    else:
        print("Usage: python main.py [--daemon|--show|--gui]")
        sys.exit(2)

        