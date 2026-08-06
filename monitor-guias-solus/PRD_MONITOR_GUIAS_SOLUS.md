# 📋 PRD — Monitor de Guias Solus
**Documento de Requisitos do Produto — v1.1.0**
**Última atualização:** 06/08/2026 | **Autor:** @henrikcampos7-max
**Repositório:** https://github.com/henrikcampos7-max/agentic-awesome-skills
**Caminho local:** `C:\Users\phenrique\.gemini\antigravity\scratch\agentic-awesome-skills\monitor-guias-solus`

---

> [!IMPORTANT]
> **Guia para IAs que assumirem o projeto:** Leia este documento antes de escrever qualquer código.
> Todo o estado atual está documentado aqui. Respeite a arquitetura e o checklist. Não reescreva código já entregue — apenas complemente.

---

## 🎯 1. Visão do Produto

### 1.1 Problema
A **Farmácia Oncológica de Cacoal (RO)** monitora manualmente guias de autorização no sistema **Solus** (Unimed). A equipe precisa entrar repetidamente para verificar mudanças de status, causando:
- Perda de tempo operacional
- Risco de atraso no início de tratamentos
- Falta de rastreabilidade das alterações

### 1.2 Solução
Aplicação **desktop Windows** que:
1. Monitora guias no Solus de forma automática
2. Exibe painel de controle em tempo real
3. Notifica mudanças de status via notificação Windows
4. Registra auditoria completa com conformidade LGPD

### 1.3 Usuários-Alvo
| Perfil | Unidade | Acesso |
|--------|---------|--------|
| Farmacêutico responsável | Cacoal | Total |
| Auxiliar de farmácia | Cacoal | Visualização |
| Gestor regional | Ji-Paraná (futuro) | Relatórios |

### 1.4 Contexto Futuro (Ecossistema Maior)
- **Controle de Estoque Oncológico** (integração futura)
- **Lista de Compras Automatizada** (integração futura)
- **Automações do GEMED** (integração futura)
- **WhatsApp Institucional** (integração futura)
- **Expansão para Ji-Paraná** (fase 2)

---

## 🏗️ 2. Arquitetura de Software

### 2.1 Stack Tecnológica
| Camada | Tecnologia | Versão | Status |
|--------|-----------|--------|--------|
| Interface | PySide6 | 6.7.0 | ✅ Implementado |
| Banco de Dados | SQLite3 (nativo) | — | ✅ Implementado |
| Agendador | APScheduler | 3.10.4 | ✅ Implementado |
| Notificações | win10toast | 0.9 | ✅ Implementado |
| Testes | pytest + pytest-cov | 7.4.3 | ✅ Implementado |
| Build | PyInstaller | latest | ⏳ Pendente |
| CI/CD | GitHub Actions | — | ✅ Workflow criado |

### 2.2 Estrutura de Pastas (Estado Atual)

```
monitor-guias-solus/
├── src/
│   ├── main.py                    ✅ Criado
│   ├── adapters/
│   │   ├── __init__.py            ✅ Criado
│   │   ├── solus_adapter.py       ✅ Interface ABC criada
│   │   └── simulator.py           ✅ Mock com 10 guias simuladas
│   ├── database/
│   │   ├── __init__.py            ✅ Criado
│   │   └── schema.py              ✅ SQLite com 4 tabelas + índices
│   ├── models/
│   │   ├── __init__.py            ✅ Criado
│   │   └── guide.py               ✅ Guide, GuideHistory, Settings
│   ├── services/
│   │   ├── __init__.py            ✅ Criado
│   │   ├── repository.py          ✅ GuideRepository com filtros
│   │   ├── monitor.py             ✅ MonitorService
│   │   ├── history.py             ✅ HistoryService com LGPD
│   │   ├── notifier.py            ✅ Windows Toast
│   │   └── scheduler.py           ✅ APScheduler 60min
│   ├── ui/
│   │   ├── __init__.py            ✅ Criado
│   │   ├── main_window.py         ✅ Janela principal PySide6
│   │   ├── styles/
│   │   │   ├── __init__.py        ✅ Criado
│   │   │   └── stylesheet.py      ✅ Estilo visual profissional
│   │   └── widgets/
│   │       ├── __init__.py        ✅ Criado
│   │       ├── dashboard.py       ✅ 4 cards de indicadores
│   │       ├── table.py           ✅ Tabela com cores por status
│   │       ├── filters.py         ✅ Filtros de status/período
│   │       └── dialogs.py         ⚠️ ARQUIVO VAZIO — precisa ser implementado
│   └── utils/
│       ├── __init__.py            ✅ Criado
│       ├── constants.py           ✅ Constantes do sistema
│       └── logger.py              ✅ Logger com hash de PII (LGPD)
├── tests/
│   ├── __init__.py                ✅ Criado
│   ├── conftest.py                ✅ Fixtures compartilhadas
│   ├── test_database.py           ✅ 10 testes
│   ├── test_repository.py         ✅ 11 testes
│   ├── test_services.py           ✅ 5 testes
│   └── test_models.py             ✅ 8 testes
├── .gitignore                     ✅ Criado
├── requirements.txt               ✅ Criado
├── pytest.ini                     ✅ Criado
├── README.md                      ✅ Criado
├── ESPECIFICACAO_COMPLETA.md      ✅ Criado (API docs + banco detalhado)
└── DEPLOYMENT.md                  ✅ Criado (PyInstaller + produção)
```

### 2.3 Diagrama de Camadas

```
┌─────────────────────────────────────────────────┐
│              UI Layer (PySide6)                 │
│  MainWindow → DashboardPanel → GuideTable       │
│              FiltersPanel → Dialogs             │
├─────────────────────────────────────────────────┤
│             Services Layer                      │
│  MonitorService  │ HistoryService               │
│  NotificationService │ SyncScheduler            │
├─────────────────────────────────────────────────┤
│           Repository Layer                      │
│              GuideRepository                    │
├─────────────────────────────────────────────────┤
│            Database Layer (SQLite)              │
│  guides │ history │ audit_log │ settings        │
├─────────────────────────────────────────────────┤
│              Adapters Layer                     │
│  SolusAdapterInterface │ SimulatedAdapter       │
│  [PENDENTE] SolusWebAdapter (scraping real)     │
└─────────────────────────────────────────────────┘
```

---

## 🗄️ 3. Modelo do Banco de Dados

### Tabela `guides` ✅
```sql
CREATE TABLE guides (
    id                INTEGER PRIMARY KEY AUTOINCREMENT,
    numero_guia       TEXT NOT NULL UNIQUE,
    paciente          TEXT NOT NULL,
    status            TEXT NOT NULL DEFAULT 'Guia emitida / liberada',
    ultima_consulta   TIMESTAMP,
    ultima_alteracao  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ciencia_status    TEXT DEFAULT 'Pendente',  -- 'Pendente' | 'Ciente'
    ciencia_timestamp TIMESTAMP,
    criado_em         TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Tabela `history` ✅
```sql
CREATE TABLE history (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    guide_id        INTEGER NOT NULL,
    status_anterior TEXT,
    status_novo     TEXT NOT NULL,
    timestamp       TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    usuario         TEXT DEFAULT 'Sistema',
    observacoes     TEXT,
    FOREIGN KEY (guide_id) REFERENCES guides(id)
);
```

### Tabela `audit_log` ✅ (LGPD)
```sql
CREATE TABLE audit_log (
    id               INTEGER PRIMARY KEY AUTOINCREMENT,
    acao             TEXT NOT NULL,
    tabela           TEXT,
    registro_id      INTEGER,
    usuario          TEXT DEFAULT 'Sistema',
    ip_address       TEXT,
    dados_anteriores TEXT,
    dados_novos      TEXT,
    timestamp        TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Tabela `settings` ✅
```sql
CREATE TABLE settings (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    chave         TEXT NOT NULL UNIQUE,
    valor         TEXT,
    tipo          TEXT,
    criado_em     TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Status possíveis
```python
STATUSES = [
    "Guia emitida / liberada",
    "Guia negada",
    "Guia cancelada",
    "Guia pedido/aguard confirmação",
    "Guia com setor de OPME",
    "Sob auditoria na Unimed origem",
    "Guia parcialmente liberada",
    "Cancelada na Unimed origem",
    "Negada na Unimed origem",
    "Guia sob auditoria"
]
```

---

## 🎨 4. Protótipos de Telas

### Tela 1 — Main Dashboard ✅ Implementado
```
┌──────────────────────────────────────────────────────────────┐
│  MONITOR DE GUIAS - SOLUS                             v1.0.0 │
│  Última sync: 11:00  🟢 Ativo  [🔄 Sincronizar]  [⚙️]       │
├──────────────────────────────────────────────────────────────┤
│  [➕ Nova Guia]                                              │
├────────────┬────────────┬────────────┬────────────────────────┤
│ 📋 32      │ 🔔 05      │ ⚠️ 07     │ ❌ 01                  │
│ Em monit.  │ Atualiz.   │ Pend.Cien. │ Erros                  │
├────────────┴────────────┴────────────┴────────────────────────┤
│ FILTROS: Status [Todos ▼]  De:[01/05] Até:[05/08]            │
│ ☑ Somente hoje   ☐ Somente pendentes de ciência               │
├──────┬───────────┬───────────────────┬─────────────┬──────────┤
│ Cor  │ Nº Guia  │ Paciente          │ Status      │ Ciência  │
├──────┼───────────┼───────────────────┼─────────────┼──────────┤
│  ◼  │ 11624001 │ PEDRO H. SILVA    │ Sob audit.  │ 🔴 Pend. │
│  🟢  │ 11624002 │ MARIA E. FERREIRA │ Emitida     │ 🟢 Ciente│
│  🔴  │ 11624003 │ JOÃO V. OLIVEIRA  │ Negada      │ 🔴 Pend. │
└──────┴───────────┴───────────────────┴─────────────┴──────────┘
```

### Tela 2 — Dialog Nova Guia ⚠️ dialogs.py VAZIO
```
┌──────────────────────────────────┐
│  ➕ Adicionar Nova Guia          │
├──────────────────────────────────┤
│  Número da Guia:                 │
│  [______________________________]│
│                                  │
│  Nome do Paciente:               │
│  [______________________________]│
│                                  │
│  Status Inicial:                 │
│  [Guia emitida / liberada ▼]    │
│                                  │
│        [Cancelar]  [Adicionar]   │
└──────────────────────────────────┘
```

### Tela 3 — Dialog Histórico / Ciência ⏳ Não implementado
```
┌───────────────────────────────────────────────┐
│  👁️ Histórico — Guia 11624001                │
│  Paciente: PEDRO HENRIQUE DA SILVA            │
├───────────────────────────────────────────────┤
│  05/08/26 11:00 ← Guia sob auditoria         │
│      anterior: Guia emitida / liberada        │
│      por: Sistema                             │
│  ─────────────────────────────────────────   │
│  04/08/26 15:30 ← [Criação]                  │
│      por: henrique.campos                     │
├───────────────────────────────────────────────┤
│  STATUS DE CIÊNCIA: 🔴 Pendente               │
│  Observações: [___________________________]   │
│                                               │
│     [Fechar]     [✓ Marcar como Ciente]      │
└───────────────────────────────────────────────┘
```

### Tela 4 — Configurações ⏳ Não implementado
```
┌──────────────────────────────────────────┐
│  ⚙️ Configurações                        │
├──────────────────────────────────────────┤
│  SINCRONIZAÇÃO                           │
│  Intervalo: [60] minutos                 │
│  URL Solus: [______________________]     │
│  Login:     [______________________]     │
│  Senha:     [••••••••••••••••••••••]     │
│                                          │
│  NOTIFICAÇÕES                            │
│  ☑ Notificar mudança de status          │
│  ☑ Notificar guias negadas              │
│  ☐ Notificar guias aprovadas            │
│                                          │
│  USUÁRIO                                 │
│  Nome:    [henrique.campos]              │
│  Unidade: [Farmácia Oncológica Cacoal]  │
│                                          │
│     [Cancelar]          [Salvar]        │
└──────────────────────────────────────────┘
```

### Tela 5 — Login ⏳ Sprint 1 — Não implementado
```
┌──────────────────────────────────────────┐
│                                          │
│     🏥 Monitor de Guias Solus           │
│         Farmácia Oncológica              │
│                                          │
│  Usuário: [__________________________]   │
│  Senha:   [__________________________]   │
│                                          │
│  ☐ Lembrar usuário                       │
│                                          │
│         [      Entrar      ]             │
│                                          │
│    v1.0.0 — Cacoal (RO)                 │
└──────────────────────────────────────────┘
```

---

## ✅ 5. Checklist Mestre (50 tarefas)

### 🏗️ FASE 1 — Infraestrutura (100% CONCLUÍDA)
- [x] **T01** — Estrutura de pastas (`src/`, `tests/`, etc.)
- [x] **T02** — `requirements.txt` com dependências
- [x] **T03** — `.gitignore` adequado
- [x] **T04** — `pytest.ini` para configuração de testes
- [x] **T05** — Schema SQLite com 4 tabelas
- [x] **T06** — Índices no banco para otimização
- [x] **T07** — Modelo `Guide`
- [x] **T08** — Modelo `GuideHistory`
- [x] **T09** — Modelo `Settings`
- [x] **T10** — `SolusAdapterInterface` (ABC)

### 🔌 FASE 2 — Serviços (100% CONCLUÍDA)
- [x] **T11** — `SimulatedSolusAdapter` com 10 guias fictícias
- [x] **T12** — `GuideRepository` com CRUD e filtros avançados
- [x] **T13** — `MonitorService` com detecção de mudanças
- [x] **T14** — `HistoryService` com auditoria e exportação JSON
- [x] **T15** — `NotificationService` Windows Toast
- [x] **T16** — `SyncScheduler` APScheduler (intervalo configurável)
- [x] **T17** — `Logger` com hash de PII (LGPD)
- [x] **T18** — `constants.py` com status e constantes globais

### 🖥️ FASE 3 — Interface Gráfica (65% CONCLUÍDA)
- [x] **T19** — `MainWindow` (janela principal PySide6)
- [x] **T20** — `DashboardPanel` com 4 cards de indicadores
- [x] **T21** — `GuideTable` com tabela colorida por status
- [x] **T22** — `FiltersPanel` com filtros de status, período e ciência
- [x] **T23** — `stylesheet.py` com estilo visual profissional
- [ ] **T24** ⚠️ — Completar `dialogs.py` — Dialog Nova Guia (arquivo está **vazio**)
- [ ] **T25** ⏳ — Dialog de Histórico / Ciência (Tela 3)
- [ ] **T26** ⏳ — Tela de Configurações (Tela 4)
- [ ] **T27** ⏳ — Tela de Login (Tela 5)
- [ ] **T28** ⏳ — Integrar Login com `settings` do banco
- [ ] **T29** ⏳ — Barra de status (última sync, versão, usuário logado)

### 🧪 FASE 4 — Testes (75% CONCLUÍDA)
- [x] **T30** — 10 testes unitários para `Database`
- [x] **T31** — 11 testes unitários para `GuideRepository`
- [x] **T32** — 5 testes unitários para `Services`
- [x] **T33** — 8 testes unitários para `Models`
- [ ] **T34** ⏳ — Testes de integração (DB + Repository + Service end-to-end)
- [ ] **T35** ⏳ — Testes para `dialogs.py`
- [ ] **T36** ⏳ — Configurar pytest-cov e atingir ≥80% de cobertura
- [ ] **T37** ⏳ — Teste de smoke: inicialização da UI sem erros

### 🔄 FASE 5 — CI/CD e Documentação (80% CONCLUÍDA)
- [x] **T38** — GitHub Actions (`test-monitor-guias.yml`) rodando pytest
- [x] **T39** — `ESPECIFICACAO_COMPLETA.md` (arquitetura, API docs, banco)
- [x] **T40** — `DEPLOYMENT.md` (PyInstaller, produção Windows)
- [x] **T41** — `README.md` (instalação e uso)
- [x] **T42** — Este PRD mestre
- [ ] **T43** ⏳ — Step de build `.exe` no GitHub Actions
- [ ] **T44** ⏳ — `CHANGELOG.md` com histórico de versões

### 🔌 FASE 6 — Adaptador Solus Real (0% — Requer acesso ao sistema)
- [ ] **T45** ⏳ — Implementar `SolusWebAdapter` (scraping via Selenium/Playwright)
- [ ] **T46** ⏳ — Tela de configuração de credenciais Solus
- [ ] **T47** ⏳ — Criptografar credenciais salvas (`cryptography` lib)
- [ ] **T48** ⏳ — Fallback automático para Simulator se Solus falhar

### 📦 FASE 7 — Empacotamento (0% — Pendente)
- [ ] **T49** ⏳ — Gerar executável `.exe` com PyInstaller
- [ ] **T50** ⏳ — Instalador Windows (NSIS ou Inno Setup)

---

## 🧪 6. Plano de Testes

### Testes existentes (34 — passando com Python instalado)
| Arquivo | Qtd | Foco |
|---------|-----|------|
| `test_database.py` | 10 | CRUD SQLite, unicidade, histórico |
| `test_repository.py` | 11 | Filtros, CRUD via Repository |
| `test_services.py` | 5 | MonitorService, HistoryService |
| `test_models.py` | 8 | Validação de modelos |

### Testes a implementar
| ID | Tipo | Descrição |
|----|------|-----------|
| T34 | Integração | DB + Repository + Service end-to-end |
| T35 | Unitário | Dialogs (NovaGuia, Histórico) |
| T36 | Coverage | ≥80% com pytest-cov |
| T37 | Smoke | Inicializar UI sem crash |

### Critério de aceite
- ✅ 0 testes falhando
- ✅ Cobertura ≥ 80%
- ✅ Sem warnings críticos

---

## 📊 7. Estado Atual

| Fase | Descrição | Status | Progresso |
|------|-----------|--------|-----------|
| 1 | Infraestrutura | ✅ Concluída | 100% |
| 2 | Serviços | ✅ Concluída | 100% |
| 3 | Interface Gráfica | ⚠️ Parcial | 65% |
| 4 | Testes | ⚠️ Parcial | 75% |
| 5 | CI/CD e Docs | ⚠️ Parcial | 80% |
| 6 | Adaptador Solus Real | ⏳ Pendente | 0% |
| 7 | Empacotamento | ⏳ Pendente | 0% |

### Próximas tarefas (em ordem de prioridade)
1. **T24** — Implementar `dialogs.py` (Dialog de Nova Guia)
2. **T25** — Dialog de Histórico / Ciência
3. **T27** — Tela de Login
4. **T26** — Tela de Configurações
5. **T34** — Testes de integração
6. **T45** — Adaptador Solus real (quando tiver acesso)
7. **T49** — Build `.exe`

---

## 🔧 8. Instruções para a IA que Assumir o Projeto

### Antes de começar:
1. Leia este PRD completo
2. Leia `ESPECIFICACAO_COMPLETA.md` (API docs e banco detalhado)
3. Inspecione os arquivos em `src/` antes de alterar qualquer coisa
4. Consulte `tests/` para entender o comportamento esperado

### Convenções de código:
- **Linguagem:** Python 3.10+
- **Tipagem:** usar `from typing import ...` em funções públicas
- **Docstrings:** português nas classes e métodos principais
- **Nomenclatura:** `snake_case` para funções, `PascalCase` para classes
- **Commits:** prefixos `feat:`, `fix:`, `docs:`, `test:`, `chore:`

### Como rodar o projeto:
```bash
cd C:\Users\phenrique\.gemini\antigravity\scratch\agentic-awesome-skills\monitor-guias-solus
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python -m pytest tests/ -v
python src/main.py
```

### Repositório remoto:
```
URL:    https://github.com/henrikcampos7-max/agentic-awesome-skills
Branch: main
Pasta:  monitor-guias-solus/
```

---

## 📜 9. Histórico de Versões

| Versão | Data | Descrição |
|--------|------|-----------|
| 1.0.0 | 05/08/2026 | Etapas 1–4 entregues via GitHub Copilot |
| 1.1.0 | 06/08/2026 | CI/CD, DEPLOYMENT.md e este PRD criados via Antigravity |

---

*Este documento pode ser usado por qualquer IA: Gemini, Claude, Copilot, Codex, Cursor ou Windsurf.*
