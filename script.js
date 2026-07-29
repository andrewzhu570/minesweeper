const API_URL = "http://127.0.0.1:5000/api";
let isAutoSolving = false;

window.onload = startNewGame;

async function startNewGame() {
    isAutoSolving = false;
    document.getElementById('auto-btn').innerText = "Auto Solve";

    try {
        const response = await fetch(`${API_URL}/new-game`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ size: 8, mines: 7 })
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

    boardDiv.style.gridTemplateColumns = `repeat(${data.grid.length}, 40px)`;
    boardDiv.innerHTML = '';

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


