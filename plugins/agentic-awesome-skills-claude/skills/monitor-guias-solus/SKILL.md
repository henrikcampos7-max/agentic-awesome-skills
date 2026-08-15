---
name: monitor-guias-solus
description: "Guia para desenvolver e manter o Monitor de Guias Solus (app Windows Python/PySide6 de rastreio de guias de oncologia). Use ao implementar features, aplicar o design system Clinical Precision ou alterar UI, banco, serviços ou testes do projeto."
category: development
risk: safe
source: self
source_type: self
date_added: "2026-08-14"
author: henrikcampos7
tags: [pyside6, python, desktop-app, design-system, sqlite, windows]
tools: [opencode, claude, cursor]
---

# Monitor de Guias Solus

## Overview

Aplicativo Windows (Python 3.10–3.12 + PySide6 + SQLite) que monitora guias de
autorização de procedimentos oncológicos enviadas à Unimed. Esta skill padroniza
como agentes de IA devem implementar mudanças no projeto, aplicar o design system
"Clinical Precision" (exportado do Google Stitch) e respeitar as regras de
escopo, testes e Git definidas em `monitor-guias-solus/AGENTS.md`.

## When to Use This Skill

- Use ao implementar novas features, corrigir bugs ou alterar a UI do Monitor de Guias Solus.
- Use ao aplicar ou estender o design system Clinical Precision (paleta teal, badges de status, tabelas).
- Use ao criar ou alterar widgets PySide6, telas, serviços, repositórios, banco ou testes do projeto.
- Use ao registrar mudanças, rodar a suíte de testes ou preparar um PR do projeto.

## How It Works

### Step 1: Entender o projeto

- Projeto vive em `monitor-guias-solus/`; leia `README.md`, `AGENTS.md` do
  projeto e a seção relevante do `PRD_MONITOR_GUIAS_SOLUS.md` antes de editar.
- Arquitetura: UI (`src/ui/`) ↔ serviços ↔ repositórios ↔ adaptadores, com
  banco SQLite. Preserve essa separação.
- Dados de pacientes, nomes e números de guia são dados pessoais: use apenas
  dados sintéticos em testes e nunca registre credenciais ou PII em texto puro.

### Step 2: Aplicar o design system

- Tokens e mapeamento: `monitor-guias-solus/design/README.md` e
  `design/stitch/DESIGN.md` (fonte da verdade). Referência visual: `design/stitch/screen.png` e `code.html`.
- Paleta: primário teal `#006065`, fundo `#F7FAFA`, superfícies brancas com
  borda `#E2E8F0`, texto `#181C1D`; cantos de 4–8px; fonte Inter.
- Cores de status (badges) ficam em `src/utils/constants.py::STATUS_COLORS`:
  verde = autorizada, vermelho = negada/cancelada, âmbar = pendente,
  azul = em análise, laranja = alerta, cinza = fechada, púrpura = OPME, teal = auditoria.
- O QSS global vive em `src/ui/styles/stylesheet.py` (tokens em `COLORS`).
- Nunca hardcode cores fora desses dois arquivos; prefira badges "subtle fill"
  (fundo 10% do semântico, texto 80%) e mantenha contraste AA.

### Step 3: Implementar

- Mudanças pequenas, compatíveis com Python 3.10–3.12; tipagem em APIs
  públicas, `snake_case`, classes `PascalCase`, docstrings em português.
- Não sobrescreva alterações locais pendentes (`git status`) nem refatore fora
  do escopo da tarefa.

### Step 4: Validar

- Rode primeiro os testes relacionados à mudança; antes do PR rode a suíte
  completa: `python -m pytest tests/ -v --tb=short`.
- Registre mudanças relevantes em `CHANGELOG.md` (seção "Não publicado").

### Step 5: Git e PR

- Use branch de tópico e commits `feat:`, `fix:`, `docs:`, `test:` ou `chore:`;
  nunca envie direto para `main`. PRs usam o template padrão do repo.
- Não versione `.env`, `*.db`, `*.bak`, logs, `.venv/` ou o `.pytest_cache`.
- Ao alterar esta SKILL.md ou outra do repo, valide com
  `npm run validate && npm run security:docs` antes do PR.

## Examples

### Example 1: Adicionar um novo status

```python
# src/utils/constants.py
STATUS_COLORS = {
    "Novo status": "#006065",  # teal primário — contraste AA sobre branco
    # ...demais status
}
```

Use a cor semântica adequada (verde/vermelho/âmbar/azul/laranja/cinza) e teste
o badge no diálogo de histórico (`src/ui/widgets/dialogs.py`).

### Example 2: Mudar um token do design system

1. Atualize `design/stitch/DESIGN.md` (fonte da verdade).
2. Propague para `src/ui/styles/stylesheet.py::COLORS` e `STATUS_COLORS`.
3. Rode a suíte e registre em `CHANGELOG.md`.

## Limitations

- O sistema Solus é simulado por padrão; não implemente automação real sem
  acesso autorizado e requisitos confirmados.
- Não contorne CAPTCHA, MFA, bloqueios ou políticas do Solus.
- Esta skill cobre apenas o projeto `monitor-guias-solus/`; alterações fora do
  projeto exigem autorização explícita do usuário.
