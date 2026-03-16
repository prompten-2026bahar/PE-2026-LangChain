# Generative UI

Generative UI, yapay zekanın doğal dil istemlerinden tam kullanıcı arayüzleri üretmesini sağlar. Bu modelde çıktı sohbet balonundaki metin değil; doğrudan form, kart, dashboard ve benzeri arayüz bileşenleridir.

Bu desen, bileşen kataloğu tanımlamak, yapay zekaya bu katalog üzerinden spec ürettirmek ve çıktıyı güvenli biçimde render etmek için [json-render](https://json-render.dev) kullanır.

## Nasıl çalışır?

1. **Katalog tanımla**: Yapay zekanın kullanabileceği bileşenleri ve tipli prop'larını belirt
2. **Yapay zekayı yönlendir**: Doğal dil ile istenen UI'yi tarif et
3. **Spec üret**: AI, bileşen ağacını anlatan JSON belge üretir
4. **Güvenli render et**: `Renderer`, bu spec'i gerçek bileşenlerle çizer

Katalog bir guardrail görevi görür; model yalnızca tanımladığınız bileşenleri ve şemaya uyan prop'ları kullanabilir.

## Bileşen kataloğu tanımlama

Her bileşen için açıklama ve Zod şeması verilir:

```ts
const catalog = defineCatalog(schema, {
  components: {
    Card: {
      description: "A card container with optional title and padding",
      props: z.object({
        title: z.string().optional(),
        padding: z.enum(["sm", "md", "lg"]).optional(),
      }),
    },
  },
  actions: {},
});
```

Katalog küçük ve odaklı tutulmalıdır; ihtiyacınız olmayan fazla bileşenler çıktıyı bozabilir.

## Component registry oluşturma

Registry, katalogdaki bileşenleri gerçek render implementasyonlarına bağlar:

```tsx
const { registry } = defineRegistry(catalog, {
  components: {
    Card: ({ props, children }) => <div className="card">{children}</div>,
  },
});
```

## Ajana bağlanma

Ajan, structured output kullanarak json-render spec döndürür. `useStream` ile akış kurulup AI mesajı içindeki `tool_calls` üzerinden spec çekilir.

## Akış sırasında kademeli render

Spec akışta parçalı gelir. Her eleman başlangıçta `type` veya `props` içermeyebilir. Bu yüzden yalnızca tamamlanmış elemanlar filtrelenmeli ve `Renderer` bileşenine `loading={true}` verilmelidir.

## Spec biçimi

Çıktı tipik olarak şu yapıyı taşır:

- `root`: kök elemanın kimliği
- `elements`: tüm bileşenlerin tutulduğu düz harita

Her eleman çocuklarını kimlikler üzerinden referanslar.

## En iyi uygulamalar

- Bileşen açıklamalarını açık yazın
- Render etmeden önce `type` ve `props` doğrulaması yapın
- Akışlı kullanım için kademeli render tasarlayın
- Tasarım token'ları ile tema uyumunu koruyun
- `Renderer` mutlaka `JSONUIProvider` içinde kullanılmalıdır
