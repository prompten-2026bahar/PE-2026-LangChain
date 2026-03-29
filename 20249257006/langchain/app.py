from __future__ import annotations

import os

os.environ.setdefault("ANONYMIZED_TELEMETRY", "false")

import streamlit as st

from lc_pdf_qa.ingest import run_ingest
from lc_pdf_qa.qa import ask as rag_ask
from lc_pdf_qa.settings import chroma_path, data_path


def _render_sources(ctx: list) -> None:
    seen: set[str] = set()
    for doc in ctx:
        src = doc.metadata.get("source", "?")
        key = f"{src}:{doc.page_content[:80]}"
        if key in seen:
            continue
        seen.add(key)
        st.markdown(f"**Kaynak:** `{src}`")
        st.text(doc.page_content[:1200])


st.set_page_config(page_title="Prompt Mühendisliği - İlk Proje", layout="wide")
st.title("Prompt Mühendisliği - İlk Proje")
st.caption("Soldan PDF/TXT/MD yükleyin → **İndeksle** → aşağıdaki kutuya yazın.")

root = data_path()
root.mkdir(parents=True, exist_ok=True)
upload_dir = root / "uploads"
upload_dir.mkdir(parents=True, exist_ok=True)

st.sidebar.subheader("Veri")
st.sidebar.code(str(root), language="text")

uploaded = st.sidebar.file_uploader(
    "PDF / TXT / MD yükle",
    type=["pdf", "txt", "md"],
    accept_multiple_files=True,
)
if uploaded:
    for f in uploaded:
        (upload_dir / f.name).write_bytes(f.getvalue())
    st.sidebar.success(f"{len(uploaded)} dosya kaydedildi.")

if st.sidebar.button("İndeksle"):
    with st.spinner("İndeksleniyor…"):
        try:
            n = run_ingest(root, clear_index=True)
            st.sidebar.success(f"{n} parça indekslendi.")
        except Exception as e:  # noqa: BLE001
            st.sidebar.error(str(e))

if st.sidebar.button("Sohbeti temizle"):
    st.session_state.pop("chat_messages", None)
    st.rerun()

st.sidebar.divider()
st.sidebar.caption(f"İndeks: `{chroma_path()}`")

if "chat_messages" not in st.session_state:
    st.session_state.chat_messages = []

for msg in st.session_state.chat_messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg["role"] == "assistant" and msg.get("context"):
            with st.expander("Kaynaklar"):
                _render_sources(msg["context"])

if prompt := st.chat_input("Sorunuzu yazın…"):
    st.session_state.chat_messages.append({"role": "user", "content": prompt})
    try:
        with st.spinner("Yanıt hazırlanıyor…"):
            out = rag_ask(prompt)
        answer = (out.get("answer") or "").strip() or "_Yanıt boş._"
        ctx = out.get("context") or []
    except FileNotFoundError as e:
        answer = str(e)
        ctx = []
    except Exception as e:  # noqa: BLE001
        answer = f"Hata: {e}"
        ctx = []
    st.session_state.chat_messages.append(
        {"role": "assistant", "content": answer, "context": ctx}
    )
    st.rerun()
