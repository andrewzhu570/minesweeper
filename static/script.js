const API_URL = "/api";
let isAutoSolving = false;

window.onload = startNewGame;

const DIFFICULTIES = {
    easy: { size: 8, mines: 7 },
    medium: { size: 10, mines: 15 },
    hard: { size: 16, mines: 40 }
};

document.getElementById('difficulty').addEventListener('change', startNewGame);

async function startNewGame() {
    isAutoSolving = false;
    document.getElementById('auto-btn').innerText = "Auto Solve";

    const selectedDiff = document.getElementById('difficulty').value;
    const config = DIFFICULTIES[selectedDiff] || DIFFICULTIES.medium;

    try {
        const response = await fetch(`${API_URL}/new-game`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ size: config.size, mines: config.mines})
        });
        const data = await response.json();
        renderBoard(data);
    } catch (err) {
        console.error("Failed to start new game:", err);
    }
}

function renderBoard(data) {
    const boardDiv = document.getElementById('board');
    const statusDiv = document.getElementById('status');

    const autoSolveBtn = document.getElementById('auto-btn');
    const solveStepBtn = document.getElementById('solve-btn')

    const isGameOver = data.game_over || data.win;


    const cols = data.grid[0] ? data.grid[0].length : data.grid.length;
    boardDiv.style.gridTemplateColumns = `repeat(${cols}, 40px)`;
    boardDiv.innerHTML = '';

    if (isGameOver) {
        boardDiv.style.pointerEvents = 'none';
        boardDiv.style.opacity = '0.85';
        if (autoSolveBtn) autoSolveBtn.disabled = true;
        if (solveStepBtn) solveStepBtn.disabled = true;
    } else {
        boardDiv.style.pointerEvents = 'auto';
        boardDiv.style.opacity = '1';
        if (autoSolveBtn) autoSolveBtn.disabled = false;
        if (solveStepBtn) solveStepBtn.disabled = false;
    }

    data.grid.forEach((row, r) => {
        row.forEach((cell, c) => {
            const cellDiv = document.createElement('div');
            cellDiv.classList.add('cell');

            if (cell.revealed) {
                cellDiv.classList.add('revealed');
                if (cell.has_mine) {
                    cellDiv.innerText = '💣';
                } else if (cell.neighbor_mines > 0) {
                    cellDiv.innerText = cell.neighbor_mines;
                }
            } else if (cell.flagged) {
                cellDiv.classList.add('flagged');
                cellDiv.innerText = '🚩';
            }

            cellDiv.onclick = () => handleCellClick(r, c);
            cellDiv.oncontextmenu = (e) => {
                e.preventDefault();
                handleCellFlag(r, c);
            };

            boardDiv.appendChild(cellDiv);
        });
    });

    if (data.win) {
        statusDiv.innerText = "🎉 You Won!";
    } else if (data.game_over) {
        statusDiv.innerText = "💥 Game Over!";
    } else {
        statusDiv.innerText = "";
    }
}

async function handleCellClick(r, c) {
    try {
        const response = await fetch(`${API_URL}/click`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ row: r, col: c })
        });
        const data = await response.json();
        renderBoard(data);
    } catch (err) {
        console.error("Failed to click cell:", err);
    }
}

async function handleCellFlag(r, c) {
    try {
        const response = await fetch(`${API_URL}/flag`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ row: r, col: c })
        });
        const data = await response.json();
        renderBoard(data);
    } catch (err) {
        console.error("Failed to flag cell:", err);
    }
}

async function stepSolve() {
    try{
        const res = await fetch(`${API_URL}/solve-step`, { method: 'POST'});
        const data = await res.json();
        renderBoard(data)

        if (data.status === 'stuck' && !data.game_over && !data.win) {
            document.getElementById('status').innerText = "Solver is stuck! Make a guess.";
        }
        return data;
    } catch (err) {
        console.log("Failed to run solve step", err);
    }
}

async function toggleAutoSolve() {
    isAutoSolving = !isAutoSolving;
    const btn = document.getElementById('auto-btn');
    btn.innerText = isAutoSolving ? "Pause" : "Auto Solve";

    while (isAutoSolving) {
        const data = await stepSolve();

        if (!data || data.game_over || data.win || data.status === 'stuck') {
            isAutoSolving = false;
            btn.innerText = "Auto Solve";
            break;
        }

        await new Promise(res => setTimeout(res, 250));
    }
}
