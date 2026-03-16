# Branching Chat

Yapay zeka ajanlarıyla yapılan konuşmalar çoğu zaman doğrusal değildir. Kullanıcı eski bir soruyu yeniden yazmak, beğenmediği bir yanıtı tekrar üretmek ya da önceki işi kaybetmeden bambaşka bir konuşma yolunu denemek isteyebilir. Branching chat, sohbet arayüzüne sürüm kontrolü mantığı getirir.

Bu desen için [LangGraph Agent Server](/langsmith/local-server) gerekir.

## Branching chat nedir?

Bu modelde konuşma bir liste değil, bir ağaç olarak ele alınır. Her mesaj bir düğümdür. Bir mesajı düzenlemek veya bir AI yanıtını yeniden üretmek, o noktadan yeni bir **dal** oluşturur.

Temel yetenekler:

- herhangi bir kullanıcı mesajını düzenleme
- herhangi bir AI yanıtını yeniden üretme
- dallar arasında geçiş yapma

## `useStream` kurulumu

Dallanmayı etkinleştirmek için `fetchStateHistory: true` kullanılmalıdır:

```tsx
const stream = useStream<typeof myAgent>({
  apiUrl: AGENT_URL,
  assistantId: "branching_chat",
  fetchStateHistory: true,
});
```

## Mesaj metadata'sını anlama

`getMessagesMetadata(msg)` çağrısı her mesaj için dal bilgisi döndürür:

- `branch`: bu mesaj sürümünün dal kimliği
- `branchOptions`: o mesaj pozisyonu için mevcut tüm dal sürümleri
- `firstSeenState.parent_checkpoint`: düzenleme ve yeniden üretim için kullanılacak çatallanma noktası

## Mesaj düzenleme

Kullanıcı mesajını düzenlemek için:

1. metadata içinden `parent_checkpoint` alınır
2. düzenlenen mesaj o checkpoint ile tekrar gönderilir
3. ajan o noktadan itibaren yeniden çalışır ve yeni dal oluşur

## Yanıtı yeniden üretme

AI yanıtını yeniden üretmek için aynı checkpoint kullanılır; fakat yeni input verilmez:

```tsx
stream.submit(undefined, { checkpoint });
```

Bu yöntem özellikle deterministik olmayan, sıcaklık kullanan modellerde farklı alternatif yanıtlar üretmek için faydalıdır.

## Branch switcher

Bir mesajın birden fazla sürümü varsa küçük bir branch switcher bileşeni ile kullanıcı önceki/sonraki varyantlar arasında geçebilir.

`stream.setBranch(branchId)` çağrısı, görünümü seçilen dala geçirir. Bu yalnızca ilgili mesajı değil, o mesajdan sonraki tüm konuşma akışını değiştirir.

## Perde arkasında nasıl çalışır?

LangGraph her durum değişimini bir **checkpoint** olarak saklar. `checkpoint` parametresiyle submit edildiğinde, arka uç mevcut konuşmaya ek yapmak yerine o noktadan yeni bir dal çatallar.

Bu yapı sayesinde:

- eski sürümler silinmez
- farklı konuşma yolları korunur
- kullanıcı istediği zaman farklı dalları karşılaştırabilir
