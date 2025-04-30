function selectLight(color) {
    const lights = document.querySelectorAll('.light');
    lights.forEach(light => {
        light.classList.remove('selected');
        light.classList.remove('bouncing');
    });

    const selected = document.querySelector(`.${color}`);
    selected.classList.add('selected');
    selected.classList.add('bouncing');

    selected.addEventListener('animationend', () => {
        selected.classList.remove('bouncing');
    }, { once: true });
}
