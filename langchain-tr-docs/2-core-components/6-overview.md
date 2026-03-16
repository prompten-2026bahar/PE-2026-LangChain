# LangChain Genel Bakış

LangChain, önceden hazırlanmış bir ajan mimarisi ve farklı model ya da araçlarla entegrasyonlar sunan açık kaynaklı bir çerçevedir; böylece ekosistem geliştikçe uyum sağlayabilen ajanlar inşa edebilirsiniz.

LangChain, LLM destekli tamamen özelleştirilmiş ajanlar ve uygulamalar geliştirmeye başlamanın en kolay yoludur. Kısa bir kodla OpenAI, Anthropic, Google ve daha fazlasına bağlanabilirsiniz. Çerçeve, hızlı başlamanıza ve LLM'leri ajanlarınıza ve uygulamalarınıza sorunsuz biçimde entegre etmenize yardımcı olmak için önceden hazırlanmış bir ajan mimarisi ve model entegrasyonları sunar.

## LangChain, LangGraph ve Deep Agents karşılaştırması

Bir ajan geliştirmek istiyorsanız, otomatik konuşma sıkıştırma, sanal dosya sistemi ve alt ajan başlatma gibi özelliklerle kutudan çıktığı gibi çalışan bir yapı sunduğu için Deep Agents ile başlamanız önerilir. Bu yeteneklere ihtiyaç duymuyorsanız veya daha fazla özelleştirme istiyorsanız LangChain ile başlayın. Deterministik akışlar ile ajan tabanlı akışların birleşimi ve daha düşük seviyeli kontrol gerekiyorsa LangGraph kullanın.

## Bir ajan oluşturun

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
```

## Temel avantajlar

### Standart model arayüzü

Sağlayıcıların farklı API'lerini tek bir standart etkileşim modeline indirger.

### Kullanımı kolay ve esnek ajan yapısı

Az kodla başlangıç yapılabilir, ancak ihtiyaç duyulan bağlam mühendisliği ve özelleştirmeye de izin verir.

### LangGraph üzerine inşa edilmiştir

Dayanıklı yürütme, insanın sürece dahil olması, kalıcılık ve akış yetenekleri LangGraph tabanı üzerinden sağlanır.

### LangSmith ile hata ayıklama

Yürütme yollarını, durum geçişlerini ve çalışma zamanı metriklerini görünür kılar.
