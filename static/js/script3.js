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
let answered = false;

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


function lock_all(){
    document.getElementById('answers').classList.remove('hidden');
    document.getElementById('buzzButton').classList.add('touchability');
    clearInterval(timerInterval);
    document.getElementById('timer').classList.add('hidden');
    document.getElementById('countdown').classList.remove('hidden');

    let remainingTime2 = 10;
    updateTimerDisplay2(remainingTime2);

    countdownInterval = setInterval(() => {
        remainingTime2--;
        updateTimerDisplay2(remainingTime2);

        if (remainingTime2 <= 0) {


            fetch('/answer', { method: 'POST' })
                .then(response => response.json())
                .then(data => {
                    console.log(data)
                });



            clearInterval(countdownInterval);


            
            if (remainingTime > 0 && answered == false){
                let more = remainingTime;
                timerInterval = setInterval(() => {
                    updateTimerDisplay(remainingTime);
            
                    if (remainingTime <= 0 || answered == true) {
                        clearInterval(remainingTime);
                        answered = false;
                        document.getElementById('newButton').click();
                    }
                }, 1000);





            }else{
                document.getElementById('newButton').click();
            };
            
        };
    }, 1000); 

};




document.getElementById('buzzButton').addEventListener('click', () => {
    document.getElementById('answers').classList.remove('hidden');
    document.getElementById('buzzButton').classList.add('touchability');
    clearInterval(timerInterval);
    document.getElementById('timer').classList.add('hidden');
    document.getElementById('countdown').classList.remove('hidden');

    let remainingTime2 = 10;
    updateTimerDisplay2(remainingTime2);

    countdownInterval = setInterval(() => {
        remainingTime2--;
        updateTimerDisplay2(remainingTime2);

        if (remainingTime2 <= 0) {


            fetch('/answer', { method: 'POST' })
                .then(response => response.json())
                .then(data => {
                    console.log(data)
                });



            clearInterval(countdownInterval);


            
            if (remainingTime > 0 && answered == false){
                let more = remainingTime;
                timerInterval = setInterval(() => {
                    updateTimerDisplay(remainingTime);
            
                    if (remainingTime <= 0 || answered == true) {
                        clearInterval(remainingTime);
                        answered = false;
                        document.getElementById('newButton').click();
                    }
                }, 1000);





            }else{
                document.getElementById('newButton').click();
            };
            
        };
    }, 1000);
});

let answers = document.getElementsByTagName('span');
for (let i = 0; i < answers.length; i++) {
    
    answers[i].addEventListener('click', () => {
        setTimeout(() => {
            document.getElementById('answers').classList.add('touchability');
            answered = true;
        }, 50);
    });
    


}

document.getElementById('buzzButton').addEventListener('click', () => {
    fetch('/buzz', { method: 'POST' })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'locked') {
                startBuzzerTimer();
            }
        });
});


document.getElementById('newButton').addEventListener('click', () => {
    fetch('/answer', { method: 'POST' })
        .then(response => response.json())
        .then(data => {
            console.log(data)
        });
});










function startBuzzerTimer() {
    let buzzerTimeLeft = 10;
    buzzerTimer = setInterval(() => {
        buzzerTimeLeft--;
        updateBuzzerTimerDisplay(buzzerTimeLeft);

        if (buzzerTimeLeft <= 0) {
            clearInterval(buzzerTimer);
            resetMainTimer(); // If the buzzer time ends, reset the main timer for all players
        }
    }, 1000);
}


function updateBuzzerTimerDisplay(timeLeft) {
    // Update buzzer timer display logic here
    console.log("Remaining Buzzer Time:", timeLeft);
}


function resetMainTimer() {
    fetch('/reset_timer', { method: 'POST' })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'reset') {
                startTimer(); // Restart the main timer for all players
                unlockQuizForAll();
            }
        });
}


function unlockQuizForAll() {
    fetch('/check_lock')
        .then(response => response.json())
        .then(data => {
            if (data.locked) {
                // Unlock the quiz for all players
                document.querySelectorAll('input[type=radio]').forEach(input => {
                    input.disabled = false;
                });
                buzzButton.disabled = false;
            }
        });
};






// function checkLockStatus() {
//     fetch('/check_update')
//         .then(response => response.json())
//         .then(data => {
//             if (data.status === true) {
//                 console.log("Lock status: locked");
//                 startTimer();

//             } else {
//                 console.log("Lock status: unlocked");
//                 lock_all();
//             }
//         })
//         .catch(error => console.error('Error:', error));
// }

// // Call the checkLockStatus function every 1 second (1000 milliseconds)
// setInterval(checkLockStatus, 1000);








window.onload = startTimer;





