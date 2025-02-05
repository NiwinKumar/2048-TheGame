function updateBoard(board) {
    // Clear the current board
    const gameBoard = document.getElementById("game-board");
    gameBoard.innerHTML = '';

    // Create and append new cells
    for (let i = 0; i < 4; i++) {
        for (let j = 0; j < 4; j++) {
            const cell = document.createElement('div');
            cell.classList.add('cell');
            const number = board[i][j];
            if (number !== 0) {
                cell.textContent = number;
                cell.style.backgroundColor = getCellColor(number);
                cell.style.color = getTextColor(number);
            }
            gameBoard.appendChild(cell);
        }
    }
}

//Function to update the score and high score in the HTML
function updateScore(score, high_score) {
    document.getElementById("score").textContent = score;
    document.getElementById("high-score").textContent = high_score;
}

function showGameOver() {
    document.getElementById("game-over").style.display = "flex";
}



function sendMove(direction) {
    fetch("/move", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ direction: direction }),
    })
        .then((response) => response.json())
        .then((data) => {
            updateBoard(data.board);
            //Update the score and high score in the HTML
            updateScore(data.score, data.high_score);
            if (data.game_over) {
                showGameOver();
            }
        })
        .catch((error) => {
            console.error("Error:", error);
        });
}

function getCellColor(number) {
    const colors = {
        2: "#eee4da",
        4: "#ede0c8",
        8: "#f2b179",
        16: "#f59563",
        32: "#f67c5f",
        64: "#f65e3b",
        128: "#edcf72",
        256: "#edcc61",
        512: "#edc850",
        1024: "#edc53f",
        2048: "#edc22e",
    };
    return colors[number] || '#3c3a32';
}

function getTextColor(number) {
    return number >= 8 ? '#f9f6f2' : '#776e65';
}

//Function to handle key presses
document.addEventListener("keydown", (event) => {
    switch (event.key) {
        case "ArrowUp":
            sendMove("up");
            break;
        case "ArrowDown":
            sendMove("down");
            break;
        case "ArrowLeft":
            sendMove("left");
            break;
        case "ArrowRight":
            sendMove("right");
            break;
    }
});

//Function to handle the new game button
document.getElementById("new-game-button").addEventListener("click", () => {
    //Hide game over message
    document.getElementById("game-over").style.display = "none";
    fetch("/reset", {
        method: "POST",
    })
        .then((response) => response.json())
        //Update the UI
        .then((data) => {
            updateBoard(data.board);
            updateScore(data.score, data.high_score);
        })
        .catch((error) => {
            console.error("Error:", error);
        });
});
//Function to load the initial board
// Initial board update
fetch("/reset", {
    method: "POST",
})
    .then((response) => response.json())
    .then((data) => {
        updateBoard(data.board);
        updateScore(data.score, data.high_score);
    })
    .catch((error) => {
        console.error("Error:", error);
    });
tool_outputs