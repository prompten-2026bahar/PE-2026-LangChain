# Middleware Genel Bakış

Middleware, ajan yürütmesinin farklı aşamalarına müdahale etmenizi sağlayan genişletme noktaları sunar. Model çağrılarından araç çalıştırmalarına kadar çeşitli adımlarda davranışı değiştirebilir, izleme ekleyebilir, yönlendirme uygulayabilir veya güvenlik denetimleri koyabilirsiniz.

LangChain middleware yapısı, özellikle şu durumlarda kullanışlıdır:

- Modeli çalışma zamanında değiştirmek
- İstekleri veya yanıtları dönüştürmek
- Loglama ve gözlemlenebilirlik eklemek
- Koruma katmanları ve politika kontrolleri uygulamak
- Araç çağrılarından önce ya da sonra işlem yapmak

Hazır middleware bileşenlerini kullanabilir veya kendi middleware katmanınızı yazabilirsiniz.
