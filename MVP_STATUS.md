# Status do MVP: Sistema de Conferência de Estoque (Stoki)
> **Data de Atualização:** 11 de Maio de 2026
> **Ambiente Atual:** Produção (Streamlit Community Cloud + Supabase PostgreSQL)

---

## 🚀 1. O que o Sistema JÁ FAZ (Funcionalidades Concluídas)

O sistema atual opera como um **MVP Independente (Produto Mínimo Viável)**. Isso significa que ele possui toda a base de validação e rastreabilidade necessária para ser usado isoladamente, sem depender do SAP B1.

### 🔐 Autenticação e Segurança
- **Login e Cadastro de Operadores:** Fluxo completo de cadastro de novos usuários com e-mail e senha.
- **Recuperação de Senha:** Mecanismo básico de reset de senha para operadores.
- **Controle de Sessão:** Proteção de rotas, impedindo acesso às telas sem estar logado.

### 📱 Escaneamento e Validação (Mobile/Desktop)
- **Leitura via Câmera:** Capacidade de ler QR Codes tanto das Prateleiras quanto dos Rolos utilizando a câmera do celular ou notebook.
- **Entrada Manual:** Permite a digitação manual dos códigos caso a câmera não consiga focar.
- **Validação de Localização (Bipagem):** Cruzamento automático entre o "local onde o rolo foi encontrado" e o "local onde ele deveria estar" (baseado na importação de dados).
- **Alerta de Divergências:** Telas visuais de sucesso (Verde) para itens corretos, e telas de Alerta (Vermelho) para itens que estão na prateleira errada, informando imediatamente ao operador onde o item deveria estar.

### 📦 Importação e Geração de Etiquetas
- **Importação em Lote via Excel:** Upload de planilhas para popular a base de dados em massa com as informações dos rolos (Código, Descrição, Local Esperado).
- **Download de Planilha Modelo:** O sistema fornece uma planilha padrão para preenchimento.
- **Geração de QR Codes:** Geração dinâmica de QR Codes para todos os itens cadastrados no banco de dados, entregues em um arquivo `.zip` pronto para impressão.
- **QR Codes de Teste:** Exibição de QR Codes pré-renderizados na tela para facilitar testes rápidos pelo celular.

### 📊 Rastreabilidade e Relatórios
- **Dashboard de Histórico:** Tabela completa listando quem escaneou, qual item, quando, e se o item estava correto ou divergente.
- **Rastreamento de Operador:** Todo scan é vinculado ao operador logado.
- **Exportação de Dados:** Geração de um arquivo Excel detalhado (Log de auditoria) com todo o histórico de operações do armazém.

### ☁️ Infraestrutura
- **Banco de Dados em Nuvem (Supabase):** Substituição do SQLite local por um banco PostgreSQL robusto, com *Connection Pooling* para suportar múltiplos usuários simultâneos.
- **Hospedagem (Streamlit Cloud):** Sistema 100% online, acessível por qualquer dispositivo móvel via navegador, sem necessidade de instalação de aplicativos.

---

## 🎯 2. Próximas Funcionalidades (Roadmap de Implementação)

As funções a seguir representam os próximos passos evolutivos do sistema. Podemos começar a implementar qualquer uma delas de acordo com a prioridade da empresa.

### 🔼 Prioridade Alta
1. **Baixa Automática (Saída de Material):**
   - **Descrição:** Criar um fluxo específico onde o operador "Bipa" um rolo para informar que ele está sendo retirado do estoque e levado para a máquina de corte.
   - **Por que fazer:** Atualmente o sistema rastreia *onde* o item está (conferência), mas não tira ele do inventário quando é consumido.

2. **Integração com SAP B1 - Fase 1 (Leitura):**
   - **Descrição:** Conectar a API do sistema com o *Service Layer* do SAP para puxar automaticamente a lista de itens, descrições e depósitos esperados, eliminando a necessidade de importar planilhas do Excel manualmente.
   - **Pré-requisito:** Liberação de IP, Usuário e Senha da API do SAP B1 pela equipe de TI.

### 🔀 Prioridade Média
3. **Resolução de Divergências no App:**
   - **Descrição:** Quando o operador acha um item na prateleira errada, permitir que um supervisor valide no próprio celular um botão de "Atualizar Localização", transferindo oficialmente o rolo para a nova prateleira.

4. **Recuperação de Senha por E-mail (SMTP):**
   - **Descrição:** Melhorar a segurança da redefinição de senha, enviando um link temporário para o e-mail do operador, substituindo a mensagem de tela atual.

### 🔄 Prioridade Baixa / Futuro
5. **Integração com SAP B1 - Fase 2 (Escrita e Transferência):**
   - **Descrição:** Fazer com que toda bipagem realizada no celular (seja de correção de prateleira ou de saída para produção) reflita instantaneamente em uma "Transferência de Estoque (StockTransfers)" lá dentro do banco do SAP.
   - **Por que é futuro:** Exige homologação rigorosa para evitar "quebrar" ou bagunçar os registros financeiros e fiscais do SAP em produção.

6. **Dashboard Gráfico de Produtividade:**
   - **Descrição:** Gráficos mostrando quantos rolos cada operador bipou no dia, taxa de acerto do estoque e tempo médio de conferência.
