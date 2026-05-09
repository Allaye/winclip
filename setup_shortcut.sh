#!/bin/bash
set -e

echo "Setting up WinClip..."
echo ""
echo -n "Where would you like to install WinClip? [Default: $HOME/.local/share/winclip]: "
read -r user_dir < /dev/tty || true
INSTALL_DIR=${user_dir:-"$HOME/.local/share/winclip"}
INSTALL_DIR="${INSTALL_DIR/#\~/$HOME}"

if [ ! -d "$INSTALL_DIR/.git" ]; then
    echo "Downloading WinClip to $INSTALL_DIR..."
    rm -rf "$INSTALL_DIR"
    mkdir -p "$INSTALL_DIR"
    git clone https://github.com/Allaye/winclip.git "$INSTALL_DIR"
else
    echo "WinClip already found in $INSTALL_DIR, pulling latest changes..."
    (cd "$INSTALL_DIR" && git fetch origin && git reset --hard origin/master)
fi

WINCLIP_DIR="$INSTALL_DIR"
SHOW_COMMAND="python3 $WINCLIP_DIR/main.py --show"
SERVICE_SOURCE="$WINCLIP_DIR/winclip.service"
SYSTEMD_USER_DIR="$HOME/.config/systemd/user"

echo ""
echo "Installing WinClip dependencies..."

if command -v uv >/dev/null 2>&1; then
    (cd "$WINCLIP_DIR" && uv sync)
elif command -v pip3 >/dev/null 2>&1; then
    (cd "$WINCLIP_DIR" && pip3 install -e .)
fi

if command -v apt-get >/dev/null 2>&1; then
    SYSTEM_PACKAGES=(xclip wl-clipboard ydotool xdotool libgtk-4-dev gir1.2-gtk-4.0 libgirepository1.0-dev libcairo2-dev pkg-config python3-dev python3-gi)
    sudo apt-get update && sudo apt-get install -y "${SYSTEM_PACKAGES[@]}"
elif command -v dnf >/dev/null 2>&1; then
    DNF_PACKAGES=(xclip wl-clipboard ydotool xdotool gtk4-devel gobject-introspection-devel cairo-devel python3-devel python3-gobject)
    sudo dnf install -y "${DNF_PACKAGES[@]}"
elif command -v pacman >/dev/null 2>&1; then
    PACMAN_PACKAGES=(xclip wl-clipboard ydotool xdotool gtk4 gobject-introspection python-gobject cairo)
    sudo pacman -S --needed --noconfirm "${PACMAN_PACKAGES[@]}"
fi

mkdir -p "$SYSTEMD_USER_DIR"
sed "s|%WINCLIP_DIR%|$WINCLIP_DIR|g" "$SERVICE_SOURCE" > "$SYSTEMD_USER_DIR/winclip.service"
systemctl --user daemon-reload
systemctl --user enable winclip.service
systemctl --user restart winclip.service

echo ""
echo "=== KEYBOARD SHORTCUT SETUP ==="
echo "Create a custom shortcut in your system settings:"
echo "Command: $SHOW_COMMAND"
echo "Shortcut: Ctrl+Alt+C"
