# Arquitetura do Sistema de Conferência de Estoque
> Sistema de validação de localização de rolos de tecido integrado ao SAP Business One

---

## Visão Geral

O sistema tem como objetivo **escanear rolos de tecido por QR Code**, comparar a localização física com a esperada no SAP B1, registrar divergências e gerar relatórios operacionais.

---

## Parte 1 — Contexto do Problema

### Situação atual
- Estoque com centenas de rolos de tecido em tubos
- Prateleiras identificadas com QR Code (ex: `TEC01.A`, `B01`, `B02`)
- Rolos identificados apenas por **etiqueta impressa** (sem QR Code ainda)
- Localização dos itens deveria estar no SAP, mas não há validação física
- Erros de picking e itens fora do lugar ocorrem com frequência

### O que o sistema resolve
- Operador escaneia a prateleira + o rolo
- Sistema valida se o rolo está no lugar certo
- Registra divergências com hora, local e operador
- Gera relatório exportável em Excel

---

## Parte 2 — Stack Tecnológica

| Camada | Tecnologia | Motivo |
|---|---|---|
| Linguagem | Python 3.11+ | Domínio do time |
| Interface | Streamlit | Visual rápido, só Python |
| Banco local | SQLite | Sem instalação, ideal para MVP |
| Banco futuro | PostgreSQL | Se o projeto crescer |
| Relatórios | pandas + openpyxl | Geração de Excel |
| QR Code | qrcode + pillow | Geração de etiquetas |
| Leitura | Scanner USB | Plug and play, sem câmera |
| Integração SAP | requests | Chamadas REST ao Service Layer |
| Versionamento | Git + GitHub | Controle de versão |

### Instalação das dependências
```bash
pip install streamlit pandas openpyxl qrcode pillow requests python-dotenv sqlalchemy
```

---

## Parte 3 — Estrutura de Pastas

```
sistema-estoque/
│
├── app/
│   ├── main.py               # Ponto de entrada Streamlit
│   ├── pages/
│   │   ├── login.py          # Tela de login
│   │   ├── scan.py           # Tela de escaneamento
│   │   ├── validation.py     # Tela de validação
│   │   └── report.py         # Tela de relatório
│   │
│   ├── services/
│   │   ├── scan_service.py   # Lógica de escaneamento
│   │   ├── sap_service.py    # Integração com SAP
│   │   └── report_service.py # Geração de relatórios
│   │
│   ├── database/
│   │   ├── db.py             # Conexão SQLite
│   │   └── models.py         # Tabelas do banco
│   │
│   └── utils/
│       ├── qr_generator.py   # Geração de QR Codes
│       └── importer.py       # Importação de Excel
│
├── data/
│   ├── estoque.db            # Banco SQLite
│   └── imports/              # Arquivos Excel importados
│
├── .env                      # Variáveis de ambiente (SAP, senhas)
├── requirements.txt
└── README.md
```

---

## Parte 4 — Banco de Dados

### Tabela: `operators` (operadores)
```sql
id          INTEGER PRIMARY KEY
name        TEXT NOT NULL
badge       TEXT UNIQUE        -- matrícula
created_at  DATETIME
```

### Tabela: `items` (rolos de tecido)
```sql
id                INTEGER PRIMARY KEY
item_code         TEXT UNIQUE        -- ex: TC.000.296
description       TEXT               -- ex: Tecido Screen Blackout
lot               TEXT               -- ex: TEC01.A.N02
quantity_m2       REAL               -- metragem atual
expected_location TEXT               -- localização esperada (vinda do SAP)
sap_warehouse     TEXT               -- depósito no SAP
created_at        DATETIME
```

### Tabela: `locations` (prateleiras)
```sql
id            INTEGER PRIMARY KEY
location_code TEXT UNIQUE    -- ex: TEC01.A, B02
sector        TEXT           -- ex: TEC01
shelf         TEXT           -- ex: A, B
level         TEXT           -- ex: 01, 02
qr_data       TEXT           -- conteúdo do QR Code
```

### Tabela: `scans` (escaneamentos)
```sql
id                INTEGER PRIMARY KEY
item_code         TEXT
scanned_location  TEXT           -- onde foi encontrado
expected_location TEXT           -- onde deveria estar
operator_id       INTEGER
status            TEXT           -- CORRETO / DIVERGENTE / NAO_ENCONTRADO
created_at        DATETIME
sent_to_sap       BOOLEAN DEFAULT FALSE
sap_response      TEXT
```

### Tabela: `divergences` (divergências)
```sql
id                INTEGER PRIMARY KEY
scan_id           INTEGER
item_code         TEXT
expected_location TEXT
found_location    TEXT
resolved          BOOLEAN DEFAULT FALSE
resolved_at       DATETIME
resolved_by       INTEGER
```

---

## Parte 5 — Telas do Sistema

### Tela 1: Login
- Campo de nome ou matrícula do operador
- Sem senha complexa (uso em estoque)

### Tela 2: Escaneamento
```
[ Escanear Prateleira ] → campo recebe QR Code da prateleira
[ Escanear Rolo ]       → campo recebe QR Code do rolo
[ Validar ]             → botão de confirmação
```

### Tela 3: Resultado da Validação
```
✅ CORRETO
   Item: TC.000.296 — Tecido Screen Blackout
   Local escaneado:  TEC01.A
   Local esperado:   TEC01.A

❌ DIVERGENTE
   Item: TC.000.290 — Tecido Essentials Grey
   Local escaneado:  B02
   Local esperado:   TEC01.A  ← deveria estar aqui
```

### Tela 4: Relatório
- Total de itens escaneados
- Itens corretos vs divergentes
- Filtro por operador, data, setor
- Botão: **Exportar Excel**

---

## Parte 6 — Fluxo Completo do Sistema

```
[Rolo físico com QR Code impresso pelo sistema]
              ↓
[Operador faz login no sistema]
              ↓
[Escaneia QR Code da prateleira]  →  TEC01.A / B02
              ↓
[Escaneia QR Code do rolo]  →  TC.000.296
              ↓
[Sistema busca localização esperada no banco local]
              ↓
[Compara localização escaneada x esperada]
              ↓
      ┌───────┴───────┐
      ✅ CORRETO      ❌ DIVERGENTE
      │               │
      Registra OK     Registra divergência
                      Mostra onde deveria estar
              ↓
[Relatório gerado com todas as ocorrências]
              ↓
[Exportação Excel / Envio ao SAP (quando disponível)]
```

---

## Parte 7 — Geração de QR Codes para os Rolos

Como os rolos **não têm QR Code hoje**, o sistema vai gerar e imprimir.

### Conteúdo do QR Code do rolo
```
TC.000.296|TEC01.A.N02|Tecido Screen Blackout
```

### Conteúdo do QR Code da prateleira (já existente)
```
TEC01.A
B01
B02
```

### Funcionalidade de geração no sistema
1. Importar Excel com lista de itens
2. Sistema gera QR Code para cada item
3. Gera PDF/imagem para impressão em etiqueta
4. Operador cola no rolo físico

---

## Parte 8 — Integração com SAP B1

> Esta fase só começa após o MVP local estar funcionando.

### Pré-requisitos a confirmar com a empresa
- [ ] SAP B1 versão (10.0 recomendado)
- [ ] Service Layer ativo na empresa
- [ ] URL do Service Layer: `https://servidor:50000/b1s/v2`
- [ ] Usuário técnico para API
- [ ] Ambiente de teste disponível

### Fluxo de autenticação SAP
```python
POST /b1s/v2/Login
{
  "CompanyDB": "nome_empresa",
  "UserName": "usuario_api",
  "Password": "senha"
}
# Retorna cookie B1SESSION para próximas chamadas
```

### O que buscar no SAP
| Dado | Endpoint SAP |
|---|---|
| Lista de itens | `GET /Items` |
| Código de barras do item | `GET /BarCodes` |
| Depósitos | `GET /Warehouses` |
| Posições de prateleira | `GET /BinLocations` |
| Transferências de estoque | `POST /StockTransfers` |
| Contagem de inventário | `POST /InventoryCountings` |

### Política de segurança
- **Nunca gravar direto no SAP produtivo**
- Sempre usar ambiente de homologação para testes
- Toda movimentação no SAP exige aprovação humana antes do envio
- Sistema salva localmente mesmo se SAP estiver offline

---

## Parte 9 — Fases de Desenvolvimento

### Fase 1 — MVP Local (sem SAP)
- [ ] Criar banco SQLite com tabelas
- [ ] Tela de login
- [ ] Tela de escaneamento
- [ ] Lógica de validação
- [ ] Tela de resultado
- [ ] Tela de relatório
- [ ] Exportação Excel

### Fase 2 — QR Codes e Importação
- [ ] Importar Excel com itens genéricos
- [ ] Gerar QR Codes dos rolos
- [ ] Imprimir etiquetas para teste físico

### Fase 3 — Integração SAP (quando disponível)
- [ ] Testar autenticação no Service Layer
- [ ] Buscar itens reais do SAP
- [ ] Buscar localizações reais
- [ ] Enviar divergências validadas ao SAP

### Fase 4 — Dados Reais
- [ ] Importar Excel real exportado do SAP
- [ ] Piloto com setor específico do estoque
- [ ] Ajustes com base no uso real

---

## Parte 10 — Requisitos Funcionais

- O sistema deve permitir login por operador
- O sistema deve ler QR Code de prateleira e de rolo
- O sistema deve comparar localização escaneada com esperada
- O sistema deve registrar data, hora e operador em cada scan
- O sistema deve indicar claramente se o item está correto ou divergente
- O sistema deve mostrar onde o item deveria estar em caso de divergência
- O sistema deve gerar relatório de todos os escaneamentos
- O sistema deve exportar relatório em Excel
- O sistema deve importar lista de itens via Excel
- O sistema deve gerar QR Codes para os rolos
- O sistema deve funcionar offline (sem SAP disponível)
- O sistema deve registrar histórico completo de escaneamentos

## Requisitos Não Funcionais

- Funcionar em rede local da empresa
- Não gravar diretamente no banco do SAP
- Ter validação antes de qualquer envio ao SAP
- Ser simples para uso por operadores em estoque
- Ter backup do banco intermediário
- Ter logs de erro
- Ambiente de teste separado do SAP produtivo

---

## Parte 11 — Entregáveis do Projeto (TCC)

- [ ] Documento de diagnóstico do processo atual
- [ ] Fluxograma do processo atual
- [ ] Fluxograma do processo proposto
- [ ] Este documento de arquitetura
- [ ] Protótipo funcional do sistema
- [ ] Banco de dados com histórico de escaneamentos
- [ ] Gerador de QR Codes para rolos
- [ ] Relatório de divergências em Excel
- [ ] Modelo de integração com SAP B1
- [ ] Matriz de requisitos
- [ ] Indicadores de resultado esperados:
  - Redução de erros de picking
  - Redução do tempo de busca de item
  - Aumento da acuracidade de estoque
  - Rastreabilidade por operador

---

## Resumo Executivo

> **Criar uma solução em Python para conferência física de rolos de tecido por leitura de QR Code, validando a localização real contra a localização esperada no SAP Business One, registrando divergências e gerando relatórios para reduzir erros de picking e melhorar a organização do estoque.**
