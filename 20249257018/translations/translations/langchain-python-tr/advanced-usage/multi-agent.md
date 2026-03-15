# Multi-agent

Çok ajanlı sistemler, karmaşık iş akışlarını çözmek için özelleşmiş bileşenleri koordine eder. Ancak her karmaşık görev için çok ajanlı mimari gerekmez; bazen doğru araçlarla donatılmış tek bir ajan da benzer sonucu verebilir.

## Neden multi-agent?

Geliştiriciler genellikle şu ihtiyaçlar nedeniyle multi-agent yaklaşımı arar:

- **Bağlam yönetimi**: Modelin bağlam penceresini aşmadan uzman bilgiyi sunmak
- **Dağıtık geliştirme**: Farklı ekiplerin yetenekleri bağımsız geliştirebilmesi
- **Paralelleştirme**: Alt görevler için uzman işçiler üretip eşzamanlı çalıştırmak

Multi-agent desenleri özellikle şu durumlarda değerlidir:

- Tek bir ajan çok fazla [tool](/oss/python/langchain/tools) içerdiğinde
- Uzun istemler ve alan özel araçlar gerektiğinde
- Belirli koşullar sağlanmadan bazı yeteneklerin açılmaması gerektiğinde

Tasarımın merkezinde **context engineering** vardır: hangi ajanın hangi bilgiyi göreceğine karar vermek.

## Desenler

LangChain dokümanı beş ana desen açıklar:

- **Subagents**: Ana ajan, alt ajanları araç gibi koordine eder
- **Handoffs**: Duruma göre ajanlar arasında kontrol aktarılır
- **Skills**: İhtiyaç halinde yüklenen uzman istem ve bilgi paketleri
- **Router**: Giriş sınıflandırılır ve uygun uzman ajana yönlendirilir
- **Custom workflow**: LangGraph ile tamamen özel yürütme akışları kurulur

## Desen seçimi

Desen seçerken şu boyutlar değerlendirilir:

- Dağıtık geliştirme
- Paralel yürütme
- Multi-hop çağrılar
- Kullanıcıyla doğrudan etkileşim

Örneğin:

- Tek atımlık görevlerde `handoffs`, `skills` ve `router` daha verimli olabilir
- Tekrarlayan görevlerde durum koruyan `handoffs` ve `skills` çağrı sayısını azaltır
- Çok alanlı görevlerde `subagents` ve `router` paralel yürütme sayesinde daha verimlidir

## Performans karşılaştırması

Belge, farklı desenleri şu senaryolarda karşılaştırır:

- tek seferlik istek
- tekrarlanan istek
- çok alanlı istek

Ana çıkarımlar:

- `Subagents`, merkezi kontrol sağlar ancak fazladan model çağrısı maliyeti olabilir
- `Handoffs` ve `Skills`, tekrar eden görevlerde çağrı tasarrufu sağlar
- `Router`, açık yönlendirme adımıyla uzman ajanlara dağıtım yapar
- Büyük bağlamlı ve paralel işlerde `Subagents` ve `Router` öne çıkar
