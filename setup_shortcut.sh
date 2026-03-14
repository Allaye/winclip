#!/bin/bash

set -e

# WinClip Keyboard Shortcut Setup Script

echo "Setting up WinClip keyboard shortcut..."
echo ""
echo ""

# Get the current directory
WINCLIP_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SHOW_COMMAND="python3 $WINCLIP_DIR/main.py --show"
SERVICE_SOURCE="$WINCLIP_DIR/winclip.service"
SYSTEMD_USER_DIR="$HOME/.config/systemd/user"

echo "WinClip directory: $WINCLIP_DIR"
echo "Show command: $SHOW_COMMAND"

echo ""
echo "Installing WinClip dependencies..."

if command -v uv >/dev/null 2>&1; then
	(cd "$WINCLIP_DIR" && uv sync)
elif command -v pip3 >/dev/null 2>&1; then
	(cd "$WINCLIP_DIR" && pip3 install -e .)
else
	echo "Warning: neither 'uv' nor 'pip3' was found. Skipping Python dependency installation."
fi

if command -v apt-get >/dev/null 2>&1; then
	SYSTEM_PACKAGES=(xclip wl-clipboard ydotool xdotool)
	echo "Installing system packages: ${SYSTEM_PACKAGES[*]}"
	sudo apt-get update
	sudo apt-get install -y "${SYSTEM_PACKAGES[@]}"
else
	echo "Warning: unsupported package manager. Install these packages manually: xclip wl-clipboard ydotool xdotool"
fi

# Install the systemd user service for login startup
mkdir -p "$SYSTEMD_USER_DIR"
sed "s|%WINCLIP_DIR%|$WINCLIP_DIR|g" "$SERVICE_SOURCE" > "$SYSTEMD_USER_DIR/winclip.service"
systemctl --user daemon-reload
systemctl --user enable --now winclip.service
echo "Installed and started user service: winclip.service"

# Instructions for setting up keyboard shortcut
echo ""
echo "=== KEYBOARD SHORTCUT SETUP ==="
echo ""
echo "Choose a unique shortcut for WinClip (recommended: Ctrl+Alt+C):"
echo ""
echo "1. GNOME/KDE:"
echo "   - Go to Settings → Keyboard → Shortcuts"
echo "   - Add custom shortcut:"
echo "     Name: Show WinClip"
echo "     Command: $SHOW_COMMAND"
echo "     Shortcut: Ctrl+Alt+C (recommended)"
echo "     Alternative: Ctrl+Shift+C"
echo "     Alternative: Super+Shift+C"
echo ""
echo "2. i3/Sway:"
echo "   - Add to your config file:"
echo "     bindsym \$mod+Shift+c exec $SHOW_COMMAND"
echo "     # or: bindsym Control+Mod1+c exec $SHOW_COMMAND"
echo ""
echo "3. Other window managers:"
echo "   - Add to ~/.xbindkeysrc:"
echo "     \"$SHOW_COMMAND\""
echo "     Control+Mod1+c"
echo "     # or: Control+Shift+c"
echo ""
echo "=== USAGE ==="
echo ""
echo "Start WinClip in background:"
echo "  python3 $WINCLIP_DIR/main.py --daemon"
echo ""
echo "Start WinClip with GUI:"
echo "  python3 $WINCLIP_DIR/main.py --show"
echo ""
echo "Show WinClip (if running in background):"
echo "  $SHOW_COMMAND"
echo ""
echo "WinClip will now start automatically when you log in via the user service."
