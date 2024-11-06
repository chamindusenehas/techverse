function cham() {
    fetch('/join_quizzee')
        .then(response => response.json())
        .then(data => {
            if (data.start_quiz) {
                window.location.href = '/quiz';
            }
        })
        .catch(error => {
            console.error('Error joining quiz:', error);
            document.getElementById('status-message').innerText = 'Error joining the quiz. Please try again.';
        });
}

setInterval(cham, 500);