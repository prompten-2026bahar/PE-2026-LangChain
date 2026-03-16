# Prebuilt Middleware

LangChain ve [Deep Agents](/oss/python/deepagents/overview), yaygın kullanım senaryoları için önceden hazırlanmış middleware bileşenleri sunar. Bu middleware'ler üretime hazırdır ve yapılandırılabilir.

## Sağlayıcıdan bağımsız middleware'ler

Doküman şu hazır middleware gruplarını listeler:

- Summarization
- Human-in-the-loop
- Model call limit
- Tool call limit
- Model fallback
- PII detection
- To-do list
- LLM tool selector
- Tool retry
- Model retry
- LLM tool emulator
- Context editing
- Shell tool
- File search
- Filesystem
- Subagent

## Summarization

Konuşma geçmişi token sınırına yaklaşınca otomatik özetleme yapar; yakın geçmişi korurken eski bağlamı sıkıştırır.

Kullanım örneği:

```python
from langchain.agents import create_agent
from langchain.agents.middleware import SummarizationMiddleware

agent = create_agent(
    model="gpt-4.1",
    tools=[your_weather_tool, your_calculator_tool],
    middleware=[
        SummarizationMiddleware(
            model="gpt-4.1-mini",
            trigger=("tokens", 4000),
            keep=("messages", 20),
        ),
    ],
)
```

Önemli yapılandırma alanları:

- `model`
- `trigger`
- `keep`
- `token_counter`
- `summary_prompt`
- `trim_tokens_to_summarize`

`trigger`, özetlemenin ne zaman çalışacağını belirler. `keep`, özetleme sonrası ne kadar bağlam tutulacağını tanımlar.

## Human-in-the-loop

Araç çağrılarından önce insan onayı almak için yürütmeyi durdurur. Özellikle:

- yüksek riskli veritabanı yazımları
- finansal işlemler
- uyumluluk gerektiren süreçler

için kullanılır.

## Model ve tool limit middleware'leri

- **Model call limit**: model çağrılarının üst sınırını koyar
- **Tool call limit**: araç çalıştırma sayısını kontrol eder

Bu middleware'ler maliyet, güvenlik ve sonsuz döngü riskini azaltır.

## Retry ve fallback middleware'leri

- **Model fallback**: birincil model hata verirse alternatif modele düşer
- **Tool retry**: başarısız araç çağrılarını tekrar dener
- **Model retry**: model çağrılarını üstel geri çekilmeyle tekrarlar

## PII ve context middleware'leri

- **PII detection**: kişisel veriyi tespit eder ve maskeleme / engelleme uygular
- **Context editing**: konuşma bağlamını temizler, kırpar veya düzenler

## Ajan yeteneklerini genişleten middleware'ler

- **To-do list**: görev planlama ve takip
- **LLM tool selector**: ana modele gitmeden uygun araçları seçtirme
- **Shell tool**: kalıcı shell oturumu sağlama
- **File search**: dosya sistemi üzerinde glob ve grep araması
- **Filesystem**: bağlam ve uzun süreli bellek için dosya sistemi sağlama
- **Subagent**: alt ajan başlatabilme

Hazır middleware'ler, sık ihtiyaç duyulan davranışları sıfırdan yazmadan eklemek için tasarlanmıştır.
