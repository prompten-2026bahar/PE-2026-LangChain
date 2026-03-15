# Structured Output

Structured output, ajanın düz metin yerine tipli ve makine tarafından okunabilir veri döndürmesini sağlar. Böylece tek bir string göstermek yerine kartlar, tablolar, grafikler veya alan özel bileşenlerle işlenebilecek yapılandırılmış nesneler elde edersiniz.

## Structured output nedir?

Ajan serbest biçimli metin üretmek yerine, önceden tanımlanmış bir şemaya uyan yapılandırılmış nesneyi bir tool call üzerinden döndürür. Bunun avantajları:

- tür güvenli veri
- render üzerinde hassas kontrol
- modelden bağımsız tutarlı çıktı biçimi

Tool call burada gerçek iş mantığı çalıştırmak için değil, tipli veriyi taşımak için kullanılır.

## Kullanım alanları

- ürün karşılaştırmaları
- veri analizi özetleri
- adım adım kılavuzlar
- tarifler
- matematik ve bilim içerikleri
- seyahat planları

## Şema tanımlama

Örneğin bir tarif asistanı için:

```ts
interface Recipe {
  title: string;
  description: string;
  servings: number;
  ingredients: Ingredient[];
  steps: RecipeStep[];
  totalTime: string;
}
```

Şemanın biçimi, UI'nin nasıl çizileceğini doğrudan belirler.

## Mesajlardan structured output çıkarma

Genellikle son `AIMessage` içindeki ilk `tool_call.args` alanı okunur:

```ts
function extractStructuredOutput<T>(messages: any[]): T | null {
  const aiMessages = messages.filter(AIMessage.isInstance);
  if (aiMessages.length === 0) return null;

  const lastAI = aiMessages[aiMessages.length - 1];
  const toolCall = lastAI.tool_calls?.[0];
  if (!toolCall) return null;

  return toolCall.args as T;
}
```

## `useStream` ile kurulum

```tsx
const stream = useStream<typeof myAgent>({
  apiUrl: "http://localhost:2024",
  assistantId: "recipe_assistant",
});
```

## Yapılandırılmış veriyi render etme

Veri çekildikten sonra her alan uygun UI bileşeniyle eşleştirilir:

- metinler için paragraf / başlık
- sayılar için stat kartları
- diziler için liste / tablo
- iç içe nesneler için kart veya accordion
- markdown için markdown renderer
- formüller için KaTeX veya MathJax

## Kısmi akış verisini ele alma

Akış sırasında `tool_call.args` tamamlanmamış olabilir. Bu yüzden zorunlu alanların dolu olup olmadığını kontrol etmek gerekir.

```ts
const recipe = extractStructuredOutput<Recipe>(stream.messages, [
  "title",
  "ingredients",
  "steps",
]);
```

## Kademeli render

Tüm veri gelene kadar beklemek yerine alanlar geldikçe kartı parça parça doldurmak daha iyi kullanıcı deneyimi sağlar. Özellikle başlık, açıklama ve detayların doğal sırayla aktığı şemalarda bu yaklaşım iyi çalışır.
