# WinClip

WinClip is a GTK4 clipboard manager for Linux with persistent history, pinning, one-click paste, and a background session mode that can be summoned on demand.

![WinClip screenshot](screenshot.png)

## Features

- Clipboard history stored in SQLite
- Pin and unpin important clips
- One-click paste for saved entries
- Background mode with hidden startup
- Show-on-demand UI using `--show`
- Login startup through a user `systemd` service

## Requirements

- Python 3.12+
- GTK4 / PyGObject
- `xclip`
- `wl-copy` on Wayland
- `ydotool` for simulated paste

## Installation

```bash
git clone https://github.com/Allaye/winclip.git
cd winclip
./setup_shortcut.sh
```

The setup script:

- installs Python dependencies with `uv sync` when available
- falls back to `pip3 install -e .`
- installs required system packages on Debian/Ubuntu systems
- installs and enables the user `systemd` service

Run the UI with:

```bash
python3 main.py --show
```

If you prefer a manual Python install:

```bash
pip install -e .
```

Then run:

```bash
python3 main.py --show
```

## Usage

Show the UI:

```bash
python3 main.py --show
```

Start in background mode:

```bash
python3 main.py --daemon
```

After the window is closed, it hides and can be shown again with:

```bash
python3 main.py --show
```

## Autostart And Shortcut

Install the user service:

```bash
./setup_shortcut.sh
```

This installs:

- `winclip.service` into `~/.config/systemd/user`

Recommended keyboard shortcut command:

```bash
python3 /path/to/winclip/main.py --show
```

Use the full absolute path for desktop shortcuts so the command works outside the repository directory.

Check the background service:

```bash
systemctl --user status winclip.service
```

## Notes

- On Wayland, clipboard writing uses `wl-copy`.
- Standard paste currently targets editor-style paste behavior.
- Many terminals use `Ctrl+Shift+V` instead of `Ctrl+V`.

## License

MIT. See `LICENSE.txt`.
