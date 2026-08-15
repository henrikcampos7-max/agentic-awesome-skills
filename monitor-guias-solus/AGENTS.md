# Monitor de Guias Solus

## Escopo

- Trabalhe somente em `monitor-guias-solus/`, salvo pedido explícito.
- Leia apenas os arquivos ligados à tarefa; localize primeiro símbolos com `rg`.
- Preserve a arquitetura Python/PySide6, SQLite, serviços, adaptadores e repositórios.
- Não sobrescreva alterações locais nem refatore código fora do escopo.

## Segurança e dados

- Trate nomes, números de guia e dados de pacientes como dados pessoais.
- Use dados sintéticos em testes e nunca registre credenciais ou PII em texto puro.
- Não contorne CAPTCHA, MFA, bloqueios ou políticas do Solus.
- Mantenha o simulador como padrão até haver acesso autorizado ao sistema real.
- Não versione `.env`, bancos `*.db`, backups `*.bak`, logs ou `.venv/`.

## Fluxo

- Antes de editar, consulte `README.md`, a seção pertinente do PRD e os testes relacionados.
- Faça mudanças pequenas e mantenha compatibilidade com Python 3.10–3.12.
- Use tipagem em APIs públicas, nomes `snake_case`, classes `PascalCase` e docstrings em português.
- Execute primeiro os testes diretamente relacionados; antes do PR, execute `python -m pytest tests/ -v --tb=short`.
- Registre mudanças relevantes em `CHANGELOG.md`.
- Use branch de tópico e commits `feat:`, `fix:`, `docs:`, `test:` ou `chore:`; nunca envie direto para `main`.

## Resposta

- Seja conciso e informe somente: alteração, arquivos, testes e pendências.
