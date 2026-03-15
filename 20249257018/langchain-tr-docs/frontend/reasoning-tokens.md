# Reasoning Tokens

Reasoning token'ları, OpenAI o1/o3 veya geniş düşünme destekli Anthropic Claude gibi gelişmiş modellerin içsel düşünme sürecini görünür kılar. Bu modeller, akıl yürütme ile son yanıtı ayıran yapılandırılmış içerik blokları üretir.

## Reasoning token nedir?

Akıl yürüten modeller genellikle iki içerik türü üretir:

1. **Reasoning blocks**: modelin iç düşünme zinciri, problemi parçalara ayırması ve adım adım analizi
2. **Text blocks**: kullanıcıya gösterilen son yanıt

Örnek yapı:

```ts
{ type: "reasoning", reasoning: "Let me think about this step by step..." }
{ type: "text", text: "The answer is 42." }
```

Her model reasoning token üretmez; bu desen yalnızca geniş düşünme veya chain-of-thought çıktısı destekleyen modeller için geçerlidir.

## Kullanım alanları

- Şeffaflık
- Hata ayıklama
- Eğitim araçları
- Karar destek sistemleri
- Düzenlemeye tabi alanlarda denetlenebilirlik

## Reasoning ve text bloklarını ayırma

`AIMessage.contentBlocks` içindeki bloklar `type` alanına göre filtrelenir:

```ts
function extractBlocks(msg: AIMessage) {
  const reasoningBlocks = msg.contentBlocks
    .filter((b) => b.type === "reasoning")
    .map((b) => b.reasoning);

  const textBlocks = msg.contentBlocks
    .filter((b) => b.type === "text")
    .map((b) => b.text);
}
```

Bir mesaj birden fazla reasoning bloğu içerebilir; bunlar birleştirilerek tam düşünme akışı elde edilir.

## `useStream` ile kullanma

`useStream`, mesaj dizisini reaktif şekilde sağlar ve son AI mesajı akış sırasında güncellenebilir.

```tsx
function Chat() {
  const stream = useStream<typeof myAgent>({
    apiUrl: "http://localhost:2024",
    assistantId: "reasoning",
  });
}
```

## ThinkingBubble bileşeni

Reasoning içeriği, açılıp kapanabilen ayrı bir kutuda gösterilir. Kullanıcı isterse düşünme sürecini açar, istemezse yalnızca son cevaba odaklanır.

```tsx
function ThinkingBubble({ reasoning, isStreaming }) {
  const [isExpanded, setIsExpanded] = useState(false);
}
```

Bu bileşende:

- akış devam ederken spinner gösterilebilir
- düşünme metni varsayılan olarak kapalı tutulabilir
- akış tamamlandıktan sonra önizleme veya tam içerik sunulabilir

## Stil önerileri

Reasoning alanı, normal mesajlardan görsel olarak ayrılmalıdır:

- farklı arka plan rengi
- ince sınır çizgisi
- okunabilir ama daha ikincil tipografi
- aç/kapat simgesi

## Akış göstergesi

Model reasoning üretmeye devam ederken animasyonlu bir gösterge kullanmak faydalıdır. Akış sırasında kutuyu varsayılan olarak kapalı tutmak, yeni token'lar geldikçe oluşabilecek düzen sıçramalarını azaltır.

## Tam AI yanıtı

İdeal yaklaşım, `ThinkingBubble` ile son metin çıktısını aynı `AIResponse` bileşeninde birleştirmektir. Böylece kullanıcı isterse düşünme zincirini, isterse sadece son cevabı görür.
