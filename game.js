const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');
let balls = [];
let catcherX = canvas.width / 2;
const catcherWidth = 100;
let score = 0;
let misses = 0;  // Keep track of how many balls the player missed
let maxMisses = 3;
let gameOver = false;
let fallSpeed = 5;  // Initial fall speed
let gameInterval;
let demoMode = false;  // Flag to activate demo mode

const catchMessages = ["Look at you, finally making that button work!", "Awesome!", "You got it!", "Nice moves!", "Spot on!"];
const missMessages = ["Whoops!", "Missed!", "Are you playing or just sightseeing?", "Do you need glasses? Because that wasn’t even close!", "I’d call that a pass, but I don’t think the ball agrees."];
let messageTimeout;

// Start the game when the button is clicked
document.getElementById('startButton').addEventListener('click', function() {
    document.getElementById('startPage').style.display = 'none';
    document.getElementById('gamePage').style.display = 'block';

    // Check if we want demo mode for automatic gameplay
    const isDemo = confirm("Do you want to watch the demo mode?");
    demoMode = isDemo;  // Enable demo mode if the user agrees
    startGame();
});

// Restart the game when the restart button is clicked
document.getElementById('restartButton').addEventListener('click', function() {
    document.getElementById('restartButton').style.display = 'none';
    document.getElementById('gameOver').style.display = 'none';
    startGame();
});

function drawCatcher() {
    ctx.fillStyle = 'green';
    ctx.fillRect(catcherX, canvas.height - 50, catcherWidth, 10);
}

function createBall() {
    return {
        x: Math.random() * canvas.width,
        y: 0,
        size: 30
    };
}

function drawBalls() {
    for (let i = 0; i < balls.length; i++) {
        const ball = balls[i];
        ball.y += fallSpeed;
        ctx.beginPath();
        ctx.arc(ball.x, ball.y, ball.size / 2, 0, Math.PI * 2);
        ctx.fillStyle = 'black';
        ctx.fill();

        if (ball.y > canvas.height - 50) {
            if (ball.x > catcherX && ball.x < catcherX + catcherWidth) {
                score += 10;
                showMessage(catchMessages[Math.floor(Math.random() * catchMessages.length)], 'green');
                balls.splice(i, 1);
                document.getElementById('score').textContent = 'Score: ' + score;

                // Increase fall speed every 50 points
                if (score % 50 === 0) {
                    fallSpeed += 1;  // Increase difficulty by increasing the ball fall speed
                }
            } else {
                misses++;
                showMessage(missMessages[Math.floor(Math.random() * missMessages.length)], 'red');
                balls.splice(i, 1);
                document.getElementById('misses').textContent = `Misses: ${misses} / ${maxMisses}`;

                if (misses >= maxMisses) {
                    gameOver = true;
                    endGame();
                    clearInterval(gameInterval);
                }
            }
        }
    }
}

// Automated catcher movement in demo mode
function automatedMove() {
    if (balls.length > 0) {
        const closestBall = balls[0];  // Get the first ball in the list
        if (closestBall.x < catcherX && catcherX > 0) {
            catcherX -= 10;  // Move left towards the ball
        } else if (closestBall.x > catcherX + catcherWidth && catcherX < canvas.width - catcherWidth) {
            catcherX += 10;  // Move right towards the ball
        }
    }
}

// Update the game to call automatedMove if in demo mode
function updateGame() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    drawCatcher();
    if (Math.random() < 0.03) {
        balls.push(createBall());
    }
    drawBalls();
    
    if (demoMode) {
        automatedMove();  // Automate catcher movement
    }
}

document.addEventListener('keydown', function(event) {
    if (!gameOver && !demoMode) {  // Only move manually if not in demo mode
        if (event.key === 'ArrowLeft' && catcherX > 0) {
            catcherX -= 20;
        }
        if (event.key === 'ArrowRight' && catcherX < canvas.width - catcherWidth) {
            catcherX += 20;
        }
    }
});

function startGame() {
    // Reset game variables
    balls = [];
    score = 0;
    misses = 0;  // Reset the miss count
    fallSpeed = 5;  // Reset the speed
    gameOver = false;
    document.getElementById('gameOver').style.display = 'none';
    document.getElementById('score').textContent = 'Score: 0';
    document.getElementById('misses').textContent = `Misses: 0 / ${maxMisses}`;
    document.getElementById('restartButton').style.display = 'none';
    
    // Clear any previous game loop
    clearInterval(gameInterval);
    
    // Start the game loop
    gameInterval = setInterval(updateGame, 30);
}

function endGame() {
    document.getElementById('gameOver').style.display = 'inline';
    document.getElementById('restartButton').style.display = 'inline';
}

function showMessage(message, color) {
    clearTimeout(messageTimeout);
    const messageDiv = document.getElementById('message');
    messageDiv.textContent = message;
    messageDiv.style.color = color;
    messageTimeout = setTimeout(() => {
        messageDiv.textContent = '';
    }, 3000);  // Display the message for 3 seconds
}
