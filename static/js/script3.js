
const timeLimitInSeconds = 30; 
    
    
function updateTimerDisplay(remainingTime) {
    const minutes = Math.floor(remainingTime / 60);
    const seconds = remainingTime % 60;
    document.getElementById('timer').innerText = `Time Remaining: ${minutes}:${seconds < 10 ? '0' : ''}${seconds}`;
}


function startTimer() {
    let remainingTime = timeLimitInSeconds;
    updateTimerDisplay(remainingTime);

    const timerInterval = setInterval(() => {
        remainingTime--;
        updateTimerDisplay(remainingTime);

        if (remainingTime <= 0) {
            clearInterval(timerInterval);
            document.getElementById('newButton').click();
        }
    }, 1000);
}


window.onload = startTimer;