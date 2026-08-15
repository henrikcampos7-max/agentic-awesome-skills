# Design System — Monitor de Guias Solus

Fonte: export do **Google Stitch** em [`stitch/`](stitch/) (design "Clinical Precision",
gerado a partir da tela do app e do manual de marca da Unimed).

## Tokens e onde vivem no código

| Token (Stitch) | Valor | Uso no app |
|---|---|---|
| `primary` | `#006065` | Botões, foco de inputs, tab selecionada, badge "Sob auditoria" |
| `primary-hover` / `primary-pressed` | `#00767C` / `#004F53` | Estados de botão |
| `background` / `surface` | `#F7FAFA` / `#FFFFFF` | Fundo da janela / cartões e tabelas |
| `outline-variant` | `#E2E8F0` | Bordas de inputs, tabelas, grupos, separadores |
| `on-surface` / `on-surface-variant` | `#181C1D` / `#3E4949` | Texto principal / secundário e cabeçalhos |
| `error` | `#BA1A1A` | Mensagens de erro e badges de status negado |
| `zebra` | `#F1F4F4` | Linhas alternadas de tabela |

Status semânticos (badges): verde = autorizada, vermelho = negada/cancelada,
âmbar = pendente, azul = em análise, laranja = alerta/expirada, cinza = fechada,
púrpura = OPME, teal = auditoria. Definidos em
`src/utils/constants.py::STATUS_COLORS`.

## Implementação

- `src/ui/styles/stylesheet.py` — tokens e QSS global do app.
- `src/utils/constants.py::STATUS_COLORS` — cores dos badges de status
  (usadas por `src/ui/widgets/dialogs.py`).
- Tipografia: Inter (fallback Segoe UI/Arial) aplicada no QSS global.

## Diretrizes ao alterar

- Nunca use cores hardcoded fora de `stylesheet.py` e `STATUS_COLORS`.
- Prefira chips "subtle fill" (fundo 10% do semântico, texto 80%) para status.
- Mantenha contraste AA: texto escuro `#181C1D` sobre fundos claros.
- Ao atualizar o design, regenere no Stitch e substitua `stitch/` mantendo
  `DESIGN.md` como fonte da verdade dos tokens.
