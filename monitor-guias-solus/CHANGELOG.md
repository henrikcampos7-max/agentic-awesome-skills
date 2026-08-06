# CHANGELOG — Monitor de Guias Solus

Todas as mudanças notáveis deste projeto são documentadas aqui.
Formato baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/).

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
