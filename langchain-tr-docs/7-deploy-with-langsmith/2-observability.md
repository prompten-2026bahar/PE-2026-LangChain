# Observability

LangChain ile ajan geliştirirken ve çalıştırırken şu konularda görünürlük gerekir:

- hangi araçların çağrıldığı
- hangi prompt'ların üretildiği
- modelin nasıl karar verdiği

`create_agent` ile oluşturulan LangChain ajanları, [LangSmith](/langsmith/home) üzerinden tracing desteğini doğal olarak sunar. LangSmith; LLM uygulamalarını kaydetme, hata ayıklama, değerlendirme ve izleme için kullanılır.

## Trace nedir?

[*Traces*](/langsmith/observability-concepts#traces), ajan yürütmesinin her adımını kaydeder:

- ilk kullanıcı girdisi
- model etkileşimleri
- tool call'lar
- karar noktaları
- final yanıt

Bu yürütme verisi şunlar için kullanılır:

- sorunları ayıklamak
- farklı girdilerde performansı değerlendirmek
- üretimde kullanım desenlerini izlemek

## Gereksinimler

- LangSmith hesabı
- LangSmith API anahtarı

## Tracing'i etkinleştirme

Ek kod gerekmeden tracing açılabilir:

```bash
export LANGSMITH_TRACING=true
export LANGSMITH_API_KEY=<your-api-key>
```

## Hızlı başlangıç

Normal ajan kodunuzu çalıştırmanız yeterlidir; tüm adımlar otomatik izlenir:

```python
from langchain.agents import create_agent

agent = create_agent(
    model="gpt-4.1",
    tools=[send_email, search_web],
    system_prompt="You are a helpful assistant that can send emails and search the web."
)
```

Varsayılan olarak izler `default` adlı projeye yazılır.

## Seçmeli tracing

İsterseniz tüm uygulama yerine yalnızca belirli çağrıları `tracing_context` içinde izleyebilirsiniz:

```python
import langsmith as ls

with ls.tracing_context(enabled=True):
    agent.invoke({"messages": [{"role": "user", "content": "Send a test email"}]})
```

## Proje adı belirleme

İzleri özel bir proje adına yazmak için `LANGSMITH_PROJECT` ortam değişkeni kullanılabilir.

Bu sayfa, ajan davranışını görünür hale getirip üretimde hata ayıklama ve izleme yapmanın temel yolunu açıklar.
