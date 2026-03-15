# Değişiklik Günlüğü

Bu sayfa, LangChain ekosistemindeki son sürüm notlarını ve önemli değişiklikleri listeler. RSS beslemesi ile Slack, e-posta, Discord botları ve diğer abonelik araçlarına entegre edilebilir.

## 10 Mart 2026

### `langgraph` v1.1

- Tür güvenli akış desteği için `stream()` ve `astream()` çağrılarına `version="v2"` verilebilir; böylece her parça `type`, `ns` ve `data` anahtarlarını içeren birleşik `StreamPart` çıktısı döndürür.
- Tür güvenli `invoke()` desteği ile `version="v2"` verildiğinde `.value` ve `.interrupts` alanlarına sahip `GraphOutput` nesnesi elde edilir.
- `invoke()` ve `values` akış çıktısı, bildirilen Pydantic modeline veya dataclass tipine otomatik dönüştürülebilir.
- Time travel, interrupt ve subgraph senaryolarında geri oynatma düzeltmeleri yapıldı.
- `version="v2"` isteğe bağlıdır; geriye dönük uyumluluk korunur.

## 10 Şubat 2026

### `deepagents` v0.4

- Takılabilir sandbox sistemleri için yeni paketler eklendi: `langchain-modal`, `langchain-daytona`, `langchain-runloop`.
- Konuşma geçmişi özetleme mekanizması model düğümüne taşındı ve `wrap_model_call` olayları ile çalışır hale getirildi.
- Token sayımı iyileştirildi.
- Bazı modellerde `ContextOverflowError` oluştuğunda özetleme otomatik tetiklenir.
- `"openai:"` önekiyle başlayan model dizgelerinde varsayılan olarak Responses API kullanılır.

## 15 Aralık 2025

### `langchain` v1.2.0

- `create_agent` için sağlayıcıya özgü araç parametreleri ve tanımları, araçlara eklenen yeni `extras` niteliği üzerinden sadeleştirildi.
- Ajan `response_format` alanında katı şema uyumu desteği eklendi.

## 8 Aralık 2025

### `langchain-google-genai` v4.0.0

Google GenAI entegrasyonu, Gemini API ve Vertex AI Platform'a aynı arayüzden erişim sunan birleşik Generative AI SDK ile yeniden yazıldı. Bazı kırıcı değişiklikler ve `langchain-google-vertexai` tarafında kullanım dışı bırakılan paketler bulunuyor.

## 25 Kasım 2025

### `langchain` v1.1.0

- Sohbet modelleri `.profile` niteliği üzerinden desteklenen yetenekleri açığa çıkarır.
- Özetleme middleware’i, model profilleri kullanarak esnek tetikleme noktalarını destekler.
- Yapılandırılmış çıktı tarafında `ProviderStrategy` çıkarımı model profilleri üzerinden yapılabilir.
- `create_agent` içinde `system_prompt` parametresine doğrudan `SystemMessage` geçme desteği eklendi.
- Başarısız model çağrıları için üstel geri çekilmeli yeni retry middleware’i eklendi.
- Güvensiz içeriği algılamak için içerik moderasyon middleware’i eklendi.

## 20 Ekim 2025

### v1.0.0

#### `langchain`

- Resmi sürüm notları ve geçiş kılavuzu yayımlandı.

#### `langgraph`

- Resmi sürüm notları ve geçiş kılavuzu yayımlandı.

Herhangi bir sorunla karşılaşırsanız veya geri bildiriminiz varsa resmi issue açılması önerilir. v0.x dokümantasyonu için arşivlenmiş içerik ve eski API referansı kullanılabilir.
