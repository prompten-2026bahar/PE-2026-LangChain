# Tools

Araçlar, [agents](/oss/python/langchain/agents) tarafının gerçek dünyayla etkileşim kurmasını sağlar. Böylece ajanlar anlık veri çekebilir, kod çalıştırabilir, dış veritabanlarını sorgulayabilir ve dış sistemlerde eylem gerçekleştirebilir.

Temelde araçlar; iyi tanımlanmış giriş ve çıkışlara sahip çağrılabilir fonksiyonlardır. Bu fonksiyonlar [chat model](/oss/python/langchain/models) tarafına verilir ve model, konuşma bağlamına göre hangi aracı ne zaman çağıracağına karar verir.

## Araç oluşturma

### Basit tanım

En kolay yöntem `@tool` dekoratörüdür:

```python
from langchain.tools import tool

@tool
def search_database(query: str, limit: int = 10) -> str:
    """Search the customer database for records matching the query."""
    return f"Found {limit} results for '{query}'"
```

Type hint zorunludur; çünkü input şemasını onlar belirler.

## Araç özelliklerini özelleştirme

### Özel araç adı

```python
@tool("web_search")
def search(query: str) -> str:
    """Search the web for information."""
```

### Özel açıklama

Araç açıklaması modele, aracı ne zaman kullanacağını anlatır. Bu yüzden açık ve kısa olmalıdır.

## Gelişmiş şema tanımı

Karmaşık girişler için Pydantic model ya da JSON Schema kullanılabilir:

```python
class WeatherInput(BaseModel):
    location: str
    units: Literal["celsius", "fahrenheit"] = "celsius"
```

## Ayrılmış parametre adları

Şu adlar araç argümanı olarak kullanılamaz:

- `config`
- `runtime`

Çünkü bunlar LangChain tarafından dahili amaçlarla ayrılmıştır.

## Bağlama erişim

Araçlar, [`ToolRuntime`] üzerinden çalışma zamanı verilerine erişebilir:

- **State**: kısa süreli bellek
- **Context**: immutable çalışma zamanı yapılandırması
- **Store**: uzun süreli bellek
- **Stream Writer**: uzun süren işlemlerde gerçek zamanlı güncelleme
- **Config**: çalışma yapılandırması
- **Tool Call ID**: çağrı kimliği

### State'e erişim

```python
@tool
def get_last_user_message(runtime: ToolRuntime) -> str:
    messages = runtime.state["messages"]
```

### State güncelleme

Araçlar `Command(update=...)` ile state güncelleyebilir:

```python
@tool
def set_user_name(new_name: str) -> Command:
    return Command(update={"user_name": new_name})
```

### Context'e erişim

Kullanıcı kimliği veya oturum bilgisi gibi veriler `runtime.context` üzerinden okunur.

### Store'a erişim

Kalıcı veriler `runtime.store` üzerinden alınır veya yazılır. Bu sayede araçlar konuşmalar arası uzun süreli bellekle çalışabilir.

Özetle tools, ajanların yalnızca cevap üreten sistemler olmaktan çıkıp dış dünyayla etkileşen uygulamalara dönüşmesini sağlar.
