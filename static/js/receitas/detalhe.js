document.addEventListener('DOMContentLoaded', () => {

    /* =========================================================================
     * 1. Lógica do Carrossel de Mídia
     * ========================================================================= */
    const carrossel = document.getElementById('carrossel_midia');
    if (carrossel) {
        const conteudo = carrossel.querySelector('.carrossel_conteudo');
        const items = carrossel.querySelectorAll('.midia_item');
        const prevBtn = carrossel.querySelector('.prev_btn');
        const nextBtn = carrossel.querySelector('.next_btn');
        const navPontosContainer = carrossel.querySelector('.pontos_navegacao');
        let currentIndex = 0;
        const totalItems = items.length;

        if (totalItems > 1) {
            // Cria os pontos de navegação
            for (let i = 0; i < totalItems; i++) {
                const ponto = document.createElement('span');
                ponto.classList.add('ponto');
                if (i === 0) ponto.classList.add('ativo');
                ponto.addEventListener('click', () => {
                    goToSlide(i);
                });
                navPontosContainer.appendChild(ponto);
            }

            const pontos = carrossel.querySelectorAll('.ponto');

            function updateCarrossel() {
                const offset = -currentIndex * 100;
                conteudo.style.transform = `translateX(${offset}%)`;
                
                pontos.forEach((p, i) => {
                    p.classList.toggle('ativo', i === currentIndex);
                });
            }

            function goToSlide(index) {
                currentIndex = index;
                updateCarrossel();
            }

            prevBtn.addEventListener('click', () => {
                currentIndex = (currentIndex > 0) ? currentIndex - 1 : totalItems - 1;
                updateCarrossel();
            });

            nextBtn.addEventListener('click', () => {
                currentIndex = (currentIndex < totalItems - 1) ? currentIndex + 1 : 0;
                updateCarrossel();
            });
            
            // Inicializa a posição
            updateCarrossel();
        }
    }


    /* =========================================================================
     * 2. Lógica do Modal de Confirmação de Exclusão (EXISTENTE NO HTML)
     * ========================================================================= */
    const modal = document.getElementById('modal_confirmacao_exclusao');
    const btnCancelar = document.getElementById('btn_cancelar_exclusao');
    const btnConfirmar = document.getElementById('btn_confirmar_exclusao');
    const receitaNomeModal = document.getElementById('receita_nome_modal');
    let receitaIdParaExcluir = null;

    if (modal) {
        // Função global para ser chamada pelo 'onclick' no template
        window.mostrarConfirmacaoExclusao = (receitaId, nomeReceita) => {
            receitaIdParaExcluir = receitaId;
            receitaNomeModal.textContent = nomeReceita;
            modal.style.display = 'flex'; // Exibe o modal
        };

        const esconderModal = () => {
            modal.style.display = 'none'; // Esconde o modal
            receitaIdParaExcluir = null;
        };

        btnCancelar.addEventListener('click', esconderModal);
        
        // Clica no overlay para fechar (opcional)
        modal.addEventListener('click', (e) => {
            if (e.target === modal) {
                esconderModal();
            }
        });

        // Confirma e submete o formulário escondido
        btnConfirmar.addEventListener('click', () => {
            if (receitaIdParaExcluir) {
                const form = document.getElementById(`form_excluir_${receitaIdParaExcluir}`);
                if (form) {
                    form.submit(); // Submete o formulário POST
                }
            }
            esconderModal();
        });
    }

    /* =========================================================================
     * 3. Lógica do Botão Favoritar (NOVA)
     * ========================================================================= */
    const btnFavoritar = document.getElementById('btn_favoritar');
    
    // Verifica se o botão e as variáveis globais do Django existem (usuário logado)
    if (btnFavoritar && typeof RECEITA_ID !== 'undefined') {
        const iconeFavorito = document.getElementById('icone_favorito');
        const textoFavorito = btnFavoritar.querySelector('.texto_favorito');

        btnFavoritar.addEventListener('click', async () => {
            
            btnFavoritar.disabled = true; // Desabilita o botão
            
            // Determina se a receita está favoritada atualmente
            const isFavoritado = btnFavoritar.classList.contains('favoritado');
            
            try {
                // Requisição POST para o endpoint de favoritos
                const response = await fetch(FAVORITAR_URL, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': CSRF_TOKEN
                    },
                    // Opcional: enviar o estado atual no corpo da requisição
                    body: JSON.stringify({
                        receita_id: RECEITA_ID,
                        action: isFavoritado ? 'desfavoritar' : 'favoritar'
                    })
                });

                if (!response.ok) {
                    throw new Error(`Erro de rede ou servidor: ${response.status}`);
                }

                const data = await response.json();

                if (data.status === 'success') {
                    // Atualiza a interface baseada no novo estado retornado
                    const novoStatus = data.novo_status; 

                    if (novoStatus === 'favoritado') {
                        btnFavoritar.classList.add('favoritado');
                        iconeFavorito.classList.remove('fa-heart-o');
                        iconeFavorito.classList.add('fa-heart');
                        textoFavorito.textContent = 'Desfavoritar';
                        btnFavoritar.setAttribute('aria-label', 'Desfavoritar');
                        btnFavoritar.setAttribute('title', 'Remover dos Favoritos');

                    } else if (novoStatus === 'desfavoritado') {
                        btnFavoritar.classList.remove('favoritado');
                        iconeFavorito.classList.remove('fa-heart');
                        iconeFavorito.classList.add('fa-heart-o');
                        textoFavorito.textContent = 'Favoritar';
                        btnFavoritar.setAttribute('aria-label', 'Favoritar');
                        btnFavoritar.setAttribute('title', 'Adicionar aos Favoritos');
                    }
                } else {
                    console.error('Falha na operação:', data.message || 'Ocorreu um erro.');
                }

            } catch (error) {
                console.error('Erro ao processar a requisição de favoritos:', error);
            } finally {
                btnFavoritar.disabled = false; // Reabilita o botão
            }
        });
    }
});