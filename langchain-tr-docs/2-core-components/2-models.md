# Models

LLM'ler, insan benzeri metni yorumlayıp üretebilen güçlü yapay zeka araçlarıdır. İçerik yazma, çeviri, özetleme ve soru cevaplama gibi görevleri her biri için ayrı özel eğitim gerekmeden gerçekleştirebilirler.

Birçok model, metin üretiminin yanında şu yetenekleri de destekler:

- **Tool calling**
- **Structured output**
- **Multimodality**
- **Reasoning**

Modeller, LangChain ajanlarının akıl yürütme motorudur. Hangi aracın çağrılacağına, araç sonuçlarının nasıl yorumlanacağına ve final yanıtın ne zaman verileceğine model karar verir.

## Temel kullanım

Modeller iki şekilde kullanılabilir:

1. **Ajanlarla birlikte**
2. **Bağımsız olarak**

Aynı model arayüzü iki durumda da çalışır.

## Model başlatma

Bağımsız bir modeli başlatmanın en kolay yolu `init_chat_model` kullanmaktır:

```python
from langchain.chat_models import init_chat_model

model = init_chat_model("gpt-5.2")
response = model.invoke("Why do parrots talk?")
```

LangChain; OpenAI, Anthropic, Azure, Google Gemini, AWS Bedrock ve HuggingFace gibi büyük sağlayıcıları destekler.

Örnekler:

- `init_chat_model("gpt-5.2")`
- `init_chat_model("claude-sonnet-4-6")`
- `init_chat_model("google_genai:gemini-2.5-flash-lite")`

## Desteklenen yetenekler

Model sayfası özellikle şu yeteneklere odaklanır:

- araç çağırma
- yapılandırılmış çıktı
- çoklu ortam desteği
- akıl yürütme

## Temel yöntemler

- `invoke`: tam yanıt üretir
- `stream`: yanıtı akış halinde döndürür
- `batch`: birden çok isteği verimli biçimde işler

## Parametreler

Model davranışı parametrelerle kontrol edilir. Yaygın parametreler:

- `model`
- `api_key`
- `temperature`
- `max_tokens`
- `timeout`

Sağlayıcıya göre desteklenen parametre seti değişebilir. LangChain'in standart arayüzü, sağlayıcı değiştirmeyi ve farklı modelleri karşılaştırmayı kolaylaştırır.
