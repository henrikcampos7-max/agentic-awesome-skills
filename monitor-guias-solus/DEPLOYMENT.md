# Monitor de Guias Solus - Guia de Deployment e Produção

Este documento especifica o procedimento completo para gerar o executável standalone (`.exe`) do **Monitor de Guias Solus** e implantá-lo em ambientes de produção Windows.

---

## 📋 Pré-requisitos de Build

- **Sistema Operacional**: Windows 10 ou Windows 11 (64-bit)
- **Python**: 3.10 ou superior
- **PyInstaller**: `pip install pyinstaller`

---

## 🛠️ Passo a Passo para Gerar o Executável (.exe)

### 1. Preparar o Ambiente

```powershell
cd monitor-guias-solus
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
pip install pyinstaller
```

### 2. Gerar o Executável Standalone

Execute o comando PyInstaller com a janela oculta (`--noconsole`) e ícone personalizado:

```powershell
pyinstaller --noconsole `
            --onefile `
            --name "MonitorGuiasSolus" `
            --add-data "src;src" `
            src/main.py
```

O arquivo executável `MonitorGuiasSolus.exe` será gerado na pasta `dist/`.

---

## 🚀 Implantação e Configuração em Produção

### 1. Estrutura de Arquivos em Produção

```
C:\Program Files\MonitorGuiasSolus\
├── MonitorGuiasSolus.exe
├── data\
│   └── guias.db          (Gerado automaticamente na primeira execução)
└── logs\
    └── audit.log         (Logs de auditoria e conformidade LGPD)
```

### 2. Inicialização Automática com o Windows

Para iniciar a aplicação juntamente com o Windows, adicione o atalho na pasta de inicialização do usuário:

1. Pressione `Win + R` e digite `shell:startup`.
2. Crie um atalho apontando para `MonitorGuiasSolus.exe`.

---

## 🛡️ Segurança e Backup da Base de Dados

1. **Localização do Banco**: O arquivo `guias.db` utiliza SQLite em modo WAL (Write-Ahead Logging) para garantir alta integridade.
2. **Rotina de Backup Recomendada**:
   - Agendar um script diário em PowerShell no Agendador de Tarefas do Windows para copiar `guias.db` para um servidor de backup seguro.

---

## 🔍 Solução de Problemas (Troubleshooting)

- **Erro de Notificação do Windows**: Certifique-se de que a central de notificações do Windows 10/11 esteja habilitada para a aplicação.
- **Permissão de Leitura/Escrita**: Certifique-se de que a pasta de execução possui permissões de escrita para salvar o banco SQLite e logs de auditoria LGPD.
