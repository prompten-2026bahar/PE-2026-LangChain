# Deployment

LangChain ajanınızı üretime taşımaya hazır olduğunuzda, LangSmith ajan iş yükleri için tasarlanmış yönetilen bir barındırma platformu sunar. Geleneksel platformlar kısa ömürlü ve stateless web uygulamalarına odaklanırken, LangGraph durum tutan ve arka planda uzun süre çalışan ajanlar için özel olarak tasarlanmıştır.

LangSmith; altyapı, ölçekleme ve operasyonel yükü üstlenir; siz de doğrudan repository'nizden dağıtım yapabilirsiniz.

## Gereksinimler

Başlamadan önce şunlar gerekir:

- bir GitHub hesabı
- bir LangSmith hesabı

## Ajanı deploy etme

### 1. GitHub repository oluşturma

Uygulama kodunuz bir GitHub deposunda olmalıdır. Hem public hem private repo desteklenir. Önce uygulamanın LangGraph uyumlu olduğundan emin olun ve kodu repoya gönderin.

### 2. LangSmith'e deploy etme

Genel akış:

1. LangSmith içinde **Deployments** bölümüne gidin
2. **+ New Deployment** ile yeni deployment oluşturun
3. Gerekirse GitHub hesabınızı bağlayın
4. Repository seçip **Submit** ile deploy edin

Tamamlanması yaklaşık 15 dakika sürebilir.

### 3. Studio içinde uygulamayı test etme

Deployment tamamlandıktan sonra ilgili deployment detay sayfasından **Studio** düğmesi ile grafiği açabilirsiniz.

### 4. API URL'ini alma

Deployment detayları içinden **API URL** kopyalanır.

### 5. API'yi test etme

Python tarafında `langgraph-sdk` ile agent endpoint'i test edilebilir:

```bash
pip install langgraph-sdk
```

Ardından deployment URL ve LangSmith API anahtarı ile istemci oluşturulup stream üzerinden ajan çağrılabilir.

Bu sayfa, LangSmith'in stateful ajanları üretime almak için önerilen managed dağıtım yolunu özetler.
