import csv
from datetime import date
from pathlib import Path
import re
import shutil
from urllib.parse import urlsplit
from urllib.request import Request, urlopen
from zipfile import ZipFile


MAX_BUNDLE = 350 * 1024 * 1024
MAX_ROWS = 5000
MEDIA_EXTENSIONS = {".mp4", ".mov", ".mkv", ".webm"}
AD_ID = re.compile(r"[A-Za-z0-9][A-Za-z0-9_.-]{0,99}")


def extract_bundle(url: str, destination: Path) -> None:
    if urlsplit(url).scheme != "https":
        raise ValueError("A URL do pacote deve usar HTTPS.")
    archive = destination / "input.zip"
    try:
        request = Request(url, headers={"User-Agent": "AdResearch/1.0"})
        with urlopen(request, timeout=30) as response, archive.open("wb") as out:
            if urlsplit(response.url).scheme != "https":
                raise ValueError("Redirecionamento do pacote para protocolo inesperado.")
            received = 0
            while chunk := response.read(1024 * 1024):
                received += len(chunk)
                if received > MAX_BUNDLE:
                    raise ValueError("Pacote acima de 350 MiB.")
                out.write(chunk)
    except Exception:
        raise ValueError("Falha ao baixar o ZIP via HTTPS. Confira a validade da URL e o limite de 350 MiB.") from None

    with ZipFile(archive) as bundle:
        entries = bundle.infolist()
        if len(entries) > 100 or sum(entry.file_size for entry in entries) > MAX_BUNDLE:
            raise ValueError("O ZIP expandido deve ter até 100 itens e 350 MiB.")
        seen = set()
        for entry in entries:
            if entry.filename == "media/" and entry.is_dir():
                continue
            name = entry.filename.split("/")
            media = (
                len(name) == 2
                and name[0] == "media"
                and Path(name[1]).suffix.lower() in MEDIA_EXTENSIONS
                and AD_ID.fullmatch(Path(name[1]).stem)
                and not {"\\", ":"}.intersection(name[1])
            )
            if not media and entry.filename not in {"ads.csv", "metrics.csv", "offer.json"}:
                raise ValueError("O ZIP contém um caminho fora do formato esperado.")
            key = entry.filename.casefold()
            if key in seen:
                raise ValueError("O ZIP contém arquivos com o mesmo nome.")
            seen.add(key)
            target = destination.joinpath(*name)
            target.parent.mkdir(parents=True, exist_ok=True)
            with bundle.open(entry) as source, target.open("wb") as out:
                shutil.copyfileobj(source, out)


def read_csv(path: Path, required: set[str]):
    with path.open(encoding="utf-8-sig", newline="") as source:
        sample = source.read(8192)
        source.seek(0)
        try:
            delimiter = csv.Sniffer().sniff(sample.splitlines()[0], delimiters=",;").delimiter
        except (csv.Error, IndexError):
            delimiter = ","
        reader = csv.DictReader(source, delimiter=delimiter)
        reader.fieldnames = [field.strip().lower() for field in (reader.fieldnames or [])]
        if len(set(reader.fieldnames)) != len(reader.fieldnames):
            raise ValueError(f"{path.name}: cabeçalhos repetidos.")
        if missing := required - set(reader.fieldnames):
            raise ValueError(f"{path.name}: faltam colunas {', '.join(sorted(missing))}.")
        for number, row in enumerate(reader, 2):
            if number > MAX_ROWS + 1:
                raise ValueError(f"{path.name}: máximo de {MAX_ROWS} registros.")
            if None in row or None in row.values():
                raise ValueError(f"{path.name}: quantidade de campos inválida na linha {number}.")
            yield {key: value.strip() for key, value in row.items()}


def timestamp(value):
    return date.fromisoformat(value).isoformat() if value else ""


def number(value, integral=False):
    if value in ("", None):
        return None
    if not re.fullmatch(r"[0-9]+(?:\.[0-9]+)?", value) or len(value) > 24:
        raise ValueError("Informe números não negativos, sem separador de milhar e com ponto decimal.")
    if integral and "." in value:
        raise ValueError("Informe números inteiros para quantidade de variantes.")
    return int(value) if integral else float(value)


def https_link(value):
    if not value:
        return ""
    parts = urlsplit(value)
    if parts.scheme != "https" or not parts.hostname or parts.username or parts.password:
        raise ValueError("Use URLs HTTPS sem credenciais na referência e na página de destino.")
    return value


def load_records(path: Path):
    records = {}
    for row in read_csv(path, {"id", "niche", "market", "kind", "title"}):
        identifier = row["id"]
        if not AD_ID.fullmatch(identifier) or identifier in records:
            raise ValueError("Cada anúncio precisa de um ID válido e único por arquivo.")
        if row["kind"] not in {"ad", "vsl", "offer"} or not row["title"] or not row["niche"]:
            raise ValueError(f"{identifier}: preencha título, nicho e tipo ad, vsl ou offer.")
        row["market"] = row["market"].upper()
        if not row["market"]:
            raise ValueError(f"{identifier}: informe o mercado.")
        for key in ("url", "landing_url", "source_url"):
            row[key] = https_link(row.get(key, ""))
        for key in ("first_seen", "last_seen"):
            row[key] = timestamp(row.get(key))
        if row["last_seen"] and row["first_seen"] > row["last_seen"]:
            raise ValueError(f"{identifier}: datas de observação invertidas.")
        row["distinct_variants"] = number(row.get("distinct_variants"), integral=True)
        row["status"] = row.get("status") or "reference"
        # Campaign outcomes come only from the separate authorized metrics file.
        for key in ("spend", "purchases", "revenue", "currency", "period_start", "period_end", "attribution"):
            row.pop(key, None)
        records[identifier] = row
    if not records:
        raise ValueError("ads.csv está vazio.")
    return records


def attach_metrics(records, path: Path):
    required = {"id", "market", "platform", "period_start", "period_end", "attribution", "currency",
                "spend", "purchases", "revenue"}
    seen = set()
    for row in read_csv(path, required):
        identifier = row["id"]
        record = records.get(identifier)
        if record is None or record["kind"] not in {"ad", "vsl"} or record["status"] == "offer_research":
            raise ValueError(f"{identifier}: métricas sem anúncio ou VSL correspondente.")
        scope = (row["market"].upper(), row["platform"].casefold())
        expected_scope = (record["market"], record.get("platform", "").casefold())
        if scope != expected_scope or not all(scope):
            raise ValueError(f"{identifier}: mercado e plataforma devem coincidir nos dois CSVs.")
        start = timestamp(row["period_start"])
        end = timestamp(row["period_end"])
        currency = row["currency"].upper()
        attribution = row["attribution"]
        if not start or not end or start > end or not re.fullmatch(r"[A-Z]{3}", currency) or not attribution:
            raise ValueError(f"{identifier}: informe período válido, moeda e atribuição.")
        cohort = (identifier, start, end, currency, attribution)
        if cohort in seen:
            raise ValueError(f"{identifier}: linha duplicada na mesma janela de medição.")
        seen.add(cohort)
        yield {
            **record,
            "period_start": start,
            "period_end": end,
            "currency": currency,
            "attribution": attribution,
            **{key: number(row[key]) for key in ("spend", "purchases", "revenue")},
        }
