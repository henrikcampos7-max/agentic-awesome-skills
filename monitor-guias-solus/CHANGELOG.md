# CHANGELOG — Monitor de Guias Solus

Todas as mudanças notáveis deste projeto são documentadas aqui.
Formato baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/).

---

## [Não publicado]

### Adicionado
- Agente personalizado do GitHub Copilot para finalizar e manter o Monitor de Guias Solus.
- `AGENTS.md` local com regras de escopo, testes, Git e proteção de dados para agentes de desenvolvimento.
- Design system **"Clinical Precision"** exportado do Google Stitch em `design/stitch/` (`code.html`, `DESIGN.md`, `screen.png`) com mapeamento de tokens em `design/README.md`.
- Skill `skills/monitor-guias-solus` para agentes de IA implementarem mudanças aplicando o design system.
- Agente `monitor-guias-design-system` (`.github/agents/`) para implementações de design system.
- Agente opencode do projeto em `.opencode/agent/monitor-guias-solus.md` (design system + regras do `AGENTS.md`).

### Alterado
- Credenciais locais padrão: login `henrique.campos` -> `phenrique` e senha `solus@2026` -> `123456` (placeholders atualizados em `login.py`, `main_window.py` e `configuracoes.py`).
- `src/ui/styles/stylesheet.py`: QSS reescrito com os tokens do design system Clinical Precision (teal `#006065`, fundo `#F7FAFA`, bordas `#E2E8F0`, fonte Inter, zebra nas tabelas, chips e cantos 4–8px).
- `src/utils/constants.py`: `STATUS_COLORS` atualizadas para a paleta semântica do design system (verde/vermelho/âmbar/azul/laranja/cinza/púrpura/teal) com contraste AA.

### Corrigido
- Vazamento de conexões SQLite no Windows (`with conn:` não fecha conexões; agora usa `contextlib.closing` em `schema.py`), que travava os bancos de teste e acumulava dados entre execuções.
- Ordenação de guias e histórico com timestamps de precisão de segundos (`CURRENT_TIMESTAMP`) que empatavam no mesmo segundo; `ultima_alteracao` e histórico agora usam timestamps com microssegundos.

---

## [1.1.0] — 06/08/2026

### Adicionado
- **T24** — `NovaGuiaDialog`: formulário completo para adicionar guias, com validação inline de campos obrigatórios e conversão automática de nome para maiúsculas
- **T25** — `HistoricoDialog`: visualização da timeline de alterações de status, badge colorido de status, indicador de ciência, campo de observações e confirmação com popup de auditoria LGPD
- **T26** — `ConfiguracoesDialog`: tela de configurações completa com persistência via tabela `settings` (sync, credenciais Solus, notificações, dados do usuário)
- **T27** — `LoginDialog`: tela de login com autenticação local, opção de "lembrar usuário" e persistência via banco SQLite
- **T28** — Integração Login ↔ MainWindow: `main.py` exibe `LoginDialog` antes de abrir a janela principal; usuário autenticado é propagado para toda a sessão
- **T29** — Barra de status dinâmica na janela principal: exibe contador de registros, usuário logado e versão em tempo real
- **T38** — GitHub Actions CI/CD: workflow `test-monitor-guias.yml` que executa pytest automaticamente em Python 3.10, 3.11 e 3.12
- **T39** — `ESPECIFICACAO_COMPLETA.md`: documentação técnica completa com arquitetura, API docs e schema do banco
- **T40** — `DEPLOYMENT.md`: guia de build com PyInstaller e deploy em produção Windows
- **T42** — `PRD_MONITOR_GUIAS_SOLUS.md`: documento mestre de requisitos do produto com checklist de 50 tarefas

### Alterado
- `main_window.py`: botão "Nova Guia" agora usa `NovaGuiaDialog` em vez de `QInputDialog` genérico
- `main_window.py`: botão ⚙️ agora abre `ConfiguracoesDialog`
- `main_window.py`: barra de status atualiza o contador de registros a cada refresh
- `main.py`: refatorado para incluir fluxo de login antes de abrir a janela principal

---

## [1.0.0] — 05/08/2026

### Adicionado (via GitHub Copilot)
- **T01–T10** — Estrutura base do projeto: pastas, requirements, .gitignore, pytest.ini, schema SQLite com 4 tabelas e índices, modelos Guide/GuideHistory/Settings, interface ABC SolusAdapterInterface
- **T11** — `SimulatedSolusAdapter`: mock com 10 guias fictícias para testes
- **T12** — `GuideRepository`: CRUD completo e filtros avançados (status, período, ciência)
- **T13** — `MonitorService`: detecção de mudanças de status com fallback para último status válido
- **T14** — `HistoryService`: histórico completo com exportação JSON e conformidade LGPD
- **T15** — `NotificationService`: notificações Windows Toast via `win10toast`
- **T16** — `SyncScheduler`: agendador APScheduler com callback configurável
- **T17** — `Logger` com hash de PII para conformidade com LGPD (Lei 13.709/2018)
- **T18** — `constants.py`: lista de 10 status possíveis e mapa de cores por status
- **T19–T23** — Interface gráfica PySide6: `MainWindow`, `DashboardPanel` (4 cards), `GuidesTable` (tabela colorida), `FiltersPanel` (filtros de status/período/ciência), `stylesheet.py` profissional
- **T30–T33** — 34 testes unitários: 10 para Database, 11 para Repository, 5 para Services, 8 para Models

---

## [Planejado]

- **T34** — Testes de integração end-to-end (DB + Repository + Service)
- **T35** — Testes unitários para dialogs
- **T36** — Cobertura ≥ 80% com pytest-cov
- **T37** — Smoke test de inicialização da UI
- **T43** — Step de build `.exe` no GitHub Actions
- **T45** — `SolusWebAdapter`: adaptador real via Selenium/Playwright
- **T46–T48** — Tela de credenciais Solus, criptografia local, fallback automático
- **T49** — Build executável `.exe` com PyInstaller
- **T50** — Instalador Windows (NSIS ou Inno Setup)
