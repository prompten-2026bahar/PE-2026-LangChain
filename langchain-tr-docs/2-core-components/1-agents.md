# Agents

Ajanlar, görevler üzerinde akıl yürütebilen, hangi araçların kullanılacağına karar verebilen ve çözüme doğru yinelemeli biçimde ilerleyebilen sistemler oluşturmak için dil modellerini araçlarla birleştirir.

[`create_agent`](https://reference.langchain.com/python/langchain/agents/factory/create_agent), üretime hazır bir ajan uygulaması sağlar. Bir LLM ajanı, bir hedefe ulaşmak için araçları döngü içinde çalıştırır. Ajan, model son çıktıyı ürettiğinde ya da yineleme sınırına ulaşıldığında durur.

`create_agent`, LangGraph kullanarak grafik tabanlı bir ajan çalışma zamanı oluşturur. Grafik; düğümlerden ve kenarlardan oluşur. Ajan bu grafik üzerinde ilerler ve model düğümü, araçlar düğümü veya middleware gibi parçaları yürütür.

## Temel bileşenler

### Model

Model, ajanın akıl yürütme motorudur. Statik ya da dinamik şekilde belirtilebilir.

#### Statik model

Statik modeller, ajan oluşturulurken bir kez yapılandırılır ve yürütme boyunca değişmez. En yaygın ve en yalın yaklaşım budur.

```python
from langchain.agents import create_agent

agent = create_agent("openai:gpt-5", tools=tools)
```

Model tanımlayıcı dizgeleri otomatik çıkarımı destekler. Örneğin `"gpt-5"`, `"openai:gpt-5"` olarak yorumlanır.

Daha ayrıntılı yapılandırma gerekiyorsa sağlayıcı paketleri üzerinden doğrudan model nesnesi başlatılabilir:

```python
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI

model = ChatOpenAI(
    model="gpt-5",
    temperature=0.1,
    max_tokens=1000,
    timeout=30
)
agent = create_agent(model, tools=tools)
```

#### Dinamik model

Dinamik modeller, mevcut durum ve bağlama göre çalışma zamanında seçilir. Bu, daha gelişmiş yönlendirme mantıkları ve maliyet optimizasyonu sağlar.

```python
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langchain.agents.middleware import wrap_model_call, ModelRequest, ModelResponse

basic_model = ChatOpenAI(model="gpt-4.1-mini")
advanced_model = ChatOpenAI(model="gpt-4.1")

@wrap_model_call
def dynamic_model_selection(request: ModelRequest, handler) -> ModelResponse:
    message_count = len(request.state["messages"])

    if message_count > 10:
        model = advanced_model
    else:
        model = basic_model

    return handler(request.override(model=model))

agent = create_agent(
    model=basic_model,
    tools=tools,
    middleware=[dynamic_model_selection]
)
```

### Tools

Araçlar, ajanların harici sistemlerle etkileşime geçmesini sağlar. Dil modeli, uygun olduğunda bir aracı çağırır ve sonuçları sonrasında yeniden kullanır.

### Middleware

Middleware, model çağrıları, araç yürütmeleri ya da ajan döngüsünün başka aşamalarına kanca atarak davranışı özelleştirmenizi sağlar.

### State

Ajan durumu, konuşma geçmişi, ara sonuçlar ve middleware tarafından kullanılan ek alanlar gibi yürütme boyunca taşınan verileri içerir.
