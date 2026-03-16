# Short-term Memory

## Genel Bakış

Bellek, önceki etkileşimler hakkında bilgi hatırlayan sistemdir. Ajanlar için bellek kritiktir; çünkü önceki etkileşimleri hatırlamalarına, geri bildirimlerden öğrenmelerine ve kullanıcı tercihlerine uyum sağlamalarına yardımcı olur.

Short-term memory, tek bir thread veya konuşma içindeki önceki etkileşimleri hatırlatır.

Uzun konuşmalar, LLM'ler için sorun yaratır:

- tam geçmiş bağlam penceresine sığmayabilir
- bağlam sığsa bile model eski veya alakasız içerikle dikkat dağıtabilir
- gecikme ve maliyet artabilir

## Kullanım

Ajan düzeyinde kısa süreli bellek eklemek için `create_agent` içinde `checkpointer` verilmelidir:

```python
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver

agent = create_agent(
    "gpt-5",
    tools=[get_user_info],
    checkpointer=InMemorySaver(),
)
```

State, checkpointer aracılığıyla belleğe veya veritabanına yazılır ve aynı thread daha sonra devam ettirilebilir.

## Üretimde kullanım

Gerçek sistemlerde veritabanı destekli checkpointer kullanılmalıdır:

```python
from langgraph.checkpoint.postgres import PostgresSaver
```

Postgres, SQLite ve Azure Cosmos DB gibi seçenekler mevcuttur.

## Belleği özelleştirme

Varsayılan olarak ajanlar kısa süreli belleği `AgentState` içindeki `messages` alanıyla yönetir. Ancak `state_schema` kullanarak özel alanlar ekleyebilirsiniz:

```python
class CustomAgentState(AgentState):
    user_id: str
    preferences: dict
```

## Yaygın stratejiler

Uzun konuşmaları bağlam sınırı içinde tutmak için üç temel yaklaşım kullanılır:

### Trim messages

Eski mesajların bir kısmı kırpılır ve yalnızca gerekli son mesajlar bırakılır.

### Delete messages

Belirli mesajlar veya tüm mesaj geçmişi kalıcı olarak LangGraph state içinden silinir.

### Summarize messages

Eski mesajlar özetlenir ve özet ile değiştirilir; böylece bilgi korunurken token tüketimi düşer.

Bu stratejiler, ajanın konuşma geçmişini korurken bağlam penceresini aşmamasına yardımcı olur.
