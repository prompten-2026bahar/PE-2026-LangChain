# Test

Ajanik uygulamalar, problemi çözmek için bir LLM'in kendi sonraki adımlarını seçmesine izin verir. Bu esneklik güçlüdür; ancak modelin kara kutu yapısı nedeniyle ajandaki bir değişikliğin tüm sistemi nasıl etkileyeceğini öngörmek zordur. Bu yüzden üretime hazır ajanlar için kapsamlı test şarttır.

Belgede üç temel yaklaşım önerilir:

- **Unit tests**: küçük ve deterministik parçaları sahte bileşenlerle izole biçimde test eder
- **Integration tests**: gerçek ağ çağrıları ve gerçek servislerle bileşenlerin birlikte çalıştığını doğrular
- **Evals**: ajanın izlediği yürütme yolunu referans veya rubrik üzerinden değerlendirir

Ajanik uygulamalar, LLM'lerin deterministik olmaması ve çoklu bileşen zincirleri nedeniyle genellikle integration test'lere daha fazla ihtiyaç duyar.

Alt sayfalar:

- `unit-testing.md`
- `integration-testing.md`
- `evals.md`
