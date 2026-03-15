# Retrieval

Büyük Dil Modelleri güçlüdür; ancak iki temel sınıra sahiptir:

- Sonlu bağlam penceresi vardır, yani tüm bilgi yığınını tek seferde alamazlar.
- Bilgileri statiktir; eğitim verileri belirli bir zamanda donar.

Retrieval, sorgu anında ilgili harici bilgiyi getirerek bu sorunları çözer. Bu, **Retrieval-Augmented Generation (RAG)** yaklaşımının temelidir.

## Bilgi tabanı oluşturma

Bilgi tabanı, retrieval sırasında kullanılan belge veya yapılandırılmış veri deposudur.

Eğer özel bir bilgi tabanına ihtiyacınız varsa LangChain'in:

- belge yükleyicileri
- embedding modelleri
- vector store bileşenleri

ile kendi verinizden bir bilgi tabanı oluşturabilirsiniz.

Zaten bir bilgi tabanınız varsa bunu yeniden kurmanız gerekmez. Bunun yerine:

- Ajan için bir **tool** olarak bağlayabilirsiniz
- Çekilen içeriği bağlam olarak modele verip **2-Step RAG** akışında kullanabilirsiniz

## Retrieval'dan RAG'e geçiş

Retrieval, LLM'lerin çalışma anında ilgili bağlama erişmesini sağlar. Gerçek dünyadaki uygulamalar ise genellikle retrieval'i üretimle birleştirerek bağlama dayalı yanıt üretir. Bu yaklaşımın adı RAG'dir.

## Yapı taşları

RAG sistemlerinde temel bileşenler şunlardır:

- Document loaders
- Text splitters
- Embedding models
- Vector stores
- Retrievers

Bu bileşenler modülerdir; uygulamanın mantığını baştan yazmadan değiştirilebilirler.

## RAG mimarileri

LangChain dokümanı üç ana yaklaşımı açıklar:

### 1. 2-Step RAG

Retrieval her zaman üretimden önce yapılır. Basit, öngörülebilir ve hızlıdır. Dokümantasyon botları ve SSS sistemleri için uygundur.

### 2. Agentic RAG

LLM destekli ajan, bilgiye ne zaman ve nasıl erişeceğine çalışma anında karar verir. Esnektir fakat gecikmesi değişkendir.

```python
import requests
from langchain.tools import tool
from langchain.chat_models import init_chat_model
from langchain.agents import create_agent

@tool
def fetch_url(url: str) -> str:
    """Fetch text content from a URL"""
    response = requests.get(url, timeout=10.0)
    response.raise_for_status()
    return response.text
```

Bu modelde retrieval davranışı sağlamak için ajanın bir veya daha fazla harici bilgi getiren araca erişebilmesi yeterlidir.

### 3. Hybrid RAG

2-Step ve Agentic RAG özelliklerini birleştirir. Sorgu iyileştirme, retrieval doğrulama ve yanıt kontrolü gibi ara adımlar içerebilir.

Tipik bileşenler:

- Sorgu geliştirme
- Retrieval doğrulama
- Yanıt doğrulama

Bu mimari, belirsiz sorgular, kalite kontrol gerektiren sistemler ve birden fazla kaynağın birlikte kullanıldığı iş akışları için uygundur.
