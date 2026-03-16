# LangSmith Studio

LangChain ile ajanları yerelde geliştirirken ajanın içinde neler olduğunu görselleştirmek, gerçek zamanlı etkileşim kurmak ve sorunları ayıklamak faydalıdır. **LangSmith Studio**, yerel makinenizde çalışan LangChain ajanlarını geliştirmek ve test etmek için ücretsiz bir görsel arayüz sunar.

Studio, yerelde çalışan ajana bağlanır ve şu adımları gösterir:

- modele gönderilen prompt'lar
- araç çağrıları ve sonuçları
- ara durumlar
- final çıktı

Bu sayede ek dağıtım yapmadan farklı girdileri deneyebilir ve ajan davranışını hızlıca iyileştirebilirsiniz.

## Gereksinimler

Başlamadan önce şunlar gerekir:

- bir LangSmith hesabı
- bir LangSmith API anahtarı

İzleme verilerinin LangSmith'e gitmesini istemiyorsanız `.env` içine `LANGSMITH_TRACING=false` koyabilirsiniz.

## Yerel Agent Server kurulumu

### 1. LangGraph CLI kurulumu

Yerel geliştirme sunucusu için:

```bash
# Python >= 3.11 gerekli
pip install --upgrade "langgraph-cli[inmem]"
```

### 2. Ajanı hazırlama

Mevcut LangChain ajanınızı kullanabilirsiniz. Basit örnek:

```python
from langchain.agents import create_agent

def send_email(to: str, subject: str, body: str):
    """Send an email"""
    return f"Email sent to {to}"

agent = create_agent(
    "gpt-5.2",
    tools=[send_email],
    system_prompt="You are an email assistant. Always use the send_email tool.",
)
```

### 3. Ortam değişkenleri

Proje kökünde bir `.env` dosyası oluşturup LangSmith API anahtarınızı ekleyin:

```env
LANGSMITH_API_KEY=lsv2...
```

Bu dosyanın Git'e eklenmemesi gerekir.

### 4. `langgraph.json` yapılandırması

LangGraph CLI, ajanı bulmak ve bağımlılıkları yönetmek için `langgraph.json` kullanır.

Özetle LangSmith Studio, ajan geliştirme döngüsünü hızlandıran görsel bir hata ayıklama ve test arayüzüdür.
