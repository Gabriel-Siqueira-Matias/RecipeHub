document.addEventListener('DOMContentLoaded', function() {

    // =========================================================================

    // 1. LÓGICA DO CARROSSEL DE MÍDIA (SWIPE, BOTÕES E PONTOS)

    // =========================================================================

    const carrossel = document.getElementById('carrossel_midia');

   

    if (carrossel) {
        const carrosselConteudo = carrossel.querySelector('.carrossel_conteudo');
        const midiaItens = carrossel.querySelectorAll('.midia_item');
        const prevBtn = carrossel.querySelector('.prev_btn');
        const nextBtn = carrossel.querySelector('.next_btn');
        const pontosContainer = carrossel.querySelector('.pontos_navegacao');

        // --- Variáveis de Estado do Carrossel ---
        let currentIndex = 0;
        const totalItems = midiaItens.length;
       
        // Variáveis de Estado para Drag/Swipe
        let isDragging = false;
        let startX = 0;
        let currentTranslate = 0;
        let prevTranslate = 0;
        const dragThreshold = 0.2; // 20% da largura do item para trocar de slide

        // Adiciona o data-index a cada item do carrossel (necessário para a lógica do vídeo)
        midiaItens.forEach((item, index) => {
            item.dataset.index = index;
        });
        
        // Encontra todos os elementos de vídeo
        const videoElementos = carrossel.querySelectorAll('video');

        // --- Funções Auxiliares do Carrossel ---
        function pauseInactiveMedia() {
            videoElementos.forEach((video) => {

                // Pausa o vídeo se não estiver no slide ativo
                const parentIndex = parseInt(video.closest('.midia_item').dataset.index);
                if (parentIndex !== currentIndex) {
                    video.pause();
                }
            });
        }

        function createPontos() {
            if (pontosContainer) {
                pontosContainer.innerHTML = '';
                for (let i = 0; i < totalItems; i++) {
                    const ponto = document.createElement('div');
                    ponto.classList.add('ponto');
                    ponto.dataset.index = i;
                    ponto.addEventListener('click', () => {
                        currentIndex = i;
                        updateCarrossel(true);
                    });
                    pontosContainer.appendChild(ponto);
                }
            }
            updatePontos();
        }



        function updatePontos() {
            if (pontosContainer) {

                // Marca o ponto ativo
                pontosContainer.querySelectorAll('.ponto').forEach((ponto, index) => {
                    ponto.classList.toggle('ativo', index === currentIndex);
                });
            }
        }

        function updateCarrossel(animated = true) {
            const offset = -currentIndex * (100 / totalItems);
            prevTranslate = offset; // Define o ponto de início para o próximo arrasto
            if (animated) {
                carrosselConteudo.style.transition = 'transform 0.4s ease-in-out';
            } else {
                carrosselConteudo.style.transition = 'none';
            }
            carrosselConteudo.style.transform = `translateX(${offset}%)`;
            updatePontos();
            pauseInactiveMedia();
        }

        // --- Funções de Drag e Swipe (Mouse e Toque) ---
        function getPositionX(event) {
            // Retorna a posição X do mouse ou do toque
            return event.type.includes('mouse') ? event.pageX : event.touches[0].clientX;
        }
        function startDrag(event) {
            if (totalItems <= 1) return;
            // Previne o drag padrão do navegador
            if (event.type === 'mousedown') event.preventDefault();
            isDragging = true;
            startX = getPositionX(event);
            carrossel.setAttribute('data-is-dragging', 'true');
            carrosselConteudo.style.transition = 'none'; // Desativa a transição suave para o arrasto
        }

        function onDrag(event) {
            if (!isDragging) return;
            const currentX = getPositionX(event);
            const dragDistance = currentX - startX;

            // Calcula o quanto arrastamos em relação à largura total
            const containerWidth = carrossel.clientWidth * totalItems;
            const percentTranslation = (dragDistance / containerWidth) * 100 * totalItems;
            currentTranslate = prevTranslate + percentTranslation;

            // Aplica a translação
            carrosselConteudo.style.transform = `translateX(${currentTranslate}%)`;
        }

        function endDrag(event) {
            if (!isDragging) return;
            isDragging = false;
            carrossel.removeAttribute('data-is-dragging');
            const currentX = getPositionX(event);
            const movedPixels = currentX - startX;
            const itemWidth = carrossel.clientWidth;
            const movedPercentage = Math.abs(movedPixels) / itemWidth;

            // Se moveu o suficiente, troca de slide
            if (movedPercentage > dragThreshold) {
                if (movedPixels < 0) { // Swiped left (próximo slide)
                    currentIndex = (currentIndex + 1) % totalItems;
                } else { // Swiped right (slide anterior)
                    currentIndex = (currentIndex - 1 + totalItems) % totalItems;
                }
            }

            // Volta para a posição correta (snap) com animação
            updateCarrossel(true);

            // Previne que um "click" seja disparado após um arrasto (importante para touch)
            if (movedPercentage > 0.05) {
                carrossel.addEventListener('click', preventClick, true);
            }
        }

        function preventClick(e) {
            e.stopPropagation();
            e.preventDefault();
            carrossel.removeEventListener('click', preventClick, true);
        }

        // --- Configuração e Event Listeners do Carrossel ---

        if (totalItems > 1) {

            // Configurações de largura
            carrosselConteudo.style.width = `${totalItems * 100}%`;
            midiaItens.forEach(item => {
                item.style.width = `${100 / totalItems}%`;
            });
           
            // Event Listeners dos botões
            if (prevBtn) {
                prevBtn.addEventListener('click', (event) => {
                    event.preventDefault();
                    currentIndex = (currentIndex - 1 + totalItems) % totalItems;
                    updateCarrossel(true);
                });
            }

            if (nextBtn) {
                nextBtn.addEventListener('click', (event) => {
                    event.preventDefault();
                    currentIndex = (currentIndex + 1) % totalItems;
                    updateCarrossel(true);
                });
            }

            // Event Listeners de Drag/Swipe (Mouse e Touch)
            carrossel.addEventListener('mousedown', startDrag);
            window.addEventListener('mousemove', onDrag);
            window.addEventListener('mouseup', endDrag);
            carrossel.addEventListener('touchstart', startDrag);
            carrossel.addEventListener('touchmove', onDrag);
            carrossel.addEventListener('touchend', endDrag);
            carrossel.addEventListener('touchcancel', endDrag);

            // Garante que o drag termine se o mouse sair da área
            carrossel.addEventListener('mouseleave', () => {
                if (isDragging) endDrag({});
            });
            createPontos();
        } else {

            // Esconde os controles se houver apenas um item
            if (prevBtn) prevBtn.style.display = 'none';
            if (nextBtn) nextBtn.style.display = 'none';
            if (pontosContainer) pontosContainer.style.display = 'none';
        }

        // Previne que vídeos capturem o clique/toque e atrapalhem o arrasto do carrossel
        videoElementos.forEach(video => {
            const stopPropagationOptions = { capture: true };
            video.addEventListener('mousedown', (e) => { e.stopPropagation(); }, stopPropagationOptions);
            video.addEventListener('touchstart', (e) => { e.stopPropagation(); }, stopPropagationOptions);
        });
        updateCarrossel(false); // Carregamento inicial
    }

    // =========================================================================

    // 2. LÓGICA DO MODAL DE CONFIRMAÇÃO DE EXCLUSÃO

    // =========================================================================

    const modalOverlay = document.getElementById('modal_confirmacao_exclusao');
    const btnConfirmar = document.getElementById('btn_confirmar_exclusao');
    const btnCancelar = document.getElementById('btn_cancelar_exclusao');
    const receitaNomeModal = document.getElementById('receita_nome_modal');
    let receitaIdParaExcluir = null;

    // Função global que é chamada pelo botão "Excluir" no HTML
    window.mostrarConfirmacaoExclusao = function(receitaId, receitaNome) {
        receitaIdParaExcluir = receitaId;
        if (receitaNomeModal) receitaNomeModal.textContent = receitaNome;
        if (modalOverlay) {
            modalOverlay.style.display = 'flex';
        }
    };

    function esconderModal() {
        if (modalOverlay) {
            modalOverlay.style.display = 'none';
        }
        receitaIdParaExcluir = null;
    }

    // Listener para Cancelar
    if (btnCancelar) {
        btnCancelar.addEventListener('click', esconderModal);
    }

    // Listener para Confirmar e Submeter o formulário POST
    if (btnConfirmar) {
        btnConfirmar.addEventListener('click', function() {
            if (receitaIdParaExcluir) {

                // Encontra e submete o formulário POST escondido
                const form = document.getElementById(`form_excluir_${receitaIdParaExcluir}`);
                if (form) {
                    form.submit();
                } else {
                    console.error('Formulário de exclusão não encontrado!');
                }
            }
            esconderModal();
        });
    }

    // Fechar o modal clicando no overlay
    if (modalOverlay) {
        modalOverlay.addEventListener('click', function(e) {
            if (e.target === modalOverlay) {
                esconderModal();
            }
        });
    }
});