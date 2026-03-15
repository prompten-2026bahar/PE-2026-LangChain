# Messages

Mesajlar, LangChain içinde modeller için bağlamın temel birimidir. Bir LLM ile etkileşimde konuşma durumunu temsil etmek için gereken içerik ve meta veriyi taşırlar.

Bir mesaj şu unsurları içerir:

- **Role**: mesaj türünü belirtir
- **Content**: asıl içerik
- **Metadata**: yanıt bilgileri, mesaj kimliği, token kullanımı gibi isteğe bağlı alanlar

LangChain, tüm sağlayıcılarla çalışan standart mesaj tipleri sunar.

## Temel kullanım

Mesaj nesneleri oluşturulup modele geçirilir:

```python
from langchain.chat_models import init_chat_model
from langchain.messages import HumanMessage, AIMessage, SystemMessage

model = init_chat_model("gpt-5-nano")

messages = [
    SystemMessage("You are a helpful assistant."),
    HumanMessage("Hello, how are you?")
]
response = model.invoke(messages)
```

## Metin istemleri

Tek seferlik görevlerde doğrudan string verilebilir:

```python
response = model.invoke("Write a haiku about spring")
```

Bu yaklaşım:

- tekil isteklerde
- konuşma geçmişi gerekmiyorsa
- daha az kod istendiğinde

uygundur.

## Mesaj istemleri

Çok turlu konuşmalar, çoklu ortam içerikleri ve sistem talimatları için mesaj listeleri tercih edilir.

## Sözlük biçimi

Mesajlar OpenAI chat completions biçiminde sözlükler olarak da verilebilir:

```python
messages = [
    {"role": "system", "content": "You are a poetry expert"},
    {"role": "user", "content": "Write a haiku about spring"},
]
```

## Mesaj türleri

- **System message**: model davranışını belirler
- **Human message**: kullanıcı girdisini temsil eder
- **AI message**: model çıktısını temsil eder
- **Tool message**: araç çağrısı sonuçlarını taşır

### SystemMessage

Modelin rolünü, tonunu ve cevaplama ilkelerini belirlemek için kullanılır.

### HumanMessage

Kullanıcı girdisini temsil eder; metin, görsel, ses ve diğer çok modlu içerikleri taşıyabilir.

### AIMessage

Model çağrısının sonucudur. Metin, tool call ve sağlayıcıya özgü metadata içerebilir.

### ToolMessage

Araç çağrılarının döndürdüğü sonuçları konuşma akışına ekler.

Mesaj sistemi, farklı sağlayıcılar arasında tutarlı konuşma geçmişi yönetimi sağladığı için LangChain mimarisinin temel parçalarından biridir.
