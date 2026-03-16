# Markdown Messages

LLM'ler doğal olarak başlıklar, listeler, kod blokları, tablolar ve satır içi biçimlendirme içeren markdown çıktısı üretir. Bu içeriği düz metin olarak göstermek, modelin sağladığı yapıyı boşa harcar. Bu desen, markdown içeriğini ajan akışı sırasında gerçek zamanlı olarak ayrıştırıp göstermeyi açıklar.

## Markdown render akışı nasıl çalışır?

İşlem hattı üç adımdan oluşur:

1. **Receive**: `useStream`, akışla gelen metni her AI mesajındaki `msg.text` alanında biriktirir.
2. **Parse**: Markdown ayrıştırıcı, ham metni HTML'e veya bileşen ağacına dönüştürür.
3. **Render**: Ayrıştırılmış çıktı DOM'a basılır.

## `useStream` kurulumu

Bu desen özel bir ajan yapılandırması gerektirmez. Ajan URL'i ve assistant kimliğiyle `useStream` bağlanır.

```ts
import type { BaseMessage } from "@langchain/core/messages";

interface AgentState {
  messages: BaseMessage[];
}
```

React örneği:

```tsx
import { useStream } from "@langchain/react";
import { AIMessage, HumanMessage } from "@langchain/core/messages";

const AGENT_URL = "http://localhost:2024";

export function Chat() {
  const stream = useStream<typeof myAgent>({
    apiUrl: AGENT_URL,
    assistantId: "simple_agent",
  });
}
```

## Markdown kütüphanesi seçimi

Önerilen eşleştirmeler:

- React: `react-markdown` + `remark-gfm`
- Vue: `marked` + `dompurify`
- Svelte: `marked` + `dompurify`
- Angular: `marked` + `dompurify`

React tarafında ham HTML enjekte edilmediği için `dompurify` gerekmez. Vue, Svelte ve Angular tarafında ise üretilen HTML mutlaka sanitize edilmelidir.

## Markdown bileşeni oluşturma

```tsx
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

export function Markdown({ children }: { children: string }) {
  return (
    <div className="markdown-content">
      <ReactMarkdown remarkPlugins={[remarkGfm]}>
        {children}
      </ReactMarkdown>
    </div>
  );
}
```

## HTML çıktısını sanitize etme

Ham HTML render ediliyorsa XSS riskini önlemek için `dompurify` kullanılmalıdır:

```ts
import DOMPurify from "dompurify";

const safeHtml = DOMPurify.sanitize(rawHtml);
```

`DOMPurify`; `<script>` etiketlerini, `onclick` niteliklerini, `javascript:` URL'lerini ve diğer XSS vektörlerini temizler.

## Akış sırasında performans

`useStream`, her yeni token geldiğinde `msg.text` alanını günceller. Tipik sohbet uzunluklarında bu yaklaşım yeterince hızlıdır. Çok uzun yanıtlar için şu optimizasyonlar düşünülebilir:

- render'ları `requestAnimationFrame` ile sınırlamak
- artımlı ayrıştırma uygulamak

## Stil verme

`.markdown-content` sınıfına paragraf, liste, kod bloğu, tablo ve alıntı stilleri tanımlanır. Sohbet baloncukları blog yazısından küçük olduğu için marj ve font boyutları daha sıkı tutulmalıdır.

## En iyi uygulamalar

- Ham HTML kullanılıyorsa mutlaka sanitize edin
- GitHub Flavored Markdown desteğini açın
- Boş içerikleri ayrıştırmadan önce kontrol edin
- Tek satırlık yeni satırları görünür yapmak için `breaks: true` kullanın
- Stilleri sohbet bağlamına uygun tutun
- Zengin içerikle test edin
