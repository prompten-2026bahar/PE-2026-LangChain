from __future__ import annotations

import os

os.environ.setdefault("ANONYMIZED_TELEMETRY", "false")

import argparse
import sys
from pathlib import Path

from lc_pdf_qa.ingest import run_ingest
from lc_pdf_qa.qa import ask as run_ask
from lc_pdf_qa.settings import data_path


def _cmd_ingest(args: argparse.Namespace) -> None:
    root = Path(args.data_dir).resolve() if args.data_dir else data_path()
    n = run_ingest(root, clear_index=not args.append_docs)
    print(f"İndeks: {n} parça.")


def _ollama_unreachable_msg() -> None:
    print(
        "Ollama'ya bağlanılamadı (localhost:11434 reddedildi). "
        "Ollama uygulamasını çalıştırın, ardından: ollama list",
        file=sys.stderr,
    )


def _is_connection_refused(exc: BaseException, _seen: set[int] | None = None) -> bool:
    if _seen is None:
        _seen = set()
    eid = id(exc)
    if eid in _seen:
        return False
    _seen.add(eid)
    if isinstance(exc, ConnectionRefusedError):
        return True
    if isinstance(exc, OSError) and getattr(exc, "winerror", None) == 10061:
        return True
    s = str(exc)
    low = s.lower()
    if "10061" in s or "connection refused" in low or "reddetti" in low:
        return True
    inner = getattr(exc, "__cause__", None) or getattr(exc, "__context__", None)
    if inner is not None and inner is not exc:
        return _is_connection_refused(inner, _seen)
    return False


def _cmd_ask(args: argparse.Namespace) -> None:
    try:
        out = run_ask(args.question)
    except Exception as e:
        if _is_connection_refused(e):
            _ollama_unreachable_msg()
            raise SystemExit(1) from e
        raise
    print(out.get("answer", ""))
    ctx = out.get("context", [])
    if ctx:
        print("\n--- Kaynaklar ---")
        seen: set[str] = set()
        for doc in ctx:
            src = doc.metadata.get("source", "?")
            if src in seen:
                continue
            seen.add(src)
            print(f"- {src}")


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="PDF / ders notu RAG (Ollama + Chroma)")
    sub = parser.add_subparsers(dest="command", required=True)

    p_ingest = sub.add_parser("ingest", help="data/ altındaki pdf, txt, md dosyalarını indeksle")
    p_ingest.add_argument(
        "--data-dir",
        type=str,
        default=None,
        help="Varsayılan: .env DATA_DIR veya proje kökünde data/",
    )
    p_ingest.add_argument(
        "--append-docs",
        action="store_true",
        help="Mevcut indeksi silmeden belge ekle",
    )
    p_ingest.set_defaults(func=_cmd_ingest)

    p_ask = sub.add_parser("ask", help="İndekslenmiş notlara göre soru sor")
    p_ask.add_argument("question", type=str, help="Soru metni")
    p_ask.set_defaults(func=_cmd_ask)

    args = parser.parse_args(argv)
    try:
        args.func(args)
    except FileNotFoundError as e:
        print(e, file=sys.stderr)
        raise SystemExit(1) from e
    except SystemExit:
        raise
    except Exception as e:  # noqa: BLE001
        if _is_connection_refused(e):
            _ollama_unreachable_msg()
            raise SystemExit(1) from e
        print(f"Hata: {e}", file=sys.stderr)
        raise SystemExit(1) from e


if __name__ == "__main__":
    main()
