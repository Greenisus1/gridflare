# Gridflare

Original fullscreen block-placement puzzle for Pi/Linux terminals. Place polyomino pieces on an 8x8 board; fill a whole row or column to flare it clear. Inspired by the place-and-clear idea of Block Blast with new code, name and art. Not an official port, no copied assets, sounds or branding.

Built with AI assistance from my design. Free, offline, no desktop, accounts, API keys, ads, paid unlocks or pip packages.

## Play

You always hold three pieces. 1-3 picks one, Arrows/WASD move its ghost over the board, Space/Enter places it. Placing all three draws three more. Every placed cell scores; each cleared line scores 100 with a growing bonus for multiple lines at once. The run ends when none of your pieces fits anywhere. R restarts, Q/Esc quits. Letter controls accept either casing.

## Display and setup

ANSI truecolor and Unicode half-block pixel art when the terminal advertises support (COLORTERM=truecolor/24bit or direct-color TERM). V toggles pixel/text manually; `python3 gridflare.py --ascii` starts in text mode. Minimum 64x24; smaller windows pause with the size they need.

Pi App Store -> Games -> Gridflare. Installer checks Python/curses and adds Python with apt/apk/pacman if needed. Package installation needs root; Arch retains its package manager's normal confirmation.

    bash app-store.sh INSTALL
    bash app-store.sh RUN
    python3 -m unittest -v
    python3 test_terminal.py

Best score saved locally at `~/.local/share/gridflare/best.json` only on game over, not on restart/quit. Saves are private, atomic and reject symlinks. No online leaderboard or synchronized sessions.

## Scope and verification

A compact original puzzle: one endless board, no levels, timers, ads or power-ups. Local unit and PTY tests cover placement rules, bounds, occupancy, row/column/multi-line clears, scoring, offer refills, game-over detection, shape validity, saves, resizing and clean terminal exit. Before publication, all 13 unit tests and pixel/text PTY control/resize/exit checks passed on a real aarch64 Raspberry Pi.

MIT license, copyright 2026 Greenisus1.
