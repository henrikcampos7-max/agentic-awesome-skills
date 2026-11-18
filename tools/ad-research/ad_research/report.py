"""Render the evidence used to compare ads and video sales letters."""

from collections import Counter, defaultdict
from datetime import date
from html import escape
from urllib.parse import quote, urlsplit


def _text(value):
    if value is None or value == "":
        return "—"
    value = escape(" ".join(str(value).split()), quote=False)
    for token in ("\\", "|", "[", "]", "*", "_", "`", "~"):
        value = value.replace(token, "\\" + token)
    return value


def _link(label, url):
    label = _text(label)
    if url and not any(ord(char) < 33 for char in url):
        try:
            parsed = urlsplit(url)
            if parsed.scheme in {"https", "http"} and parsed.hostname and not parsed.username:
                encoded = quote(url, safe=":/?&=%#;@+!,$[]")
                return f"[{label}](<{encoded}>)"
        except ValueError:
            pass
    return label


def _table(headers, rows):
    return [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
        *("| " + " | ".join(row) + " |" for row in rows),
        "",
    ]


def _label(row):
    return _link(row.get("title") or row["id"], row.get("url"))


def _days(row):
    if not row.get("first_seen") or not row.get("last_seen"):
        return None
    try:
        days = (date.fromisoformat(row["last_seen"]) - date.fromisoformat(row["first_seen"])).days
    except ValueError:
        return None
    return days + 1 if days >= 0 else None


def _sort_public(row):
    days = _days(row)
    variants = row.get("distinct_variants")
    return -(days if days is not None else -1), -(variants if variants is not None else -1), row["id"]


def _metric(value, places=2):
    return "—" if value is None else f"{value:,.{places}f}"


def _divide(numerator, denominator):
    return numerator / denominator if numerator is not None and denominator else None


def _group_key(row):
    return tuple(row.get(key) for key in ("market", "platform", "kind", "period_start", "period_end", "currency", "attribution"))


def _comparisons(rows):
    groups = defaultdict(list)
    ungrouped = []
    for row in rows:
        if row.get("status") == "offer_research":
            continue
        values = [row.get(metric) for metric in ("purchases", "spend", "revenue")]
        if all(value is None for value in values):
            continue
        cohort = _group_key(row)
        if all(cohort) and row.get("purchases") is not None:
            groups[cohort].append(row)
        else:
            ungrouped.append(row)
    return groups, ungrouped


def _metric_rows(rows):
    for row in rows:
        purchases = row.get("purchases")
        spend = row.get("spend")
        revenue = row.get("revenue")
        yield (
            _label(row),
            _metric(purchases, 0 if purchases is None or purchases % 1 == 0 else 2),
            _metric(spend),
            _metric(revenue),
            _metric(_divide(spend, purchases)),
            _metric(_divide(revenue, spend)),
        )


def _patterns(rows, key):
    counts = Counter(row[key].strip() for row in rows if isinstance(row.get(key), str) and row[key].strip())
    return ", ".join(f"{_text(value)} ({count})" for value, count in counts.most_common(6)) or "sem rótulos na amostra"


def _timestamp(seconds):
    if not isinstance(seconds, (int, float)) or seconds < 0:
        return "—"
    minutes, seconds = divmod(int(seconds), 60)
    return f"{minutes:02d}:{seconds:02d}"


def _media_evidence(details):
    transcript = details.get("transcript") or []
    scenes = details.get("scenes") or []
    overlays = details.get("screen_text") or []
    result = [f"- Mídia processada. {len(transcript)} segmentos de fala, {len(scenes)} cenas e {len(overlays)} amostras de texto na tela."]
    if details.get("duration_seconds") is not None:
        result.append(f"- Duração de {_timestamp(details['duration_seconds'])} · {details.get('width', '—')} × {details.get('height', '—')} px · {details.get('fps', '—')} fps.")
    if isinstance(transcript, list) and transcript and isinstance(transcript[0], dict):
        opening = transcript[0]
        result.append(f"- Primeira fala detectada em {_timestamp(opening.get('start_seconds'))}. {_text(str(opening.get('text', ''))[:180])}")
    if isinstance(overlays, list) and overlays and isinstance(overlays[0], dict):
        opening = overlays[0]
        result.append(f"- Primeiro texto detectado na tela em {_timestamp(opening.get('timestamp_seconds'))}. {_text(str(opening.get('text', ''))[:180])}")
    for warning in details.get("warnings") or []:
        result.append(f"- {_text(warning)}")
    return result


def build_report(rows: list[dict], media: dict[str, dict], briefs: dict[str, str]) -> str:
    """Return a Markdown audit with provenance and comparison cohorts."""
    output = [
        "# Análise de anúncios e VSLs",
        "",
        "A janela observada usa a primeira e a última data registradas, inclusive. "
        "A ordem das referências públicas prioriza essa janela e depois as variações distintas. "
        "Esses sinais medem presença na amostra.",
        "",
        "Compras, CPA e ROAS vêm das métricas fornecidas. "
        "As comparações exigem o mesmo nicho, mercado, plataforma, tipo de peça, período, moeda e atribuição. "
        "Valores ausentes ou sem denominador aparecem como —. CPA é gasto por compra e ROAS é receita atribuída por unidade gasta.",
        "",
    ]
    by_niche = defaultdict(list)
    for row in rows:
        by_niche[row["niche"]].append(row)

    for niche, entries in sorted(by_niche.items()):
        output.extend([f"## {_text(niche)}", ""])
        unique_records = list({row["id"]: row for row in entries}.values())
        public = [
            row for row in unique_records
            if row.get("status") in {"observed", "active", "reference"} and row.get("url") and _days(row) is not None
            and row.get("kind") in {"ad", "vsl"}
        ]
        public_groups = defaultdict(list)
        for row in public:
            key = (row.get("market") or "", row.get("platform") or "", row.get("kind") or "")
            public_groups[key].append(row)

        for (market, platform, kind), references in sorted(public_groups.items()):
            output.extend([
                f"### Referências públicas · {_text(market)} · {_text(platform)} · {'VSL' if kind == 'vsl' else 'Anúncios'}",
                "",
                f"- Ângulos registrados. {_patterns(references, 'angle')}",
                f"- Formatos registrados. {_patterns(references, 'format')}",
                "",
            ])
            output.extend(_table(
                ("Referência", "Primeiro registro", "Último registro", "Dias", "Variações", "Fonte do registro"),
                (
                    (
                        _label(row), _text(row.get("first_seen")), _text(row.get("last_seen")),
                        _text(_days(row)), _text(row.get("distinct_variants")),
                        _link(row.get("status") or "Fonte", row.get("source_url")),
                    )
                    for row in sorted(references, key=_sort_public)
                ),
            ))

        groups, ungrouped = _comparisons(entries)
        headers = ("Peça", "Compras", "Gasto", "Receita", "CPA", "ROAS")
        for (market, platform, kind, start, end, currency, attribution), records in sorted(groups.items()):
            ordered = sorted(records, key=lambda row: (-row["purchases"], row["id"]))
            group = f"{market} · {platform} · {kind} · {start} a {end} · {currency} · {attribution}"
            output.extend([f"### Compras atribuídas · {_text(group)}", ""])
            output.extend(_table(headers, _metric_rows(ordered)))

        if ungrouped:
            output.extend(["### Métricas sem recorte suficiente para comparação", ""])
            output.extend(_table(headers, _metric_rows(ungrouped)))

        for row in unique_records:
            row_id = row["id"]
            output.extend([f"### {_label(row)}", ""])
            if row.get("status") == "offer_research" or row.get("kind") == "offer":
                output.extend(["Indicadores de oferta publicados pela fonte. O escopo é o informado no registro.", ""])
            for key, title in (("brand", "Marca"), ("angle", "Ângulo"), ("format", "Formato"), ("platform", "Plataforma"), ("status", "Registro")):
                if row.get(key):
                    output.append(f"- {title}. {_text(row[key])}")
            if row.get("source_url"):
                output.append(f"- {_link('Fonte do registro', row['source_url'])}")
            if row.get("landing_url"):
                output.append(f"- {_link('Página de destino', row['landing_url'])}")
            if row.get("copy"):
                output.append(f"- Texto ou observação registrada. {_text(row['copy'][:400])}")
            if media.get(row_id):
                output.extend(_media_evidence(media[row_id]))
            output.append("")
            if briefs.get(row_id):
                output.extend([briefs[row_id], ""])

    if not rows:
        output.extend(["Nenhum registro na amostra.", ""])
    return "\n".join(output)
