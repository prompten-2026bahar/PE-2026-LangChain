# Integration Testing

Integration test'ler, ajanın model API'leri ve harici servislerle birlikte doğru çalıştığını doğrular. Unit test'lerden farklı olarak gerçek ağ çağrıları yapar; bu sayede bileşenlerin birlikte çalışması, kimlik bilgileri, şema uyumu ve kabul edilebilir gecikme ölçülebilir.

LLM yanıtları deterministik olmadığı için integration test'ler klasik yazılım testlerinden farklı stratejiler gerektirir.

## Unit ve integration test'leri ayırma

Integration test'ler daha yavaş çalışır ve API anahtarları ister. Bu yüzden pytest marker'larıyla ayrılması önerilir:

```python
import pytest

@pytest.mark.integration
def test_agent_with_real_model():
    agent = create_agent("claude-sonnet-4-6", tools=[get_weather])
```

Varsayılan çalıştırmalarda integration test'leri hariç tutmak için:

```ini
[pytest]
markers =
    integration: tests that call real LLM APIs
addopts = -m "not integration"
```

Integration test'leri açıkça çalıştırmak için:

```bash
pytest -m integration
```

## API anahtarlarını yönetme

Gerçek sağlayıcılarla test için anahtarları ortam değişkenlerinden yükleyin. `conftest.py` içinde anahtar yoksa testi atlayan fixture kullanılabilir:

```python
import os
import pytest

@pytest.fixture(autouse=True)
def check_api_keys():
    if not os.environ.get("OPENAI_API_KEY"):
        pytest.skip("OPENAI_API_KEY not set")
```

Yerel geliştirme için `.env` ve `python-dotenv` kullanılabilir.

Özetle integration testing, ajanın gerçek dünyadaki çalışma koşullarını doğrulamak için gereklidir; fakat maliyet, gizli anahtar yönetimi ve flaky yanıtlar nedeniyle dikkatli tasarlanmalıdır.
