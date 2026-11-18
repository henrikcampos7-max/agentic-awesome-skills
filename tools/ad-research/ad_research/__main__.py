import argparse
import json
import os
from pathlib import Path
import sys
from tempfile import TemporaryDirectory
from zipfile import BadZipFile

from .creative import generate_brief
from .inputs import MEDIA_EXTENSIONS, attach_metrics, extract_bundle, load_records
from .media import analyze_media
from .report import build_report


def arguments():
    parser = argparse.ArgumentParser(description="Analisa criativos, VSLs e dados autorizados de campanhas.")
    parser.add_argument("--dataset", type=Path, default=Path("examples"))
    parser.add_argument("--catalog", default="research-us.csv")
    parser.add_argument("--output", type=Path, default=Path("result"))
    parser.add_argument("--cloud-input", action="store_true")
    parser.add_argument("--ai", action="store_true")
    parser.add_argument("--model", default="gpt-5.4-mini")
    parser.add_argument("--whisper-model", default="base.en", choices=["tiny.en", "base.en", "small.en", "base", "small"])
    return parser.parse_args()


def select_brief_sources(records, metrics, media):
    winners = {}
    for row in metrics:
        purchases = row["purchases"]
        if not purchases:
            continue
        keys = ("niche", "market", "platform", "kind", "period_start", "period_end", "currency", "attribution")
        cohort = tuple(row[key].casefold() for key in keys)
        if cohort not in winners or purchases > winners[cohort]["purchases"]:
            winners[cohort] = row
    preferred = {row["id"] for row in winners.values()}
    eligible = [row for row in records.values() if row["kind"] in {"ad", "vsl"}]
    return sorted(eligible, key=lambda row: (row["id"] not in preferred, row["id"] not in media))


def run(dataset: Path, catalog: str, args) -> int:
    records = load_records(dataset / catalog)
    metrics_path = dataset / "metrics.csv"
    metrics = list(attach_metrics(records, metrics_path)) if metrics_path.is_file() else []
    measured_ids = {row["id"] for row in metrics}
    rows = [record for key, record in records.items() if key not in measured_ids] + metrics
    offer_path = dataset / "offer.json"
    offer = {}
    if offer_path.is_file():
        if offer_path.stat().st_size > 128 * 1024:
            raise ValueError("offer.json deve ter até 128 KiB.")
        offer = json.loads(offer_path.read_text(encoding="utf-8-sig"))
        if not isinstance(offer, dict):
            raise ValueError("offer.json deve conter um objeto JSON.")

    videos = {}
    for path in sorted((dataset / "media").glob("*")):
        if path.suffix.lower() in MEDIA_EXTENSIONS:
            if path.stem not in records or path.stem in videos:
                raise ValueError("Cada vídeo deve ter um nome único que corresponda a um ID de ads.csv.")
            videos[path.stem] = path
    if len(videos) > 8:
        raise ValueError("Envie até oito vídeos por execução.")
    requested_ai = args.ai
    use_ai = requested_ai and bool(os.environ.get("OPENAI_API_KEY"))
    notes = []
    if requested_ai and not use_ai:
        notes.append("O modo IA foi solicitado sem o secret OPENAI_API_KEY. O relatório usa os dados extraídos.")

    media = {}
    prompts = {}
    for identifier, path in videos.items():
        print(f"Analisando mídia {identifier}", flush=True)
        try:
            analysis = analyze_media(path, args.whisper_model, include_frames=use_ai)
            frames = analysis.pop("frames", [])
            if frames:
                prompts[identifier] = frames
            media[identifier] = analysis
        except (RuntimeError, ValueError, OSError) as exc:
            notes.append(f"Mídia {identifier}: falha de extração ({type(exc).__name__}). Confira o arquivo e o limite de duração.")

    briefs = {}
    if use_ai:
        eligible = select_brief_sources(records, metrics, media)
        if len(eligible) > 8:
            notes.append("A IA analisou até oito referências nesta execução. Líderes em compras de cada grupo comparável e registros com mídia têm prioridade.")
        for row in eligible[:8]:
            identifier = row["id"]
            evidence = media.get(identifier)
            if evidence is not None and identifier in prompts:
                evidence = {**evidence, "frames": prompts[identifier]}
            try:
                briefs[identifier] = generate_brief(row, evidence, offer, args.model)
            except RuntimeError as exc:
                notes.append(f"Briefing IA de {identifier}: {exc}")

    args.output.mkdir(parents=True, exist_ok=True)
    report = build_report(rows, media, briefs)
    if notes:
        report += "\n\n## Avisos da execução\n\n" + "\n".join(f"- {note}" for note in notes) + "\n"
    (args.output / "relatorio.md").write_text(report, encoding="utf-8")
    (args.output / "evidencias.json").write_text(
        json.dumps({"records": rows, "media": media, "notes": notes}, ensure_ascii=False, indent=2, allow_nan=False),
        encoding="utf-8",
    )
    print(f"Relatório concluído com {len(records)} referências e {len(media)} mídias analisadas.")
    return 0


def main():
    args = arguments()
    try:
        if not args.cloud_input:
            return run(args.dataset, args.catalog, args)
        url = os.environ.get("AD_RESEARCH_INPUT_URL")
        if not url:
            raise ValueError("Cadastre o secret AD_RESEARCH_INPUT_URL para usar o pacote na nuvem.")
        with TemporaryDirectory(prefix="ad-research-") as temp:
            extract_bundle(url, Path(temp))
            return run(Path(temp), "ads.csv", args)
    except (BadZipFile, ValueError, FileNotFoundError) as exc:
        print(f"Entrada inválida: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
