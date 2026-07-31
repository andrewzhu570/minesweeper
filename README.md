# 💣 Minesweeper with Custom Automated Solver


<img width="560" height="634" alt="Screenshot 2026-07-30 at 10 47 45 PM" src="https://github.com/user-attachments/assets/d58cd374-dab7-4643-adcd-9bd2d009ace1" />




A full-stack Minesweeper web application built from scratch with Python (Flask) and JavaScript, featuring dynamic board chording, multiple difficulty levels, and an automated solver engine that uses set-based inference logic.

Live Demo: https://minesweeper-buof.onrender.com
---

## Features

### Gameplay
* **Responsive Web Interface:** Clean layout built with HTML, CSS, and JS for smooth play on desktop and mobile browsers.
* **First-Click Safety:** Relocates mines on your first click so you never hit a bomb on move one.
* **Board Chording:** Middle/right click a number cell touching enough flags to quickly clear unflagged neighbor cells.
* **Presets & Controls:** Features Easy ($8 \times 8$), Intermediate ($10 \times 10$), and Advanced ($16 \times 16$) modes with a live timer and flag counter. An option to customize the size and mines is also included.
* **Multi Device Support:** Tracks active game sessions using unique game_id UUIDs, preventing state collision across multiple browser tabs or concurrent users.


### Custom Solver Logic
* **Step-by-Step & Auto-Play Modes:** Use `Solve Step` to reveal one logical move at a time or `Solve All` to let the program complete the board.
* **Deterministic Deduction:** Automatically places flags on guaranteed mines and reveals safe cells using neighborhood analysis.
* **Set-Difference Inference:** Uses subset logic (`find_subset_moves`) to resolve complex, overlapping boundary scenarios.

---


## Tech Stack

* **Backend:** Python 3, Flask, Flask-CORS
* **Frontend:** JavaScript, HTML, CSS
* **Deployment:** Render





