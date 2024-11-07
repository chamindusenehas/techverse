const timeLimitInSeconds = 30;
let countdownDisplay = document.getElementById("countdown");
let countdownInterval;
let timeLeft = timeLimitInSeconds;
let solution = 0;

let mainTimerInterval;
let remainingTime = timeLimitInSeconds;
let answered = false;
let buzzerTimerInterval;


function updateTimerDisplay(remainingTime) {
    const minutes = Math.floor(remainingTime / 60);
    const seconds = remainingTime % 60;
    document.getElementById('timer').innerText = `Time Remaining: ${minutes}:${seconds < 10 ? '0' : ''}${seconds}`;
}


function startTimer() {
    document.getElementById('timer').classList.remove('hidden');
    document.getElementById('countdown').classList.add('hidden');
    document.getElementById('answers').classList.add('hidden');
    fetch('/answer')
        .then(response => response.json())
        .then(data => {
            if (data.locked == false) {
                unlockVotingForAll();
            }
        });
    updateTimerDisplay(remainingTime);
    mainTimerInterval = setInterval(() => {
        remainingTime--;
        updateTimerDisplay(remainingTime);

        if (remainingTime <= 0) {
            clearInterval(mainTimerInterval);
            document.getElementById('newButton').click();
        }
    }, 1000);
}


function pauseTimer() {
    clearInterval(mainTimerInterval);
}

function resumeTimer() {
    startTimer();
}


function startBuzzerTimer() {
    let buzzerTimeLeft = 10;
    document.getElementById('timer').classList.add('hidden');
    document.getElementById('countdown').classList.remove('hidden');
    
    updateBuzzerTimerDisplay(buzzerTimeLeft);

    buzzerTimerInterval = setInterval(() => {
        buzzerTimeLeft--;
        updateBuzzerTimerDisplay(buzzerTimeLeft);

        if (buzzerTimeLeft <= 0) {
            
            if (answered == true){
                document.getElementById('newButton').click()
            }else{
                clearInterval(buzzerTimerInterval);
                resumeTimer();
                unlockVotingForAll();
            };
        }
    }, 1000);
}

function updateBuzzerTimerDisplay(timeLeft) {
    const minutes = Math.floor(timeLeft / 60);
    const seconds = timeLeft % 60;
    document.getElementById('countdown').innerText = `Time Remaining: ${minutes}:${seconds < 10 ? '0' : ''}${seconds}`;
    console.log("Remaining Buzzer Time:", timeLeft);
}


function lockVotingForAll() {
    document.getElementById('answers').classList.add('touchability');
    document.getElementById('buzzButton').classList.add('touchability');
}



function unlockVotingForAll() {
    document.getElementById('answers').classList.remove('touchability');
    document.getElementById('buzzButton').classList.remove('touchability');

}
let damnit = false;
let lockedin = 'unlocked';

document.getElementById('buzzButton').addEventListener('click', () => {
    damnit = true;
    document.getElementById('buzzButton').classList.add('touchability');
    document.getElementById('answers').classList.remove('hidden');
    fetch('/buzz', { method: 'POST' })
        .then(response => response.json())
        .then(data => {
            console.log(data.status);
        });
        fetch('/check_update', { method: 'GET' })
        .then(response => response.json())
        .then(data => {
            lockedin = data.status;
        });
});




function timer(){
    setInterval(() => {
        fetch('/check_lock')
            .then(response => response.json())
            .then(data => {
                lockedin = data.locked;
    
                if (data.locked == false) {
                    unlockVotingForAll();
                    resumeTimer();
                }else{
                    pauseTimer();
                    startBuzzerTimer();
                    if (damnit != true){
                        lockVotingForAll(); 
                    }
                }
            });
    }, 1000);
    
};







let answers = document.getElementsByTagName('span');
for (let i = 0; i < answers.length; i++) {
    
    answers[i].addEventListener('click', () => {
        setTimeout(() => {
            document.getElementById('answers').classList.add('touchability');
            answered = true;
        }, 50);
    });
    


}


document.getElementById('newButton').addEventListener('click', () => {
    fetch('/answer', { method: 'POST' })
        .then(response => response.json())
        .then(data => {
            console.log(data)
        });
});













window.onload = startTimer;





