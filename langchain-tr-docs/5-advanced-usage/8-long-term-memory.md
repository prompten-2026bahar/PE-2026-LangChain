# Uzun Süreli Bellek

## Genel Bakış

LangChain ajanları, uzun süreli belleği etkinleştirmek için [LangGraph persistence](/oss/python/langgraph/persistence#memory-store) yapısını kullanır. Bu daha ileri düzey bir konudur ve LangGraph bilgisi gerektirir.

## Bellek depolama

LangGraph, uzun süreli anıları bir [store](/oss/python/langgraph/persistence#memory-store) içinde JSON belgeleri olarak saklar.

Her kayıt:

- özel bir `namespace` altında gruplanır
- benzersiz bir `key` ile tutulur

Bu yapı, kullanıcı kimliği, organizasyon kimliği veya başka etiketlerle hiyerarşik düzenleme yapmayı kolaylaştırır. İçerik filtreleriyle namespace'ler arası arama da desteklenir.

```python
from langgraph.store.memory import InMemoryStore

def embed(texts: list[str]) -> list[list[float]]:
    return [[1.0, 2.0] * len(texts)]

store = InMemoryStore(index={"embed": embed, "dims": 2})
user_id = "my-user"
application_context = "chitchat"
namespace = (user_id, application_context)
store.put(
    namespace,
    "a-memory",
    {
        "rules": [
            "User likes short, direct language",
            "User only speaks English & python",
        ],
        "my-key": "my-value",
    },
)
```

## Araçlar içinde uzun süreli belleği okuma

Ajanın kullanabileceği bir araç, kullanıcı bilgilerini mağazadan okuyabilir:

```python
@tool
def get_user_info(runtime: ToolRuntime[Context]) -> str:
    store = runtime.store
    user_id = runtime.context.user_id
    user_info = store.get(("users",), user_id)
    return str(user_info.value) if user_info else "Unknown user"
```

Bu yaklaşımda `store`, `create_agent` içine verilir ve araçlar çalışma anında aynı mağazaya erişir.

## Araçlar içinden uzun süreli belleğe yazma

Araçlar, kullanıcıya ait bilgileri mağazaya da yazabilir:

```python
@tool
def save_user_info(user_info: UserInfo, runtime: ToolRuntime[Context]) -> str:
    store = runtime.store
    user_id = runtime.context.user_id
    store.put(("users",), user_id, user_info)
    return "Successfully saved user info."
```

Bu sayede sohbet tabanlı uygulamalar, kullanıcı tercihlerini veya profil bilgisini zaman içinde kalıcı olarak saklayabilir.
