# Custom Middleware

Özel middleware, ajan yürütme akışının belirli noktalarında çalışan hook'lar yazarak oluşturulur.

## Hook türleri

Middleware iki temel hook stili sunar:

- **Node-style hooks**
- **Wrap-style hooks**

### Node-style hooks

Belirli yürütme noktalarında sırayla çalışır. Loglama, doğrulama ve state güncellemeleri için uygundur.

Kullanılabilir hook'lar:

- `before_agent`
- `before_model`
- `after_model`
- `after_agent`

Örnek:

```python
@before_model(can_jump_to=["end"])
def check_message_limit(state: AgentState, runtime: Runtime) -> dict[str, Any] | None:
    if len(state["messages"]) >= 50:
        return {
            "messages": [AIMessage("Conversation limit reached.")],
            "jump_to": "end"
        }
    return None
```

### Wrap-style hooks

Model veya araç çağrılarının etrafında çalışır. Handler'ı:

- hiç çağırmayabilir
- bir kez çağırabilir
- birden çok kez çağırabilir

Bu yapı retry, cache ve dönüştürme işlemleri için uygundur.

Kullanılabilir hook'lar:

- `wrap_model_call`
- `wrap_tool_call`

Örnek retry middleware:

```python
@wrap_model_call
def retry_model(request: ModelRequest, handler) -> ModelResponse:
    for attempt in range(3):
        try:
            return handler(request)
        except Exception:
            if attempt == 2:
                raise
```

## State güncellemeleri

Her iki hook stili de ajan durumunu güncelleyebilir.

### Node-style güncelleme

Node-style hook, doğrudan bir dict döndürür. Bu sözlükteki alanlar ajan state'ine reducer'lar üzerinden eklenir.

```python
@after_model(state_schema=TrackingState)
def increment_after_model(state: TrackingState, runtime: Runtime) -> dict[str, Any] | None:
    return {"model_call_count": state.get("model_call_count", 0) + 1}
```

### Wrap-style güncelleme

`wrap_model_call`, `ExtendedModelResponse` ve `Command` kullanarak state'e ek güncelleme enjekte edebilir:

```python
return ExtendedModelResponse(
    model_response=response,
    command=Command(update={"last_model_call_tokens": 150}),
)
```

Bu yapı özellikle:

- token kullanımını izleme
- özetleme tetikleyicileri
- usage metadata kaydetme
- özel hesaplanmış alanları state'e yazma

gibi durumlarda faydalıdır.

## Çoklu middleware katmanları

Birden fazla middleware birlikte kullanıldığında:

- komutlar reducer'lar üzerinden birleşir
- çakışan reducer olmayan alanlarda dıştaki middleware kazanır
- retry mantığında önceki başarısız denemelerin komutları atılabilir

Bu sayede hem basit hem de gelişmiş middleware kompozisyonları güvenli biçimde kurulabilir.
