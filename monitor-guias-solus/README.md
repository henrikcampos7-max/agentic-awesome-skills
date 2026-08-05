# Monitor de Guias Solus

Aplicativo desktop Windows para monitorar guias de pacientes no sistema Solus.

## Características

- ✅ Desktop app Windows (PySide6)
- ✅ Banco SQLite local
- ✅ Painel com indicadores em tempo real
- ✅ Cadastro de guias (número + paciente)
- ✅ Filtros avançados
- ✅ Agendador de consultas (60 min)
- ✅ Notificações Windows
- ✅ Histórico e auditoria
- ✅ Compatível com LGPD

## Stack

- Python 3.12
- PySide6 (GUI)
- SQLite (Banco de dados)
- APScheduler (Agendador)

## Estrutura do Projeto

```
monitor-guias-solus/
├── src/
│   ├── main.py                 # Entry point
│   ├── database/
│   │   ├── __init__.py
│   │   ├── schema.py           # Schema SQLite
│   │   └── migrations.py       # Migrations
│   ├── models/
│   │   ├── __init__.py
│   │   ├── guide.py            # Model Guide
│   │   ├── history.py          # Model History
│   │   └── settings.py         # Model Settings
│   ├── ui/
│   │   ├── __init__.py
│   │   ├── main_window.py      # Janela principal
│   │   ├── widgets/
│   │   │   ├── dashboard.py    # Painel indicadores
│   │   │   ├── table.py        # Tabela guias
│   │   │   ├── filters.py      # Filtros
│   │   │   └── dialogs.py      # Diálogos
│   │   └── styles/
│   │       └── stylesheet.qss
│   ├── adapters/
│   │   ├── __init__.py
│   │   ├── solus_adapter.py    # Interface Solus
│   │   └── simulator.py        # Modo simulado
│   ├── services/
│   │   ├── __init__.py
│   │   ├── scheduler.py        # Agendador
│   │   ├── notifier.py         # Notificações Windows
│   │   ├── repository.py       # Repositório dados
│   │   └── monitor.py          # Lógica monitoramento
│   └── utils/
│       ├── __init__.py
│       ├── logger.py           # Logging LGPD
│       └── constants.py        # Constantes
├── tests/
│   ├── __init__.py
│   ├── test_database.py
│   ├── test_models.py
│   ├── test_services.py
│   └── test_ui.py
├── requirements.txt
├── setup.py
├── .gitignore
├── ESPECIFICACAO_COMPLETA.md
└── exemplo_painel_monitor_guias.png
```

## Instalação

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python src/main.py
```

## Roadmap de Implementação

- [x] Etapa 1: Estrutura + Banco SQLite
- [ ] Etapa 2: UI com dados simulados
- [ ] Etapa 3: Repositórios, histórico, filtros
- [ ] Etapa 4: Agendador + Notificações
- [ ] Etapa 5: Testes unitários
- [ ] Etapa 6: Adaptador Solus (integração real)

## Conformidade

- 🔒 Sem armazenamento de credenciais
- 📋 Auditoria completa (LGPD)
- 🚫 Sem contorno de CAPTCHA/MFA/bloqueios
- ✅ Comparação de status (antes/depois)
- 💾 Fallback para último status válido em erro
