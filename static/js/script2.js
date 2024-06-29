document.addEventListener('DOMContentLoaded', () => {
    const binaryContainer = document.querySelector('.binary-container');
    const colors = ['#0F0', '#FF0', '#F00', '#00F'];

    for (let i = 0; i < 300; i++) {
        const binary = document.createElement('div');
        binary.classList.add('binary');
        binary.style.left = `${Math.random() * 100}vw`;
        binary.style.animationDuration = `${Math.random() * 5 + 3}s`;
        binary.innerText = Math.random() > 0.5 ? '1' : '0';
        binaryContainer.appendChild(binary);
    }
});