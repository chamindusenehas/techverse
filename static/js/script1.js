const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');

canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

const dots = [];
const numDots = 50;

for (let i = 0; i < numDots; i++) {
    dots.push({
        x: Math.random() * canvas.width,
        y: Math.random() * canvas.height,
        vx: Math.random() *2 -1,
        vy: Math.random() *2 -1,
        radius: 2,
        color: '#FAEF5D'
    });
}

function draw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    dots.forEach((dot, index) => {
        ctx.beginPath();
        ctx.fillStyle = dot.color;
        ctx.arc(dot.x, dot.y, dot.radius,0,360);
        ctx.fill();

        for (let i = index + 1; i < dots.length; i++) {
            const otherDot = dots[i];
            const distance = Math.sqrt((dot.x - otherDot.x) ** 2 + (dot.y - otherDot.y) ** 2);
            if (distance < 150) {
                ctx.beginPath();
                ctx.strokeStyle = 'red';
                ctx.moveTo(dot.x, dot.y);
                ctx.lineTo(otherDot.x, otherDot.y);
                ctx.stroke();
            }
        }
    });
}

function update() {
    dots.forEach(dot => {
        dot.x += dot.vx;
        dot.y += dot.vy;

        if (dot.x < 0 || dot.x > canvas.width) {
            dot.vx *= -1;
        }
        if (dot.y < 0 || dot.y > canvas.height) {
            dot.vy *= -1;
        }
    });
}

function animate() {
    requestAnimationFrame(animate);
    draw();
    update();
}

animate();

