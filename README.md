# 💣 Minesweeper with Custom Automated Solver

A full-featured desktop Minesweeper application built from scratch in Python, featuring dynamic board chording, multiple difficulty levels, and an automated solver engine that uses set-based inference logic.

---

## Features

### Gameplay
* **Interactive Tkinter GUI:** Clean layout with color-coded number displays, emojis, and visual status updates.
* **First-Click Safety:** Relocates mines on your first click so you never hit a bomb on move one.
* **Board Chording:** Middle/right click a number cell touching enough flags to quickly clear unflagged neighbor cells.
* **Presets & Controls:** Features Easy ($8 \times 8$), Intermediate ($14 \times 14$), and Advanced ($20 \times 20$) modes with a live timer and flag counter.

### Custom Solver Logic
* **Step-by-Step & Auto-Play Modes:** Use `Solve Step` to reveal one logical move at a time or `Solve All` to let the program complete the board.
* **Deterministic Deduction:** Automatically places flags on guaranteed mines and reveals safe cells using neighborhood analysis.
* **Set-Difference Inference:** Uses subset logic (`find_subset_moves`) to resolve complex, overlapping boundary scenarios.
* **Benchmarking Suite:** Includes `benchmark.py` to test solver performance across hundreds of automated games.

> **Note on OS Compatibility:** The user interface, button bindings (e.g., Mac trackpad right-clicks/two-finger taps), and typography are optimized for macOS. While the core game logic runs cross-platform, visual styling may render differently on Windows or Linux.
---

## How to Run

### Option 1: Standalone macOS App (No Python Required)
1. Download **`main.zip`** from the latest GitHub Release.
2. Unzip `main.zip` to extract **`main.app`**.
3. **First-time setup:** Right-click `main.app` $\rightarrow$ select **Open** $\rightarrow$ click **Open** on the macOS security prompt.

### Option 2: From Source Code
Ensure you have **Python 3** installed, then clone the repository and run `main.py`:

```bash
git clone [https://github.com/your-username/your-repo-name.git](https://github.com/your-username/your-repo-name.git)
cd your-repo-name
python3 main.py
```



<img width="711" height="443" alt="Screenshot 2026-07-20 at 6 37 29 PM" src="https://github.com/user-attachments/assets/6b994c9f-0c15-4bee-a17a-ff42f5d2ae79" />
