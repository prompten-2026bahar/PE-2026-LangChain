# Unit Testing

Unit test'ler, ajanın küçük ve deterministik parçalarını izole biçimde test eder. Gerçek LLM yerine bellek içi bir sahte model kullanılarak tam olarak hangi yanıtların döneceği kontrol edilir; böylece testler hızlı, ücretsiz ve tekrarlanabilir olur.

## Sahte chat modeli

LangChain, metin yanıtlarını taklit etmek için `GenericFakeChatModel` sağlar:

```python
from langchain_core.language_models.fake_chat_models import GenericFakeChatModel

model = GenericFakeChatModel(messages=iter([
    AIMessage(content="", tool_calls=[ToolCall(name="foo", args={"bar": "baz"}, id="call_1")]),
    "bar"
]))
```

Bu sahte model, her çağrıda sıradaki yanıtı döndürür. Böylece:

- tool call davranışı
- metin çıktısı
- hata durumları

tam olarak kontrol edilebilir.

## `InMemorySaver` checkpointer

Test sırasında kalıcılık eklemek için `InMemorySaver` kullanılabilir:

```python
from langgraph.checkpoint.memory import InMemorySaver

agent = create_agent(
    model,
    tools=[],
    checkpointer=InMemorySaver()
)
```

Bu yapı, aynı `thread_id` ile çok turlu testler yapmaya ve state'e bağlı davranışları doğrulamaya izin verir.

## Sonraki adım

Gerçek model sağlayıcılarıyla test yapmak için bir sonraki adım `integration-testing.md` sayfasıdır.
