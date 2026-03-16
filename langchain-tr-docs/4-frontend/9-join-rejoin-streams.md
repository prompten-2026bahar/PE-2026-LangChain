# Join & Rejoin Streams

Join and rejoin deseni, çalışan bir ajan akışından istemciyi koparıp ajanı durdurmadan daha sonra aynı akışa tekrar bağlanmanıza izin verir. İstemci ayrıldığında ajan sunucu tarafında çalışmaya devam eder.

Bu desen için [LangGraph Agent Server](/langsmith/local-server) gerekir.

## Neden gerekli?

Bu yaklaşım şu senaryolarda yararlıdır:

- ağ kesintileri
- kullanıcı sayfadan ayrılıp geri döndüğünde
- mobil uygulama arka plana alındığında
- dakikalar süren uzun işlemlerde
- çok cihazlı devam senaryolarında

## Temel kavramlar

- `stream.stop()`: istemciyi akıştan ayırır ama ajanı durdurmaz
- `stream.joinStream(runId)`: mevcut akışa `runId` ile yeniden bağlanır
- `onDisconnect: "continue"`: istemci ayrılsa da ajan çalışmaya devam eder
- `streamResumable: true`: akışın daha sonra yeniden bağlanabilir olmasını sağlar

`stream.stop()` gerçek bir iptal değildir; sadece istemci bağlantısını keser.

## `useStream` kurulumu

Yeniden bağlanmak için `run_id` değeri `onCreated` geri çağrımıyla saklanmalıdır:

```tsx
const stream = useStream<typeof myAgent>({
  apiUrl: "http://localhost:2024",
  assistantId: "join_rejoin",
  onCreated(run) {
    setSavedRunId(run.run_id);
  },
});
```

## Yeniden bağlanabilir seçeneklerle gönderim

```tsx
stream.submit(
  { messages: [{ type: "human", content: text }] },
  {
    onDisconnect: "continue",
    streamResumable: true,
  }
);
```

Bu iki seçenek birlikte kullanılmalıdır. Aksi halde ajan çalışmaya devam etse bile akışa sonradan bağlanamazsınız.

## Akıştan ayrılma

```ts
stream.stop();
```

Bundan sonra:

- `stream.isLoading` false olur
- o ana kadar gelen mesajlar korunur
- ajan sunucuda çalışmaya devam eder

## Akışa yeniden katılma

```ts
stream.joinStream(savedRunId);
```

Yeniden bağlandıktan sonra:

- istemci tekrar canlı güncellemeleri alır
- bağlantı kesikken üretilen mesajlar teslim edilir
- ajan bitmişse son durum hemen döner

## Durum göstergesi ve kontrol düğmeleri

Kullanıcıların bağlı olup olmadığını anlaması için bağlantı durumu göstergesi ve `Disconnect` / `Rejoin` düğmeleri sunulmalıdır.

## `run_id` kalıcılığı

Tarayıcı kapanıp geri açıldığında da devam etmek için `run_id`, `localStorage` gibi bir depoya yazılabilir. İşlem tamamlandığında ise temizlenmelidir.

## Hata yönetimi

Run süresi dolmuş, silinmiş ya da sunucu yeniden başlatılmış olabilir. Bu durumda `joinStream` hatası yakalanmalı, saklanan `run_id` temizlenmeli ve kullanıcı bilgilendirilmelidir.
