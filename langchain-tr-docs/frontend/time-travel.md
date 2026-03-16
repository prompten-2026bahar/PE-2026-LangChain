# Time Travel

LangGraph ajanında her durum değişimi bir **checkpoint** üretir. Time travel, bu checkpoint'lerin herhangi birini incelemenizi, ajanın o anda tuttuğu tam durumu görmenizi ve isterseniz tam o noktadan yürütmeyi yeniden başlatmanızı sağlar.

Bu desen hem hata ayıklama aracı, hem geri alma düğmesi, hem de denetim kaydı gibi çalışır.

Bu özellik için [LangGraph Agent Server](/langsmith/local-server) gerekir.

## Checkpoint'ler nasıl çalışır?

LangGraph, her düğüm yürütmesinden sonra ajan durumunu saklar. Her `ThreadState` girdisi şunları içerir:

- `checkpoint`: bu anlık görüntünün kimlik bilgisi
- `values`: tam ajan durumu
- `tasks`: o anda çalışan veya planlanan düğümler
- `next`: sıradaki düğüm adları

Bu sayede ajan kararlarının tamamı zaman çizelgesi halinde elde edilir.

## `useStream` kurulumu

Checkpoint geçmişini almak için `fetchStateHistory: true` verilmelidir:

```tsx
const stream = useStream<typeof myAgent>({
  apiUrl: AGENT_URL,
  assistantId: "time_travel",
  fetchStateHistory: true,
});
```

## Zaman çizelgesi

`stream.history`, checkpoint'lerin listesini döndürür. Arayüzde bunlar tıklanabilir bir yan panel olarak gösterilebilir. Her girişte:

- hangi düğümün çalıştığı
- kaç mesaj olduğu
- varsa interrupt bilgisi

gibi özetler sunulabilir.

## Checkpoint durumunu inceleme

Bir checkpoint seçildiğinde, o andaki `values` JSON biçiminde gösterilebilir. Bu, ajanın o an ne bildiğini ve hangi kararı verdiğini görmeyi kolaylaştırır.

## Checkpoint'ten devam etme

Asıl zaman yolculuğu davranışı, herhangi bir eski checkpoint'ten tekrar yürütme başlatabilmektir:

```tsx
stream.submit(null, { checkpoint: selectedCheckpoint.checkpoint });
```

Bu çağrı:

1. ajanı seçilen checkpoint durumuna geri sarar
2. grafiği o noktadan tekrar çalıştırır
3. yeni sonucu istemciye akıtır

Bu süreç eski zaman çizelgesini silmez; sadece yeni bir dal üretir.

## Split view düzeni

En uygun UI genellikle:

- solda ana sohbet alanı
- sağda checkpoint zaman çizelgesi ve denetleyici

şeklindedir.

## Kullanım alanları

- ajan davranışını hata ayıklama
- yanlış gidişi geri alma
- alternatif yolları deneme
- denetim ve uyumluluk incelemeleri
- eğitim ve adım adım gösterim
