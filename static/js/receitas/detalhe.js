document.addEventListener('DOMContentLoaded', function() {
    const carrossel = document.getElementById('carrossel_midia');
    
    // Inicia a lógica do carrossel apenas se o elemento for encontrado
    if (carrossel) {
        const carrosselConteudo = carrossel.querySelector('.carrossel_conteudo');
        const midiaItens = carrossel.querySelectorAll('.midia_item');
        const prevBtn = carrossel.querySelector('.prev_btn');
        const nextBtn = carrossel.querySelector('.next_btn');
        const pontosContainer = carrossel.querySelector('.pontos_navegacao');

        let currentIndex = 0;
        const totalItems = midiaItens.length;

        if (totalItems <= 1) {
            if (prevBtn) prevBtn.style.display = 'none';
            if (nextBtn) nextBtn.style.display = 'none';
            if (pontosContainer) pontosContainer.style.display = 'none';
        } else {
             // Configura a largura total e dos itens
            carrosselConteudo.style.width = `${totalItems * 100}%`;
            midiaItens.forEach(item => {
                item.style.width = `${100 / totalItems}%`;
            });
            
            function updateCarrossel() {
                const offset = -currentIndex * (100 / totalItems);
                carrosselConteudo.style.transform = `translateX(${offset}%)`;
                updatePontos();
            }

            if (prevBtn) {
                prevBtn.addEventListener('click', (event) => {
                    event.preventDefault(); 
                    currentIndex = (currentIndex - 1 + totalItems) % totalItems;
                    updateCarrossel();
                });
            }

            if (nextBtn) {
                nextBtn.addEventListener('click', (event) => {
                    event.preventDefault(); 
                    currentIndex = (currentIndex + 1) % totalItems;
                    updateCarrossel();
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
                            updateCarrossel();
                        });
                        pontosContainer.appendChild(ponto);
                    }
                    updatePontos();
                }
            }

            function updatePontos() {
                if (pontosContainer) {
                    const pontos = pontosContainer.querySelectorAll('.ponto');
                    pontos.forEach((ponto, index) => {
                        ponto.classList.toggle('ativo', index === currentIndex);
                    });
                }
            }

            createPontos();
            updateCarrossel();
        }
    }

    // --- LÓGICA DO MODAL DE EXCLUSÃO ---
    const modalOverlay = document.getElementById('modal_confirmacao_exclusao');
    const btnConfirmar = document.getElementById('btn_confirmar_exclusao');
    const btnCancelar = document.getElementById('btn_cancelar_exclusao');
    const receitaNomeModal = document.getElementById('receita_nome_modal');
    
    let receitaIdParaExcluir = null;

    /**
     * Exibe o modal de confirmação.
     * Esta função é chamada pelo botão "Excluir" no HTML.
     */
    window.mostrarConfirmacaoExclusao = function(receitaId, receitaNome) {
        receitaIdParaExcluir = receitaId;
        if (receitaNomeModal) receitaNomeModal.textContent = receitaNome;
        if (modalOverlay) {
            modalOverlay.style.display = 'flex'; // Usa flex para centralizar
        }
    };

    function esconderModal() {
        if (modalOverlay) {
            modalOverlay.style.display = 'none';
        }
        receitaIdParaExcluir = null;
    }

    // Botão Cancelar
    if (btnCancelar) {
        btnCancelar.addEventListener('click', esconderModal);
    }

    // Botão Confirmar (Submeter Formulário)
    if (btnConfirmar) {
        btnConfirmar.addEventListener('click', function() {
            if (receitaIdParaExcluir) {
                // Encontra o formulário oculto pelo ID dinâmico
                const form = document.getElementById(`form_excluir_${receitaIdParaExcluir}`);
                if (form) {
                    form.submit(); // Envia o POST de exclusão
                } else {
                    console.error('Formulário de exclusão não encontrado!');
                }
            }
            esconderModal();
        });
    }
    
    // Fechar ao clicar fora
    if (modalOverlay) {
        modalOverlay.addEventListener('click', function(e) {
            if (e.target === modalOverlay) {
                esconderModal();
            }
        });
    }
});