const API_URL = "/api";
let isAutoSolving = false;
let currentGameId = null

window.onload = startNewGame;

const DIFFICULTIES = {
    easy: { size: 8, mines: 7 },
    medium: { size: 10, mines: 15 },
    hard: { size: 16, mines: 40 }
};

let timerInterval = null;
let secondsElapsed = 0;
let timerStarted = false;

function startTimer() {
    if (timerStarted) return;
    timerStarted = true;

    timerInterval = setInterval(() => {
        secondsElapsed++;
        document.getElementById('timer').innerText = String(secondsElapsed).padStart(3, "0");
    }, 1000);
}

function stopTimer() {
    clearInterval(timerInterval);
    timerInterval = null;
}

function resetTimer() {
    stopTimer();
    timerStarted = false;
    secondsElapsed = 0;
    document.getElementById('timer').innerText = "000";
}

document.getElementById('difficulty').addEventListener('change', (e) => {
    const customInputs = document.getElementById('custom-inputs');
    if (e.target.value === 'custom') {
        customInputs.style.display = 'block';
    } else {
        customInputs.style.display = 'none';
        startNewGame();
    }
});

async function startNewGame() {
    resetTimer()
    isAutoSolving = false;
    document.getElementById('auto-btn').innerText = "Auto Solve";

    const{size, mines} = getSizeAndMines()

    try {
        const response = await fetch(`${API_URL}/new-game`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ size: size, mines: mines})
        });
        const data = await response.json();
        currentGameId = data.game_id
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
    let flagged = 0
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
                flagged++;
            }

            cellDiv.onclick = () => handleCellClick(r, c);
            cellDiv.oncontextmenu = (e) => {
                e.preventDefault();
                handleCellFlag(r, c);
            };

            boardDiv.appendChild(cellDiv);
        });
    });

    const {size, mines} = getSizeAndMines()
    document.getElementById("mines-count").innerText = String(mines - flagged)
    if (data.win) {
        stopTimer()
        statusDiv.innerText = "🎉 You Won!";
    } else if (data.game_over) {
        stopTimer()
        statusDiv.innerText = "💥 Game Over!";
    } else {
        statusDiv.innerText = "";
    }
}

async function handleCellClick(r, c) {
    if (!timerStarted) {
        startTimer();
    }
    try {
        const response = await fetch(`${API_URL}/click`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ game_id: currentGameId, row: r, col: c })
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
            body: JSON.stringify({ game_id: currentGameId, row: r, col: c })
        });
        const data = await response.json();
        renderBoard(data);
    } catch (err) {
        console.error("Failed to flag cell:", err);
    }
}

async function stepSolve() {
    try{
        const res = await fetch(`${API_URL}/solve-step`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({game_id: currentGameId})
        });
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

function getSizeAndMines() {
    const selectedDiff = document.getElementById('difficulty').value;
    let size, mines;

    if (selectedDiff === 'custom') {
        size = parseInt(document.getElementById('custom-size').value, 10) || 10;
        mines = parseInt(document.getElementById('custom-mines').value, 10) || 15;

        const maxMines = (size * size) - 1;
        if (mines > maxMines) {
            mines = maxMines;
            document.getElementById('custom-mines').value = mines;
        }
    } else {
        const config = DIFFICULTIES[selectedDiff] || DIFFICULTIES.medium;
        size = config.size;
        mines = config.mines;
    }
    return {size, mines};
}
