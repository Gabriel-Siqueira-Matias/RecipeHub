document.addEventListener('DOMContentLoaded', function () {
    const midia_container = document.getElementById('midia-container');
    if (midia_container) {
        const midia_elementos = midia_container.querySelectorAll('.midia_elemento');
        const anteriorBtn = document.getElementById('anterior');
        const proximoBtn = document.getElementById('proximo');
        let currentIndex = 0;

        function showElemento(index) {
            midia_elementos.forEach(elemento => elemento.classList.remove('active'));
            midia_elementos[index].classList.add('active');
        }

        function showAnterior() {
            currentIndex--;
            if (currentIndex < 0) {
                currentIndex = midia_elementos.length - 1;
            }
            showElemento(currentIndex);
        }

        function showProximo() {
            currentIndex++;
            if (currentIndex >= midia_elementos.length) {
                currentIndex = 0;
            }
            showElemento(currentIndex);
        }

        if (anteriorBtn && proximoBtn) {
            anteriorBtn.addEventListener('click', showAnterior);
            proximoBtn.addEventListener('click', showProximo);
        }
    }
});