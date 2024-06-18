window.addEventListener('load', function () {
    const canvas = document.getElementById('confetti-canvas');
    const ctx = canvas.getContext('2d');
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;

    const confettiArray = [];
    let confettiCount = 300;
    const colors = ['#fde132', '#009bde', '#ff6b00'];

    function Confetti() {
        this.x = Math.random() * canvas.width;
        this.y = Math.random() * canvas.height - canvas.height;
        this.color = colors[Math.floor(Math.random() * colors.length)];
        this.radius = Math.random() * 6 + 2;
        this.density = Math.random() * confettiCount + 10;
        this.speedX = Math.random() * 3 - 1.5;
        this.speedY = Math.random() * 2 + 1;
    }

    Confetti.prototype.draw = function () {
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2, false);
        ctx.fillStyle = this.color;
        ctx.fill();
    }

    Confetti.prototype.update = function () {
        this.y += this.speedY;
        this.x += this.speedX;

        if (this.y > canvas.height) {
            this.y = -10;
            this.x = Math.random() * canvas.width;
        }
    }

    function init() {
        for (let i = 0; i < confettiCount; i++) {
            confettiArray.push(new Confetti());
        }
    }

    function animate() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        confettiArray.forEach(confetti => {
            confetti.update();
            confetti.draw();
        });

        if (confettiCount > 0) {
            confettiCount -= 0.5;
        }
        if (Date.now() - startTime > 5000) {
            confettiCount = 0;
        }

        requestAnimationFrame(animate);
    }

    let startTime = Date.now();
    init();
    animate();
});