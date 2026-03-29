from __future__ import annotations

from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama

from lc_pdf_qa.embeddings_factory import get_embeddings
from lc_pdf_qa.ingest import COLLECTION_NAME
from lc_pdf_qa.settings import OLLAMA_BASE_URL, OLLAMA_LLM, chroma_path

SYSTEM_PROMPT = """Sen ders notları üzerinden soru cevaplayan bir asistansın.
Yalnızca verilen bağlamdaki bilgileri kullan. Bağlamda cevap yoksa bunu Türkçe söyle; uydurma.
Cevabı Türkçe, net ve öğrenciye uygun yaz."""


def get_vectorstore() -> Chroma:
    cp = chroma_path()
    if not cp.exists():
        raise FileNotFoundError(
            f"İndeks yok: {cp}. Önce: python -m lc_pdf_qa.cli ingest"
        )
    return Chroma(
        persist_directory=str(cp),
        embedding_function=get_embeddings(),
        collection_name=COLLECTION_NAME,
    )


def build_qa_chain():
    retriever = get_vectorstore().as_retriever(search_kwargs={"k": 5})
    llm = ChatOllama(
        model=OLLAMA_LLM,
        base_url=OLLAMA_BASE_URL,
        temperature=0.2,
    )
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", SYSTEM_PROMPT),
            (
                "human",
                "Bağlam:\n{context}\n\nSoru: {input}",
            ),
        ]
    )
    doc_chain = create_stuff_documents_chain(llm, prompt)
    return create_retrieval_chain(retriever, doc_chain)


def ask(question: str) -> dict:
    chain = build_qa_chain()
    return chain.invoke({"input": question})
