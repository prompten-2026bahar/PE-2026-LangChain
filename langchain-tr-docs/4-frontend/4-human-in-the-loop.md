# Human-in-the-Loop

Her ajan eylemi gözetimsiz çalışmamalıdır. Ajan bir e-posta göndermeden, kayıt silmeden, finansal işlem gerçekleştirmeden veya geri döndürülemez bir operasyon yapmadan önce insan onayı gerekebilir. Human-in-the-Loop (HITL) deseni, ajanın duraklayıp bekleyen eylemi kullanıcıya göstermesine ve yalnızca onay geldikten sonra devam etmesine olanak tanır.

## Interrupt mekanizması nasıl çalışır?

LangGraph ajanları **interrupt** noktalarını destekler. Ajan bu noktaya geldiğinde:

1. yürütme durur ve bir interrupt yükü üretir
2. `useStream`, bu veriyi `stream.interrupt` üzerinden açığa çıkarır
3. UI, onay / red / düzenleme seçenekleri sunan inceleme kartı gösterir
4. kullanıcı karar verir
5. kod, `stream.submit()` ile resume komutu yollar
6. ajan kaldığı yerden devam eder

## HITL için `useStream` kurulumu

```tsx
export function Chat() {
  const stream = useStream<typeof myAgent>({
    apiUrl: AGENT_URL,
    assistantId: "human_in_the_loop",
  });
}
```

Interrupt varsa UI içinde onay kartı gösterilir:

```tsx
{interrupt && (
  <ApprovalCard
    interrupt={interrupt}
    onRespond={(response) =>
      stream.submit(null, { command: { resume: response } })
    }
  />
)}
```

## Interrupt payload yapısı

Bir duraklama anında `stream.interrupt`, aşağıdaki yapıya benzer bir `HITLRequest` taşır:

- `actionRequests`: ajanın yapmak istediği eylemler
- `reviewConfigs`: hangi kararların desteklendiği

Her action request:

- `action`
- `args`
- `description`

alanlarını içerebilir.

## Karar türleri

### Approve

Kullanıcı eylemi olduğu gibi onaylar.

### Reject

Kullanıcı eylemi reddeder ve isteğe bağlı bir gerekçe iletebilir.

### Edit

Kullanıcı, aracın argümanlarını değiştirip sonra devam ettirir.

## ApprovalCard bileşeni

İnceleme kartı tipik olarak:

- eylem açıklamasını
- argümanların JSON görünümünü
- onay / ret / düzenleme düğmelerini

gösterir.

`edit` modunda kullanıcı JSON argümanlarını düzenleyebilir; `reject` modunda ise gerekçe girebilir.

## Resume akışı

Kullanıcı karar verdikten sonra:

1. `stream.submit(null, { command: { resume: hitlResponse } })` çağrılır
2. komut LangGraph arka ucuna gider
3. ajan `HITLResponse` verisini alır
4. onay verilmişse işlem sürer
5. reddedilmişse gerekçe ile yeni karar verir
6. `interrupt` alanı tekrar `null` olur

## Yaygın kullanım alanları

- e-posta gönderme
- veritabanı yazma işlemleri
- para transferleri
- dosya silme
- harici API çağrıları

## Çoklu bekleyen eylemler

Bir interrupt, birden fazla `actionRequest` içerebilir. Bu durumda her eylem için ayrı kartlar gösterilir ve tüm kararlar toplanıp tek seferde resume edilir.
