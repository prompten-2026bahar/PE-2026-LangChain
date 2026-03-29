# Ders notu / PDF RAG

PDF, TXT ve Markdown dosyalarını indeksler; soruları **Ollama** (LLM) ve **sentence-transformers** (çok dilli embedding) ile yanıtlar. Vektör deposu: **Chroma** (`CHROMA_DIR`).

## Gereksinimler

- Python 3.10+
- [Ollama](https://ollama.com): uygulama/servis çalışır durumda olmalı; model çekilmiş olmalı (ör. `ollama pull llama3.1`)

## Kurulum

```bash
python -m venv .venv
```

Sanal ortamı açıp kurulum (Windows PowerShell):

```powershell
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install --default-timeout=600 --retries 10 -r requirements.txt
copy .env.example .env
```

`pip` çıktısında yol `...\Python311\...` gibi **sistem** Python’u gösteriyorsa sanal ortam kapalıdır; `ask` / `ingest` için de `Activate.ps1` sonrası aynı oturumda `python -m lc_pdf_qa.cli ...` kullanın.

**PowerShell “running scripts is disabled”:** `Activate.ps1` çalışmaz. Seçenekler:

- Sanal ortamı **açmadan** doğrudan venv Python kullanın:
  ```powershell
  .\.venv\Scripts\python.exe -m pip install -r requirements.txt
  .\.venv\Scripts\python.exe -m streamlit run app.py
  .\.venv\Scripts\python.exe -m lc_pdf_qa.cli ingest
  ```
- Bir kez (kullanıcı için) betiğe izin: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`
- **cmd.exe:** `.\.venv\Scripts\activate.bat` sonra normal `python` / `pip`

Linux / macOS: `source .venv/bin/activate` sonrası aynı `python -m pip ...` satırları; `.env` için `cp .env.example .env`.

**`Read timed out`:** Aynı `pip install` komutunu yeniden çalıştırın. Gerekirse kablolu ağ veya VPN deneyin.

İlk `ingest` sırasında Hugging Face embedding modeli indirilebilir; önbellek: `HF_HOME` veya varsayılan kullanıcı cache dizini. Çevrimdışı kullanım için (model önbellekteyken): `HF_HUB_OFFLINE=1`, `TRANSFORMERS_OFFLINE=1`.

## Veri

- Dosyalar: `DATA_DIR` (varsayılan `data/`) altında, recursive: `*.pdf`, `*.txt`, `*.md`
- Streamlit ile yüklenen dosyalar: `data/uploads/`

## Kullanım

```bash
python -m lc_pdf_qa.cli ingest
python -m lc_pdf_qa.cli ask "Soru metni"
streamlit run app.py
```

İsteğe bağlı:

```bash
python -m lc_pdf_qa.cli ingest --data-dir /path/to/notes
python -m lc_pdf_qa.cli ingest --append-docs
```

## Ortam değişkenleri (`.env`)

| Değişken | Varsayılan | Açıklama |
|----------|------------|----------|
| `OLLAMA_BASE_URL` | `http://localhost:11434` | Ollama sunucusu |
| `OLLAMA_LLM` | `llama3.1` | Model adı |
| `HF_EMBED_MODEL` | `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2` | Embedding modeli |
| `CHROMA_DIR` | `.chroma` | Kalıcı indeks dizini |
| `DATA_DIR` | `data` | Kaynak dosya kökü |

## Dağıtım notları

- `CHROMA_DIR` ve `DATA_DIR` üretimde kalıcı bir volume’a bağlanmalı.
- Ollama aynı makinede veya erişilebilir bir host’ta çalışmalı; `OLLAMA_BASE_URL` buna göre ayarlanır.
- `torch` ve `sentence-transformers` varsayılan olarak CPU ile uyumludur.
