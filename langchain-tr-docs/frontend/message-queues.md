# Message Queues

Mesaj kuyruğu, kullanıcıların ajanın mevcut işi bitirmesini beklemeden peş peşe birden fazla mesaj göndermesine izin verir. Her mesaj sunucu tarafında kuyruğa alınır ve sıralı biçimde işlenir.

Bu desen için [LangGraph Agent Server](/langsmith/local-server) gerekir. Yerelde `langgraph dev` ile çalıştırabilir veya LangSmith'e deploy edebilirsiniz.

## Neden mesaj kuyruğu?

Normal bir sohbet arayüzünde kullanıcı yeni mesaj göndermeden önce ajanın yanıtını bitirmesini bekler. Bu durum şu senaryolarda sürtünme yaratır:

- Toplu soru gönderme
- Ajan hâlâ çalışırken ek bağlam veya takip sorusu verme
- Otomatik test sekansları yürütme
- Yapılandırılmış veri giriş iş akışları

Mesaj kuyruğu tüm gönderimleri anında kabul eder ve sırayla işler.

## Nasıl çalışır?

LangGraph, eşzamanlı gönderimleri yönetmek için `multitaskStrategy: "enqueue"` kullanır. Ajan çalışırken yeni mesaj gelirse, mesaj sunucu tarafı kuyruğa eklenir. Mevcut çalıştırma bittiğinde sıradaki mesaj otomatik işlenir.

`useStream`, kuyruk durumunu `queue` özelliği üzerinden sunar:

- `queue.entries`: bekleyen tüm girişler
- `queue.size`: kuyruktaki öğe sayısı
- `queue.cancel(id)`: belirli bir girdiyi iptal eder
- `queue.clear()`: tüm kuyruğu temizler

Her `QueueEntry` şunları içerir:

- `id`
- `values`
- `options`
- `createdAt`

## `useStream` kurulumu

```ts
import type { BaseMessage } from "@langchain/core/messages";

interface AgentState {
  messages: BaseMessage[];
}
```

```tsx
import { useStream } from "@langchain/react";

function Chat() {
  const stream = useStream<typeof myAgent>({
    apiUrl: "http://localhost:2024",
    assistantId: "message_queue",
  });
}
```

## Kuyruğu gösterme

Kuyruktaki bekleyen mesajlar için ayrı bir panel oluşturulabilir. Her öğe için önizleme metni, zaman damgası ve iptal düğmesi gösterilir.

```tsx
function QueueList({ entries, queue }) {
  return (
    <div className="queue-panel">
      <div className="queue-header">
        <span>Queued messages ({entries.length})</span>
        <button onClick={() => queue.clear()}>Clear all</button>
      </div>
    </div>
  );
}
```

## Kuyruktaki mesajları iptal etme

### Tek bir girdiyi iptal etme

```ts
await queue.cancel(entryId);
```

### Tüm kuyruğu temizleme

```ts
await queue.clear();
```

Not: İptal işlemi yalnızca **henüz işlenmeye başlamamış** mesajlarda etkilidir. Ajan o mesaj üzerinde zaten çalışıyorsa `stream.stop()` ile mevcut çalıştırmayı durdurmanız gerekir.

## `onCreated` ile takip gönderimlerini zincirleme

Yeni bir run oluşturulduğunda `onCreated` geri çağırımı çalışır. Bu mekanizma, çok adımlı iş akışlarında takip sorularını programlı biçimde kuyruğa eklemek için kullanılabilir.

## Yeni bir thread başlatma

Kullanıcı yeni bir konuşma başlatmak istediğinde `switchThread(null)` çağrılır. Bu, mevcut geçmişi ve kuyruğu temizler.

## En iyi uygulamalar

- Kuyruk boyutunu sınırlayın
- Sıra numarasını gösterin
- Gönderim sonrası input odağını koruyun
- Geçişleri animasyonlu yapın
- Hataları sonraki kuyruk girdilerini bloke etmeden gösterin
- Programlı hızlı gönderimlerde küçük debounce kullanın
