# Frontend Genel Bakış

`createAgent` ile oluşturulan ajanlar için zengin ve etkileşimli ön yüzler geliştirebilirsiniz. Bu desenler, temel mesaj gösteriminden insan onayı ve zaman yolculuğu hata ayıklaması gibi ileri düzey iş akışlarına kadar uzanır.

## Mimari

Her desen aynı mimariyi izler: `createAgent` arka ucu, durumu `useStream` kancası üzerinden ön yüze aktarır.

Arka uçta `createAgent`, akış API'si sunan derlenmiş bir LangGraph grafiği üretir. Ön yüzde `useStream`, bu API'ye bağlanır ve mesajlar, araç çağrıları, kesintiler ve geçmiş dahil olmak üzere reaktif durumu sağlar; siz de bunu istediğiniz framework ile ekrana yansıtırsınız.

```python
from langchain import create_agent
from langgraph.checkpoint.memory import MemorySaver

agent = create_agent(
    model="openai:gpt-5.4",
    tools=[get_weather, search_web],
    checkpointer=MemorySaver(),
)
```

`useStream`; React, Vue, Svelte ve Angular için kullanılabilir.

## Desenler

### Mesajları ve çıktıyı gösterme

- Markdown mesajları
- Yapılandırılmış çıktı
- Akıl yürütme tokenları
- Üretken arayüz

### Ajan eylemlerini gösterme

- Araç çağırma
- İnsan sürece dahil

### Konuşmaları yönetme

- Dallanabilir sohbet
- Mesaj kuyrukları

### Gelişmiş akış

- Akışlara katılma ve yeniden katılma
- Zaman yolculuğu
