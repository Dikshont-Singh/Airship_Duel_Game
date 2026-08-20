# 🚀 Airship Duel

> A fast-paced 2-player space combat game built with Python and Pygame.

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python)
![Pygame](https://img.shields.io/badge/Pygame-2.x-green)
![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey)
![Status](https://img.shields.io/badge/Status-In%20Development-orange)

---

## 🎮 About the Game

**Airship Duel** is a 2-player space combat game developed using **Python and Pygame**.

Choose your ship, master its unique ability, and defeat your opponent in a fast-paced battle.

Every ship has a different playstyle, so choosing the right ship can completely change the way you fight.

---

## ✨ Features

- 🚀 2-player local multiplayer
- 🛸 Multiple unique playable ships
- ⚡ Unique ability for every ship
- 💥 Projectile-based combat
- ❤️ Health system
- 🔋 Ability cooldown/recharge system
- 🛡️ Defensive and offensive abilities
- 🎮 Custom main menu
- 🖼️ Ship selection system
- 🔊 Sound effects and game audio
- 🌀 Screen wrapping movement
- 💻 Windows `.exe` support

---

# 🛸 Ships & Abilities

Each ship has its own special ability.

| Ship | Ability | Playstyle |
|---|---|---|
| 🦅 Falcon | Shield | Defensive |
| ⚔️ Blade | Dash | Aggressive / Close-range |
| 🔵 Nova | Twin Shot | Multi-shot |
| 🟡 Raven | Homing Missile | Tracking |
| 🟣 Vortex | Shadow Teleport | Positioning |
| 👻 Specter | Shotgun Burst | Close-range burst |
| 🟣 Phantom | Invisible Cloak | Stealth |
| 🟤 Titan | Siege Mode | Heavy combat |

### ⚔️ Blade — Dash

Blade rapidly dashes forward for a short period.

During the dash:

- Blade is protected by a temporary shield.
- Hitting the opponent deals damage.
- The opponent is knocked backward.

### 🔫 Nova — Twin Shot

Nova temporarily fires two bullets simultaneously instead of one.

### 💣 Raven — Homing Missile

Raven launches a missile that follows the opponent.

### 🕳️ Vortex — Shadow Teleport

Vortex teleports behind the opponent, allowing it to quickly change its position.

### 👻 Specter — Shotgun Burst

Specter fires a spread of bullets in a curved/fan-shaped pattern.

### 🟣 Phantom — Invisible Cloak

Phantom temporarily becomes difficult to see and can avoid incoming attacks while cloaked.

### 🟤 Titan — Siege Mode

Titan enters a heavy combat state focused on increased firepower and durability.

---

# 🎮 Controls

## Player 1

| Key | Action |
|---|---|
| W | Move forward |
| S | Move backward |
| A | Rotate left |
| D | Rotate right |
| Space | Shoot |
| Left Shift | Ability |

## Player 2

| Key | Action |
|---|---|
| ↑ | Move forward |
| ↓ | Move backward |
| ← | Rotate left |
| → | Rotate right |
| Enter | Shoot |
| Right Shift | Ability |

> Controls may change as development continues.

---

# 🖥️ Main Menu

The game includes a custom main menu where players can:

- Select their ship
- View the selected ship
- View the ship's ability
- Read the ability description
- Start the game
- View controls
- Quit the game

---

# 🛠️ Built With

- **Python**
- **Pygame**
- **PyInstaller** — Windows executable packaging

---

# 📁 Project Structure

```text
Airship-Duel/
│
├── Airship_game.py
├── README.md
├── requirements.txt
├── game_logo.png
│
├── assets/
│   ├── ships/
│   ├── backgrounds/
│   ├── effects/
│   └── fonts/
│
├── sounds/
│   ├── shooting/
│   ├── explosions/
│   └── abilities/
│
└── dist/
    └── Airship_Duel.exe
