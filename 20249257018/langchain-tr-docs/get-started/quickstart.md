# Hızlı Başlangıç

Bu hızlı başlangıç rehberi, yalnızca birkaç dakika içinde basit bir kurulumdan tam işlevsel bir yapay zeka ajanına geçmenizi sağlar.

## LangChain Docs MCP sunucusu

Bir yapay zeka kodlama asistanı veya IDE kullanıyorsanız (örneğin Claude Code ya da Cursor), en iyi verimi almak için LangChain Docs MCP sunucusunu kurmalısınız. Bu sayede ajanınız güncel LangChain dokümantasyonuna ve örneklere erişebilir.

## Gereksinimler

Bu örnekler için şunlara ihtiyacınız olacak:

- LangChain paketini kurmak
- Bir Claude (Anthropic) hesabı oluşturmak ve API anahtarı almak
- Terminalinizde `ANTHROPIC_API_KEY` ortam değişkenini ayarlamak

Bu örneklerde Claude kullanılsa da, kod içindeki model adını değiştirip uygun API anahtarını ayarlayarak desteklenen herhangi bir modeli kullanabilirsiniz.

## Basit bir ajan oluşturma

Önce soruları yanıtlayabilen ve araç çağırabilen basit bir ajan oluşturarak başlayın. Ajan, dil modeli olarak Claude Sonnet 4.6'yı, araç olarak temel bir hava durumu fonksiyonunu ve davranışını yönlendirmek için basit bir istemi kullanacaktır.

```python
from langchain.agents import create_agent

def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"

agent = create_agent(
    model="claude-sonnet-4-6",
    tools=[get_weather],
    system_prompt="You are a helpful assistant",
)

# Run the agent
agent.invoke(
    {"messages": [{"role": "user", "content": "what is the weather in sf"}]}
)
```

Ajanınızı LangSmith ile nasıl izleyebileceğinizi öğrenmek için LangSmith dokümantasyonuna bakın.

## Gerçek dünyaya uygun bir ajan oluşturma

Şimdi üretim ortamına daha yakın bir hava tahmini ajanı oluşturalım. Bu örnek aşağıdaki temel kavramları gösterir:

1. Daha iyi ajan davranışı için ayrıntılı sistem istemleri
2. Harici verilerle entegre çalışan araçlar oluşturma
3. Tutarlı yanıtlar için model yapılandırması
4. Öngörülebilir sonuçlar için yapılandırılmış çıktı
5. Sohbet benzeri etkileşimler için konuşma belleği
6. Tam işlevli ajanı oluşturup çalıştırma

Şimdi her adımı tek tek inceleyelim.

### 1. Sistem istemini tanımlama

Sistem istemi, ajanınızın rolünü ve davranışını tanımlar. Bunu belirgin ve uygulanabilir şekilde yazın:

```python
SYSTEM_PROMPT = """You are an expert weather forecaster, who speaks in puns.

You have access to two tools:

- get_weather_for_location: use this to get the weather for a specific location
- get_user_location: use this to get the user's location
If a user asks you for the weather, make sure you know the location. If you can tell from the question that they mean wherever they are, use the get_user_location tool to find their location."""
```

### 2. Araçları oluşturma

Araçlar, sizin tanımladığınız fonksiyonları çağırarak modelin harici sistemlerle etkileşim kurmasını sağlar. Araçlar çalışma zamanı bağlamına bağlı olabilir ve ajan belleğiyle de etkileşim kurabilir. Aşağıda `get_user_location` aracının çalışma zamanı bağlamını nasıl kullandığına dikkat edin:

```python
from dataclasses import dataclass
from langchain.tools import tool, ToolRuntime

@tool
def get_weather_for_location(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"

@dataclass
class Context:
    """Custom runtime context schema."""
    user_id: str

@tool
def get_user_location(runtime: ToolRuntime[Context]) -> str:
    """Retrieve user information based on user ID."""
    user_id = runtime.context.user_id
    return "Florida" if user_id == "1" else "SF"
```

Araçlar iyi belgelenmiş olmalıdır; adları, açıklamaları ve argüman adları model isteminin bir parçası haline gelir. LangChain'in `@tool` dekoratörü meta veri ekler ve `ToolRuntime` parametresiyle çalışma zamanı enjeksiyonunu etkinleştirir.

### 3. Modelinizi yapılandırma

Kullanım senaryonuza uygun parametrelerle dil modelinizi ayarlayın:

```python
from langchain.chat_models import init_chat_model

model = init_chat_model(
    "claude-sonnet-4-6",
    temperature=0.5,
    timeout=10,
    max_tokens=1000
)
```

Seçilen model ve sağlayıcıya bağlı olarak başlatma parametreleri değişebilir; ayrıntılar için ilgili referans sayfalarına bakın.

### 4. Yanıt biçimini tanımlama

Ajan yanıtlarının belirli bir şemaya uymasını istiyorsanız isteğe bağlı olarak yapılandırılmış bir yanıt biçimi tanımlayın.

```python
from dataclasses import dataclass

@dataclass
class ResponseFormat:
    """Response schema for the agent."""
    punny_response: str
    weather_conditions: str | None = None
```

### 5. Bellek ekleme

Etkileşimler arasında durumu korumak için ajanınıza bellek ekleyin. Bu, ajanın önceki konuşmaları ve bağlamı hatırlamasını sağlar.

```python
from langgraph.checkpoint.memory import InMemorySaver

checkpointer = InMemorySaver()
```

Üretimde, mesaj geçmişini bir veritabanına kaydeden kalıcı bir checkpointer kullanın. Daha fazla ayrıntı için bellek ekleme ve yönetme dokümanına bakın.

### 6. Ajanı oluşturma ve çalıştırma

Şimdi tüm bileşenleri bir araya getirip ajanınızı çalıştırın.

```python
from langchain.agents.structured_output import ToolStrategy

agent = create_agent(
    model=model,
    system_prompt=SYSTEM_PROMPT,
    tools=[get_user_location, get_weather_for_location],
    context_schema=Context,
    response_format=ToolStrategy(ResponseFormat),
    checkpointer=checkpointer
)
```

Tebrikler. Artık bağlamı anlayan, araç kullanan, yapılandırılmış yanıt üreten ve konuşma durumunu koruyan bir yapay zeka ajanınız var.
