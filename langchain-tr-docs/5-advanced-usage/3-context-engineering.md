# Context Engineering

Güvenilir ajanlar geliştirmenin zor kısmı, onları yeterince güvenilir hale getirmektir. Çoğu zaman problem modelin yeteneksiz olması değil, modele **doğru bağlamın doğru biçimde verilmemesidir**.

Context engineering, LLM'in görevi başarıyla yapabilmesi için doğru bilgi ve araçları doğru formatta sağlamaktır. Dokümana göre bu, AI mühendislerinin en önemli işidir.

## Ajanlar neden başarısız olur?

Genellikle iki temel neden vardır:

1. Kullanılan LLM yeterince güçlü değildir
2. LLM'e doğru bağlam verilmemiştir

Pratikte en sık ikinci sebep sorun yaratır.

## Agent loop

Tipik ajan döngüsü iki ana adımdan oluşur:

1. **Model call**: LLM, istem ve araçlarla çağrılır
2. **Tool execution**: Modelin istediği araçlar çalıştırılır

Bu döngü model bitirme kararı verene kadar sürer.

## Neyi kontrol edebilirsiniz?

Belge üç tür bağlamı ayırır:

- **Model Context**: modele hangi istem, mesaj, araç, model ve çıktı biçiminin verildiği
- **Tool Context**: araçların hangi state, store ve runtime verisine erişebildiği
- **Life-cycle Context**: model ve araç çağrıları arasında gerçekleşen özetleme, guardrail, loglama gibi davranışlar

## Geçici ve kalıcı bağlam

- **Transient context**: tek bir model çağrısında LLM'in gördüğü bağlam
- **Persistent context**: state içinde kalıcı olarak saklanan bağlam

## Veri kaynakları

Context engineering boyunca ajan şu veri kaynaklarına erişir:

- **Runtime Context**: kullanıcı kimliği, API anahtarı, ortam ayarı gibi sabit çalışma zamanı bilgileri
- **State**: kısa süreli bellek; mesaj geçmişi, tool sonuçları, özel alanlar
- **Store**: uzun süreli bellek; kullanıcı tercihleri, geçmiş bilgiler, kalıcı kayıtlar

## Middleware ile context engineering

LangChain'de context engineering'i pratik hale getiren mekanizma middleware'dir. Middleware sayesinde ajan yaşam döngüsünün farklı noktalarında:

- bağlam güncellenebilir
- farklı adıma sıçranabilir

## Model context

Her model çağrısına giren şeyleri kontrol eder:

- sistem istemi
- mesajlar
- araçlar
- model seçimi
- response format

### System prompt

Sistem istemi, model davranışını belirler. Konuşmanın uzunluğu, kullanıcı rolü veya kullanıcı tercihlerine göre dinamik prompt üretilebilir.

### Messages

Mesaj geçmişi, modele gönderilen prompt'un ana gövdesini oluşturur. Yüklenen dosyalar, önceki tool sonuçları veya store bilgileri gerektiğinde mesaja enjekte edilebilir.

### Tools

Araçların sayısı, açıklamaları ve kullanılabilirliği, modelin karar kalitesini doğrudan etkiler.

### Model

Konuşma bağlamına göre farklı model seçmek maliyet ve kalite dengesini kurmak için önemlidir.

### Response format

Beklenen yanıt şemasını açık tanımlamak, çıktı güvenilirliğini artırır.

Özetle context engineering, ajanın gördüğü bağlamı kontrollü şekilde düzenleyerek güvenilirliği yükseltme işidir.
