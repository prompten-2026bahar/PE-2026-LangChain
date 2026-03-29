from __future__ import annotations

import os
import shutil
from pathlib import Path

os.environ.setdefault("ANONYMIZED_TELEMETRY", "false")

from langchain_chroma import Chroma
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from lc_pdf_qa.embeddings_factory import get_embeddings
from lc_pdf_qa.settings import chroma_path, data_path

COLLECTION_NAME = "ders_notlari"
TEXT_EXTENSIONS = {".txt", ".md"}


def _load_pdf(path: Path) -> list[Document]:
    loader = PyPDFLoader(str(path))
    docs = loader.load()
    for d in docs:
        d.metadata["source"] = str(path)
    return docs


def _load_text_file(path: Path) -> list[Document]:
    loader = TextLoader(str(path), encoding="utf-8")
    docs = loader.load()
    for d in docs:
        d.metadata["source"] = str(path)
    return docs


def collect_documents(root: Path) -> list[Document]:
    if not root.is_dir():
        return []

    out: list[Document] = []
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        suf = path.suffix.lower()
        try:
            if suf == ".pdf":
                out.extend(_load_pdf(path))
            elif suf in TEXT_EXTENSIONS:
                out.extend(_load_text_file(path))
        except Exception as e:  # noqa: BLE001
            raise RuntimeError(f"Dosya okunamadı: {path}") from e
    return out


def run_ingest(data_dir: Path | None = None, *, clear_index: bool = True) -> int:
    root = data_dir or data_path()
    root.mkdir(parents=True, exist_ok=True)

    docs = collect_documents(root)
    if not docs:
        raise SystemExit(f"İndekslenecek dosya yok: {root} (pdf, txt, md)")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150,
        add_start_index=True,
    )
    splits = splitter.split_documents(docs)

    emb = get_embeddings()
    cp = chroma_path()

    if clear_index and cp.exists():
        shutil.rmtree(cp)

    if clear_index or not cp.exists():
        Chroma.from_documents(
            documents=splits,
            embedding=emb,
            persist_directory=str(cp),
            collection_name=COLLECTION_NAME,
        )
    else:
        store = Chroma(
            persist_directory=str(cp),
            embedding_function=emb,
            collection_name=COLLECTION_NAME,
        )
        store.add_documents(splits)
    return len(splits)
