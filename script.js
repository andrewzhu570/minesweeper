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


