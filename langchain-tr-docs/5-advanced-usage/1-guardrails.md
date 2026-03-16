# Guardrails

Guardrail'ler, ajan yürütmesinin kritik noktalarında içeriği doğrulayarak ve filtreleyerek güvenli, uyumlu yapay zeka uygulamaları geliştirmenize yardımcı olur. Hassas bilgileri algılayabilir, içerik politikalarını zorlayabilir, çıktıları doğrulayabilir ve sorunlar oluşmadan önce güvensiz davranışları engelleyebilir.

## Yaygın kullanım alanları

- Kişisel verilerin sızmasını önlemek
- Prompt injection saldırılarını tespit edip engellemek
- Uygunsuz veya zararlı içeriği bloke etmek
- İş kuralları ile uyumluluk gereksinimlerini uygulamak
- Çıktı kalitesi ve doğruluğunu doğrulamak

Guardrail'ler, [middleware](/oss/python/langchain/middleware) üzerinden uygulanabilir. Böylece yürütmeye ajan başlamadan önce, tamamlandıktan sonra veya model ile araç çağrılarının çevresinde müdahale edilebilir.

## İki yaklaşım

### Deterministik guardrail'ler

Regex, anahtar sözcük eşleştirme veya açık kontroller gibi kural tabanlı mantık kullanır. Hızlı, öngörülebilir ve maliyet açısından avantajlıdır; ancak nüanslı ihlalleri kaçırabilir.

### Model tabanlı guardrail'ler

İçeriği anlamsal olarak değerlendirmek için LLM ya da sınıflandırıcı kullanır. Kural tabanlı yaklaşımın kaçırdığı daha ince sorunları yakalayabilir; fakat daha yavaş ve daha pahalıdır.

LangChain, hem yerleşik guardrail'ler hem de kendi güvenlik katmanlarınızı yazmanız için esnek middleware sistemi sunar.

## Yerleşik guardrail'ler

### Kişisel veri algılama

LangChain, konuşmalardaki Kişisel Olarak Tanımlanabilir Bilgileri (PII) algılamak ve işlemek için yerleşik middleware sağlar. E-posta, kredi kartı, IP adresi ve benzeri veri türleri tespit edilebilir.

Desteklenen işleme stratejileri:

- `redact`: değeri `[REDACTED_{PII_TYPE}]` ile değiştirir
- `mask`: değerin bir kısmını gizler
- `hash`: deterministik bir hash ile değiştirir
- `block`: algılandığında hata fırlatır

```python
from langchain.agents import create_agent
from langchain.agents.middleware import PIIMiddleware

agent = create_agent(
    model="gpt-4.1",
    tools=[customer_service_tool, email_tool],
    middleware=[
        PIIMiddleware("email", strategy="redact", apply_to_input=True),
        PIIMiddleware("credit_card", strategy="mask", apply_to_input=True),
        PIIMiddleware(
            "api_key",
            detector=r"sk-[a-zA-Z0-9]{32}",
            strategy="block",
            apply_to_input=True,
        ),
    ],
)
```

Yerleşik PII türleri:

- `email`
- `credit_card`
- `ip`
- `mac_address`
- `url`

Önemli yapılandırma seçenekleri:

- `pii_type`
- `strategy`
- `detector`
- `apply_to_input`
- `apply_to_output`
- `apply_to_tool_results`

### İnsan sürece dahil guardrail'i

Yüksek riskli araçların çalıştırılmasından önce insan onayı istemek için yerleşik middleware bulunur. Finansal işlemler, dış taraflara e-posta gönderme veya üretim verisi silme gibi hassas operasyonlarda etkilidir.

```python
from langchain.agents import create_agent
from langchain.agents.middleware import HumanInTheLoopMiddleware
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import Command

agent = create_agent(
    model="gpt-4.1",
    tools=[search_tool, send_email_tool, delete_database_tool],
    middleware=[
        HumanInTheLoopMiddleware(
            interrupt_on={
                "send_email": True,
                "delete_database": True,
                "search": False,
            }
        ),
    ],
    checkpointer=InMemorySaver(),
)
```

Bu yaklaşım için kalıcılık gerektiğinden aynı `thread_id` ile devam edilmelidir.

## Özel guardrail'ler

Daha gelişmiş guardrail'ler için ajan çalışmadan önce veya sonra devreye giren özel middleware yazabilirsiniz.

### Ajan öncesi guardrail

İstek daha başlangıçta doğrulanır. Kimlik doğrulama, oran sınırlama veya uygunsuz istekleri işlem başlamadan önce engelleme için uygundur.

```python
class ContentFilterMiddleware(AgentMiddleware):
    def __init__(self, banned_keywords: list[str]):
        super().__init__()
        self.banned_keywords = [kw.lower() for kw in banned_keywords]
```

### Ajan sonrası guardrail

Son yanıt kullanıcıya dönmeden önce doğrulanır. Model tabanlı güvenlik kontrolü, kalite doğrulaması ve uyumluluk taraması için uygundur.

Özetle guardrail yapısı, deterministik kurallarla maliyet avantajı sağlarken model tabanlı denetimlerle daha derin güvenlik taramaları yapmanıza imkân verir.
