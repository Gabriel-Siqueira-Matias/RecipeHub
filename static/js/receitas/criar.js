document.addEventListener('DOMContentLoaded', function() {

    // Função principal para gerenciar os formsets dinâmicos.
    function setupFormset(formsetId) {
        const container = document.getElementById(`${formsetId}-form-list`);
        const addButton = document.querySelector(`.btn_add_formset[data-formset-id="${formsetId}"]`);
        const totalFormsInput = document.getElementById(`id_${formsetId}-TOTAL_FORMS`);
        // O template vazio AGORA DEVE SER A TAG <template>
        const emptyFormTemplateTag = document.getElementById(`${formsetId}-empty-form-template`);
        
        // Verificação de segurança: se algum elemento essencial estiver faltando, aborta.
        if (!container || !addButton || !totalFormsInput || !emptyFormTemplateTag) {
            console.warn(`Formset não encontrado para ID: ${formsetId}. Inicialização abortada.`);
            return;
        }

        // -----------------------------------------------------------
        // 1. Função de Adicionar Formulário
        // -----------------------------------------------------------
        function addForm(e) {
            e.preventDefault();
            
            let currentTotal = parseInt(totalFormsInput.value);
            
            // 1. Clona o conteúdo do template (<div class="... form_row">...</div>)
            const newFormContent = emptyFormTemplateTag.content.cloneNode(true);
            
            // O novo formulário (a linha .form_row) é o primeiro filho do conteúdo clonado.
            const newFormRow = newFormContent.firstElementChild;
            
            // 2. Itera sobre todos os elementos para substituir '__prefix__'
            // Isso precisa ser feito em todos os atributos 'id', 'name' e 'for'
            newFormRow.querySelectorAll('*').forEach(element => {
                // Substituir IDs
                if (element.id) {
                    element.id = element.id.replace(/__prefix__/g, currentTotal);
                }
                // Substituir Names
                if (element.name) {
                    element.name = element.name.replace(/__prefix__/g, currentTotal);
                }
                // Substituir For (para as labels)
                if (element.getAttribute('for')) {
                    element.setAttribute('for', element.getAttribute('for').replace(/__prefix__/g, currentTotal));
                }
            });
            
            // 3. Insere o novo formulário na lista
            container.appendChild(newFormRow);
            
            // 4. Incrementa o TOTAL_FORMS
            totalFormsInput.value = currentTotal + 1;
            
            // 5. Adiciona o listener de remoção ao novo campo
            setupDeleteListener(newFormRow);
            
            // Opcional: foca no primeiro campo do novo formulário para melhorar a UX
            newFormRow.querySelector('input, select, textarea')?.focus();
        }
        
        // -----------------------------------------------------------
        // 2. Função de Configurar Listener de Remoção (Checkbox DELETE)
        // -----------------------------------------------------------
        function setupDeleteListener(formRow) {
            const deleteInput = formRow.querySelector('input[type="checkbox"][id$="-DELETE"]');
            
            if (deleteInput) {
                // Esconde a label padrão gerada pelo Django e garante que o checkbox esteja visível
                const deleteContainer = deleteInput.closest('.campo_delete');
                if (deleteContainer) {
                    const label = deleteContainer.querySelector('label');
                    // A label já está escondida por CSS, mas garante que não atrapalhe
                    if(label) label.style.display = 'none'; 
                    deleteInput.style.display = 'block'; 
                }

                // Efeito visual de marcação para deletar
                deleteInput.addEventListener('change', function() {
                    const row = this.closest('.form_row');
                    if (row) {
                        // Aplica ou remove a cor de fundo mais escura ao marcar para deletar
                        row.style.backgroundColor = this.checked ? '#795252' : ''; 
                        
                        // Desabilita/habilita outros campos na linha (melhora a UX)
                        row.querySelectorAll('input:not([type="hidden"]):not([id$="-DELETE"]), select, textarea').forEach(field => {
                            field.disabled = this.checked;
                        });
                    }
                });
                
                // Aplica o efeito visual inicial, caso o campo tenha sido preenchido e marcado como delete (ex: edição)
                if (deleteInput.checked) {
                    deleteInput.dispatchEvent(new Event('change'));
                }
            }
        }

        // -----------------------------------------------------------
        // 3. Inicialização
        // -----------------------------------------------------------
        // 1. Configura o evento de clique para o botão de adicionar
        addButton.addEventListener('click', addForm);

        // 2. Configura o listener de remoção para todos os campos existentes
        container.querySelectorAll('.form_row').forEach(setupDeleteListener);
    }

    // Inicializa todos os formsets que precisam de funcionalidade dinâmica
    setupFormset('ingredientes');
    setupFormset('etapas');
    setupFormset('midias');
});