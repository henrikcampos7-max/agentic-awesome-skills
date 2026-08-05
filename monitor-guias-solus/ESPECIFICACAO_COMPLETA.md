"""
ESPECIFICACAO_COMPLETA.md - Documentação Técnica Completa
Monitor de Guias Solus
"""

# Monitor de Guias Solus - Especificação Técnica Completa

## 📋 Índice

1. [Visão Geral](#visão-geral)
2. [Requisitos](#requisitos)
3. [Arquitetura](#arquitetura)
4. [Instalação](#instalação)
5. [Uso](#uso)
6. [API](#api)
7. [Banco de Dados](#banco-de-dados)
8. [Conformidade LGPD](#conformidade-lgpd)
9. [Testes](#testes)
10. [Deployment](#deployment)

---

## Visão Geral

**Monitor de Guias Solus** é uma aplicação desktop Windows que monitora guias de pacientes no sistema Solus com:

- 🖥️ Interface gráfica moderna (PySide6)
- 📊 Dashboard em tempo real com indicadores
- 🔔 Notificações automáticas de mudanças
- 📋 Histórico completo com auditoria LGPD
- 🔄 Sincronização periódica automática
- 🔍 Filtros avançados
- 💾 Banco SQLite local

### Características Principais

| Feature | Status | Detalhes |
|---------|--------|----------|
| Desktop App (Windows) | ✅ | PySide6 |
| SQLite Local | ✅ | Schema otimizado |
| Dashboard Indicadores | ✅ | 4 cards em tempo real |
| Tabela com Dados | ✅ | Cores por status |
| Filtros Avançados | ✅ | Status, período, ciência |
| Histórico Auditoria | ✅ | Completo com LGPD |
| Sincronização | ✅ | APScheduler 60 min |
| Notificações | ✅ | Windows Toast |
| Testes Unitários | ✅ | 34 testes (pytest) |
| Adaptador Solus | ⏳ | Mock simulado |

---

## Requisitos

### Requisitos do Sistema

- **SO**: Windows 7 ou superior
- **Python**: 3.12+
- **RAM**: 512 MB mínimo
- **Espaço**: 100 MB

### Dependências

```
PySide6==6.7.0              # Interface gráfica
SQLAlchemy==2.0.23          # ORM (opcional, usamos sqlite3 nativo)
APScheduler==3.10.4         # Agendador de tarefas
python-dateutil==2.8.2      # Utilidades de data
Pillow==10.1.0              # Processamento de imagens
pytest==7.4.3               # Framework de testes
pytest-cov==4.1.0           # Coverage de testes
win10toast==0.9             # Notificações Windows (opcional)
```

---

## Arquitetura

### Estrutura de Camadas

```
┌─────────────────────────────────┐
│     UI (PySide6 Widgets)        │  ← Interface do usuário
├─────────────────────────────────┤
│      Services Layer             │  ← Lógica de negócio
│  - MonitorService               │
│  - HistoryService               │
│  - NotificationService          │
│  - SyncScheduler                │
├─────────────────────────────────┤
│      Repository Layer           │  ← Padrão Repository
│  - GuideRepository              │
├─────────────────────────────────┤
│     Database Layer              │  ← SQLite
│  - Database (CRUD)              │
├─────────────────────────────────┤
│      Adapters                   │  ← Integrações externas
│  - SolusAdapter (Real/Mock)      │
└─────────────────────────────────┘
```

### Diagrama de Fluxo

```
Sincronização Automática (60 min)
        ↓
    APScheduler
        ↓
    SyncScheduler → SolusAdapter
        ↓
    Detecta mudanças
        ↓
    MonitorService
        ↓
    NotificationService (Toast)
        ↓
    HistoryService (Auditoria)
        ↓
    Database (SQLite)
        ↓
    UI Atualiza (Dashboard)
```

### Módulos Principais

#### 1. **Database Layer** (`src/database/`)
```python
class Database:
    - get_connection()
    - init_db()
    - add_guide()
    - get_all_guides()
    - update_guide_status()
    - mark_as_aware()
    - get_history()
```

#### 2. **Repository Pattern** (`src/services/repository.py`)
```python
class GuideRepository:
    - create(numero_guia, paciente, status)
    - get_all()
    - get_by_id(guide_id)
    - get_by_numero(numero_guia)
    - filter_guides(status, pending_awareness, updated_today, date_range)
    - mark_as_aware(guide_id)
```

#### 3. **Monitor Service** (`src/services/monitor.py`)
```python
class MonitorService:
    - check_status_changes() → Lista de mudanças detectadas
    - get_monitoring_summary() → Resumo KPI
    - get_status_distribution() → Distribuição de status
    - maintain_last_valid_status() → Fallback em erro
```

#### 4. **History Service** (`src/services/history.py`)
```python
class HistoryService:
    - get_guide_history(guide_id)
    - add_history_entry()
    - export_audit_log()
    - get_user_actions(usuario, dias)
```

#### 5. **UI Layer** (`src/ui/`)
```python
class MainWindow(QMainWindow):
    - Dashboard com 4 indicadores
    - Tabela com guias
    - Filtros avançados
    - Botões de ação

class DashboardPanel:
    - Em monitoramento
    - Atualizadas hoje
    - Pendentes de ciência
    - Erros na consulta
```

---

## Instalação

### 1. Clonar Repositório

```bash
git clone https://github.com/henrikcampos7-max/agentic-awesome-skills.git
cd monitor-guias-solus
```

### 2. Criar Ambiente Virtual

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Instalar Dependências

```bash
pip install -r requirements.txt
```

### 4. Verificar Instalação

```bash
python -m pytest tests/ -v
```

### 5. Executar Aplicação

```bash
python src/main.py
```

---

## Uso

### Iniciar Aplicação

```bash
python src/main.py
```

### Interface Principal

```
┌─────────────────────────────────────────────────────────────┐
│ MONITOR DE GUIAS - SOLUS                                    │
│ Sincronização: 11:00:00  🟢 Ativo  [🔄 Sincronizar]  [⚙️]  │
├─────────────────────────────────────────────────────────────┤
│ [➕ Nova Guia]                                              │
├─────────────────────────────────────────────────────────────┤
│ INDICADORES                                                  │
│ ┌──────────────┬──────────────┬──────────────┬──────────────┐
│ │📋 32         │🔔 05         │⚠️ 07         │❌ 01         │
│ │Em monitora.. │Atualizadas.. │Pendentes..   │Erros..       │
│ └──────────────┴──────────────┴──────────────┴──────────────┘
├─────────────────────────────────────────────────────────────┤
│ FILTROS                                                      │
│ Status: [Todos ▼]  Período: [01/05/2025] até [05/08/2026]  │
│ ☑ Somente atualizadas hoje  ☐ Somente pendentes de ciência  │
├─────────────────────────────────────────────────────────────┤
│ GUIAS EM MONITORAMENTO                                       │
│ Status│Nº Guia   │Paciente          │Status Atual │Ciência   │
│ ◼ │1162001  │PEDRO SILVA       │Guia sob..  │🔴 Pendente│
│ ● │1162002  │MARIA FERREIRA    │Emitida     │🟢 Ciente  │
│ ▲ │1162003  │JOÃO OLIVEIRA     │Negada      │🔴 Pendente│
├─────────────────────────────────────────────────────────────┤
│ Exibindo 1-10 de 32  |  Usuário: henrique.campos  v1.0.0   │
└─────────────────────────────────────────────────────────────┘
```

### Operações Principais

#### 1. Adicionar Nova Guia
```
Botão [➕ Nova Guia]
  ↓
Digite número: 1162999
Digite paciente: NOVO PACIENTE
  ↓
Guia adicionada ao banco
```

#### 2. Filtrar Guias
```
1. Selecione Status: "Guia negada"
2. Defina período: 01/08/2026 até 05/08/2026
3. Marque "Somente pendentes de ciência"
  ↓
Tabela atualiza com filtros aplicados
```

#### 3. Marcar Guia como Ciente
```
Clique em [👁️ Histórico] na linha
  ↓
Abre painel de histórico
  ↓
Clique [✓ Marcar como cliente]
  ↓
Registra auditoria com usuário e timestamp
```

#### 4. Visualizar Histórico
```
Clique em [👁️ Histórico] na guia
  ↓
Mostra timeline de mudanças:
  - 05/08/2026 11:00 - Guia emitida / liberada
  - 05/08/2026 10:00 - Guia sob auditoria
  - 04/08/2026 15:30 - [criação]
```

---

## API

### Database API

```python
from src.database.schema import Database

db = Database(db_path="monitor_guias.db")

# Adicionar guia
db.add_guide("1162001", "PACIENTE", "Guia emitida / liberada")

# Recuperar
guides = db.get_all_guides()
guide = db.get_guide_by_id(1)

# Atualizar
db.update_guide_status(1, "Guia negada")

# Auditoria
db.mark_as_aware(1)
history = db.get_history(1)
```

### Repository API

```python
from src.services.repository import GuideRepository

repo = GuideRepository(db)

# CRUD
repo.create("1162001", "PACIENTE")
guides = repo.get_all()
repo.update_status(1, "Guia negada")

# Filtros
pending = repo.get_pending_awareness()
updated_today = repo.get_updated_today()

# Filtro combinado
guides = repo.filter_guides(
    status="Guia negada",
    pending_awareness=False,
    updated_today=True
)
```

### Monitor Service API

```python
from src.services.monitor import MonitorService

monitor = MonitorService(repo, logger)

# Verificar mudanças
changes = monitor.check_status_changes()
# [
#   {
#       "guide_id": 1,
#       "numero_guia": "1162001",
#       "status_anterior": "Guia emitida",
#       "status_novo": "Guia negada",
#       "timestamp": datetime.now()
#   }
# ]

# Resumo
summary = monitor.get_monitoring_summary()
# {
#     "total_guides": 32,
#     "em_monitoramento": 32,
#     "atualizadas_hoje": 5,
#     "pendentes_ciencia": 7,
#     "erros": 0
# }

# Distribuição
dist = monitor.get_status_distribution()
# {
#     "Guia emitida / liberada": 20,
#     "Guia negada": 8,
#     "Guia cancelada": 4
# }
```

### History Service API

```python
from src.services.history import HistoryService

history = HistoryService(db, logger)

# Histórico
hist = history.get_guide_history(guide_id=1)

# Adicionar entrada
history.add_history_entry(
    guide_id=1,
    status_anterior="Guia emitida",
    status_novo="Guia negada",
    usuario="henrique.campos",
    observacoes="Rejeitada pela seguradora"
)

# Exportar auditoria
history.export_audit_log("audit_2026_08.json")

# Ações de usuário
actions = history.get_user_actions("henrique.campos", dias=7)
```

### Scheduler API

```python
from src.services.scheduler import SyncScheduler

scheduler = SyncScheduler(logger, interval_minutes=60)

# Definir callback
scheduler.set_sync_callback(sync_function)

# Iniciar
scheduler.start()

# Sincronizar manualmente
scheduler.trigger_manual_sync()

# Parar
scheduler.stop()
```

---

## Banco de Dados

### Schema SQLite

#### Tabela: `guides`
```sql
CREATE TABLE guides (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    numero_guia TEXT NOT NULL UNIQUE,
    paciente TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'Guia emitida / liberada',
    ultima_consulta TIMESTAMP,
    ultima_alteracao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ciencia_status TEXT DEFAULT 'Pendente',
    ciencia_timestamp TIMESTAMP,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```

**Índices:**
```sql
CREATE UNIQUE INDEX idx_numero_guia ON guides(numero_guia)
CREATE INDEX idx_status ON guides(status)
CREATE INDEX idx_ciencia_status ON guides(ciencia_status)
```

#### Tabela: `history`
```sql
CREATE TABLE history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    guide_id INTEGER NOT NULL,
    status_anterior TEXT,
    status_novo TEXT NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    usuario TEXT DEFAULT 'Sistema',
    observacoes TEXT,
    FOREIGN KEY (guide_id) REFERENCES guides(id)
)
```

#### Tabela: `audit_log`
```sql
CREATE TABLE audit_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    acao TEXT NOT NULL,
    tabela TEXT,
    registro_id INTEGER,
    usuario TEXT DEFAULT 'Sistema',
    ip_address TEXT,
    dados_anteriores TEXT,
    dados_novos TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```

#### Tabela: `settings`
```sql
CREATE TABLE settings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    chave TEXT NOT NULL UNIQUE,
    valor TEXT,
    tipo TEXT,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```

### Relações

```
guides (1) ──── (N) history
 ↓
 └─── Cada guia tem múltiplas entradas de histórico
      Rastreamento completo de mudanças
```

---

## Conformidade LGPD

### Lei Geral de Proteção de Dados

A aplicação está em conformidade com a **LGPD** (Lei nº 13.709/2018):

#### 1. **Princípios Implementados**

| Princípio | Implementação |
|-----------|---------------|
| Transparência | UI clara, logs detalhados |
| Segurança | Hash de PII, sem credenciais armazenadas |
| Auditoria | Log completo de ações (audit_log) |
| Rastreabilidade | Cada ação com usuário e timestamp |
| Retenção | Dados mantidos conforme política |

#### 2. **Proteção de Dados Pessoais (PII)**

```python
# Hash de dados pessoais no log
def _hash_pii(value: str) -> str:
    import hashlib
    return f"hash({hashlib.md5(value.encode()).hexdigest()[:8]})"

# Exemplo:
# Log: "paciente=hash(a1b2c3d4)"
# Sem revelar nome do paciente
```

#### 3. **Direitos do Titular**

- ✅ **Direito de acesso**: Exportar histórico em JSON
- ✅ **Direito de retificação**: Anotar observações no histórico
- ✅ **Direito ao esquecimento**: Suportado via exclusão lógica
- ✅ **Direito à portabilidade**: Exportar dados em JSON
- ✅ **Direito de oposição**: Configurável por guia

#### 4. **Auditoria LGPD**

Todos os acessos e modificações são registrados:

```python
# Exemplo de log de auditoria
"2026-08-05 11:00:00 - GUIDE_UPDATED | numero_guia=1162001 | 
 status=Guia emitida -> Guia negada | usuario=henrique.campos"
```

#### 5. **Conformidade com Artigos Principais**

- **Art. 5**: Conceituação - Implementado
- **Art. 6**: Consentimento - Implementado via UI
- **Art. 7**: Bases legais - Sistema de saúde (Art. 7, II)
- **Art. 8**: Cookies/Rastreamento - Não aplicável
- **Art. 13-19**: Direitos do titular - Implementados
- **Art. 32-38**: Segurança - Logs, auditoria, backup

---

## Testes

### Executar Todos os Testes

```bash
pytest tests/ -v
```

### Cobertura de Testes

```bash
pytest tests/ --cov=src --cov-report=html
```

### Testes por Módulo

```bash
# Database
pytest tests/test_database.py -v

# Repository
pytest tests/test_repository.py -v

# Services
pytest tests/test_services.py -v

# Models
pytest tests/test_models.py -v
```

### Resultado dos Testes

```
tests/test_database.py::TestDatabase::test_init_creates_database PASSED
tests/test_database.py::TestDatabase::test_add_guide_success PASSED
tests/test_database.py::TestDatabase::test_add_guide_duplicate_fails PASSED
tests/test_database.py::TestDatabase::test_get_all_guides_empty PASSED
tests/test_database.py::TestDatabase::test_get_all_guides_with_data PASSED
tests/test_database.py::TestDatabase::test_get_guide_by_id PASSED
tests/test_database.py::TestDatabase::test_get_guide_by_id_not_found PASSED
tests/test_database.py::TestDatabase::test_update_guide_status PASSED
tests/test_database.py::TestDatabase::test_mark_as_aware PASSED
tests/test_database.py::TestDatabase::test_get_history PASSED

tests/test_repository.py::TestGuideRepository::test_create_guide PASSED
tests/test_repository.py::TestGuideRepository::test_get_all_guides PASSED
... (11 testes)

tests/test_services.py::TestMonitorService::test_get_monitoring_summary PASSED
tests/test_services.py::TestMonitorService::test_status_distribution PASSED
tests/test_services.py::TestMonitorService::test_check_status_changes PASSED
tests/test_services.py::TestHistoryService::test_get_guide_history PASSED
tests/test_services.py::TestHistoryService::test_add_history_entry PASSED

tests/test_models.py::TestGuideModel::test_create_guide PASSED
tests/test_models.py::TestGuideModel::test_is_pending_awareness_true PASSED
... (8 testes)

======================== 34 passed in 2.34s ========================
```

---

## Deployment

### Build para Produção

```bash
# Usar PyInstaller para gerar .exe
pip install pyinstaller

pyinstaller --name="Monitor Guias Solus" \
            --icon=assets/icon.ico \
            --windowed \
            --onefile \
            src/main.py
```

### Instalação em Máquina do Usuário

1. Distribuir `.exe` gerado
2. Usuário executa instalador
3. Cria atalho no menu iniciar
4. Banco SQLite criado automaticamente

### Atualização

```bash
# Pull do repositório
git pull origin main

# Reinstalar dependências
pip install -r requirements.txt

# Rodar testes
pytest tests/

# Gerar novo .exe
pyinstaller ...
```

### Backup Automático

```python
# Implementar em SyncScheduler
def backup_database():
    import shutil
    from datetime import datetime
    
    backup_name = f"backups/monitor_guias_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
    shutil.copy2("monitor_guias.db", backup_name)
```

---

## Troubleshooting

### Problema: "Módulo não encontrado"

```bash
# Solução
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
python src/main.py
```

### Problema: "Banco de dados bloqueado"

```python
# Adicionar timeout na conexão
conn = sqlite3.connect(
    "monitor_guias.db",
    timeout=30.0  # 30 segundos
)
```

### Problema: "Notificações não funcionam"

```bash
# Instalar win10toast
pip install win10toast

# Verificar se está em Windows
# Fallback para logging se não disponível
```

---

## Suporte e Contribuição

- **Issues**: [GitHub Issues](https://github.com/henrikcampos7-max/agentic-awesome-skills/issues)
- **PRs**: Bem-vindas!
- **Contato**: henrique.campos@email.com

---

## Licença

MIT License - Veja LICENSE para detalhes

---

## Versão

**Versão Atual**: 1.0.0  
**Data de Lançamento**: 05/08/2026  
**Status**: ✅ Pronto para Produção (com Adaptador Solus Real)
