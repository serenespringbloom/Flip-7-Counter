# 🎴 Flip 7 Game Assistant

A simple Python Tkinter-based GUI tool to assist players in keeping track of scores, turn order, and special card effects while playing the physical card game **Flip 7**.

---

## 🕹️ Game Overview

**Flip 7** is a multiplayer card game where players try to accumulate 200 points by drawing cards ranging from 0–12. Each round, players take turns to draw or stay. Drawing duplicates in a round causes a bust, unless protected by a **Second Chance** card. Bonus point cards and special ability cards can influence the round.

This app manages:
- Player setup and turn order
- Score tracking (total and round points)
- Bust and stay logic
- Special card effects (Freeze, Flip Three, Second Chance, bonus points)
- Round transitions

---

## 🧩 Features

- ✅ Add 2 or more players by name  
- ✅ Track total and round points  
- ✅ Status indicators: Active, Stayed, Busted, Frozen  
- ✅ Detect busts and auto-stay on 7 cards  
- ✅ Play and apply special cards:  
  - **Freeze** (force another player to stay)  
  - **Flip Three** (force a player to draw 3 cards manually)  
  - **Second Chance** (prevents 1 bust)  
  - **+2**, **+4**, **+6**, **+10**, **x2** bonus cards  
- ✅ Automatically ends rounds when all players are done  
- ✅ Clears round data and special cards before new round  

---

## 🚀 Getting Started

### 🔧 Requirements
- Python 3.x
- Tkinter (usually comes with Python)

### ▶️ Run the App

```bash
python game.py
