"""WinClip entry point.

Usage:
    python main.py --daemon   Start with GUI hidden (background mode).
    python main.py --show     Start and present the window.
    python main.py --gui      Alias for --show.
"""

import sys
from app.app import start_app


def main():
    """Parse CLI arguments and launch the application."""
    mode = sys.argv[1] if len(sys.argv) > 1 else "--show"

    if mode == "--daemon":
        start_app(hide_gui=True)
    elif mode in {"--show", "--gui"}:
        start_app(hide_gui=False)
    else:
        print("Usage: python main.py [--daemon|--show|--gui]")
        sys.exit(2)


if __name__ == "__main__":
    main()
