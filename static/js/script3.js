const timeLimitInSeconds = 30;
let countdownDisplay = document.getElementById("countdown");
let countdownInterval;
let timeLeft = 10;
let solution = 0;

function updateTimerDisplay(remainingTime) {
    const minutes = Math.floor(remainingTime / 60);
    const seconds = remainingTime % 60;
    document.getElementById('timer').innerText = `Time Remaining: ${minutes}:${seconds < 10 ? '0' : ''}${seconds}`;
}

function updateTimerDisplay2(remainingTime) {
    const minutes = Math.floor(remainingTime / 60);
    const seconds = remainingTime % 60;
    document.getElementById('countdown').innerText = `Time Remaining: ${minutes}:${seconds < 10 ? '0' : ''}${seconds}`;
}

let timerInterval;
let remainingTime;
let getted = 0;

function startTimer() {
    document.getElementById('timer').classList.remove('hidden');
    document.getElementById('countdown').classList.add('hidden');
    document.getElementById('answers').classList.add('hidden');
    remainingTime = timeLimitInSeconds;
    updateTimerDisplay(remainingTime);

    timerInterval = setInterval(() => {
        remainingTime -= 1;
        updateTimerDisplay(remainingTime);

        if (remainingTime <= 0) {
            clearInterval(timerInterval);
            document.getElementById('newButton').click();
        }
    }, 1000);
}

document.getElementById('buzzButton').addEventListener('click', () => {
    setTimeout(() => {
        document.getElementById('buzzButton').classList.add('touchability');
    }, 50);
    document.getElementById('answers').classList.remove('hidden');
    clearInterval(timerInterval);
    document.getElementById('timer').classList.add('hidden');
    document.getElementById('countdown').classList.remove('hidden');

    let remainingTime2 = 10;
    updateTimerDisplay2(remainingTime2);

    countdownInterval = setInterval(() => {
        remainingTime2--;
        updateTimerDisplay2(remainingTime2);

        if (remainingTime2 <= 0) {
            clearInterval(countdownInterval);
            document.getElementById('answers').classList.add('touchability');
            document.getElementById('newButton').click();
        }
    }, 1000);
});

let answers = document.getElementById('answers');
answers.addEventListener('click', () => {
    setTimeout(() => {
        document.getElementById('answers').classList.add('touchability');
    }, 50);
});

for (let ix = 1; ix < 5; ix++) {
    document.getElementById(`option_${ix}`).addEventListener('click', () => {
        document.getElementById('selected').innerHTML = document.getElementById(`opinion_${ix}`).textContent;
    });
}

if (document.getElementById('selected').textContent === document.getElementById('banswer').textContent) {
    console.log(document.getElementById('timed'));
    console.log(remainingTime);
    document.getElementById('timed').value = remainingTime;
}

window.onload = startTimer;





