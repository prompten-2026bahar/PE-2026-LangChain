# Human-in-the-loop

Human-in-the-Loop (HITL) middleware'i, ajan araç çağrılarına insan gözetimi eklemenizi sağlar. Model gözden geçirilmesi gereken bir eylem önerdiğinde yürütme durdurulabilir, karar beklenebilir ve daha sonra devam ettirilebilir.

Bu mekanizma, araç çağrılarını yapılandırılmış bir politika ile kontrol eder. Müdahale gerekiyorsa bir `interrupt` üretilir, yürütme durur ve durum LangGraph persistence ile saklanır.

İnsan kararı üç biçimde olabilir:

- `approve`: eylemi olduğu gibi onayla
- `edit`: eylemi değiştirerek çalıştır
- `reject`: eylemi reddet ve geri bildirim ver

## Interrupt karar türleri

Her araç için izin verilen karar tipleri `interrupt_on` yapılandırmasıyla belirlenir. Birden fazla araç aynı anda durdurulmuşsa her eylem için ayrı karar gerekir ve kararların sırası interrupt içindeki eylem sırasıyla aynı olmalıdır.

Araç argümanları düzenlenirken büyük değişikliklerden kaçınılmalıdır; aksi halde model davranışı beklenmedik şekilde değişebilir.

## Interrupt yapılandırma

HITL kullanmak için ajan oluşturulurken middleware listesine eklenir:

```python
from langchain.agents import create_agent
from langchain.agents.middleware import HumanInTheLoopMiddleware
from langgraph.checkpoint.memory import InMemorySaver

agent = create_agent(
    model="gpt-4.1",
    tools=[write_file_tool, execute_sql_tool, read_data_tool],
    middleware=[
        HumanInTheLoopMiddleware(
            interrupt_on={
                "write_file": True,
                "execute_sql": {"allowed_decisions": ["approve", "reject"]},
                "read_data": False,
            },
            description_prefix="Tool execution pending approval",
        ),
    ],
    checkpointer=InMemorySaver(),
)
```

Checkpoint zorunludur; üretimde kalıcı bir checkpointer kullanılmalıdır. Ayrıca çağrılarda `thread_id` verilmelidir.

## Interrupt'a yanıt verme

`version="v2"` ile `invoke()` çağrısı, `interrupts` alanı taşıyan bir `GraphOutput` döndürür. Bu kesmeler insan inceleme arayüzüne gösterilir ve ardından `Command(resume=...)` ile kararlar geri gönderilir.

### Approve

Araç olduğu gibi çalıştırılır.

### Edit

Araç adı ve argümanları düzenlenerek çalıştırılır.

### Reject

Araç çalıştırılmaz; bunun yerine gerekçe modele geri verilir.

Bu desen özellikle dosya yazma, SQL çalıştırma, finansal işlem ve yüksek riskli otomasyonlarda kullanılır.
