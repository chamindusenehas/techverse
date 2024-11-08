let round1 = document.getElementById('round1');
let round2 = document.getElementById('round2');

function checkLockStatus() {
    fetch('/touching', { method: 'GET' })
        .then(response => response.json())
        .then(data => {
            if (data.round1_locked) {
                round1.classList.add('locked');
            }
            if (data.round2_locked) {
                round2.classList.add('locked');
            }
        });
}

// Check lock status on page load
window.onload = checkLockStatus;

// Add click event listeners to the rounds
round1.addEventListener('click', () => {
    fetch('/touching', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ "round": 1 })
    }).then(checkLockStatus);
});

round2.addEventListener('click', () => {
    fetch('/touching', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ "round": 2 })
    }).then(checkLockStatus);
});
