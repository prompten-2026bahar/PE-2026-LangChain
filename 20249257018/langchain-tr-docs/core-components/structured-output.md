# Structured Output

Structured output, ajanların belirli ve öngörülebilir bir formatta veri döndürmesini sağlar. Doğal dil çıktısını sonradan ayrıştırmak yerine, doğrudan JSON nesneleri, Pydantic modelleri veya dataclass biçiminde veriler elde edersiniz.

Bu sayfa, `create_agent` ile ajanlar üzerindeki structured output kullanımını açıklar.

## `response_format`

Structured output davranışı `response_format` parametresiyle kontrol edilir:

- `ToolStrategy[StructuredResponseT]`
- `ProviderStrategy[StructuredResponseT]`
- doğrudan şema tipi
- `None`

Bir şema doğrudan verildiğinde LangChain en uygun stratejiyi seçer:

- Sağlayıcı yerel structured output destekliyorsa `ProviderStrategy`
- Aksi halde `ToolStrategy`

Sonuç, ajan state'i içindeki `structured_response` anahtarında döner.

## Provider strategy

Bazı sağlayıcılar structured output'u API seviyesinde doğal olarak destekler. Bu yöntem en güvenilir seçenektir.

Desteklenen şema tipleri:

- Pydantic modeller
- Dataclass'lar
- TypedDict
- JSON Schema

Örnek:

```python
class ContactInfo(BaseModel):
    name: str
    email: str
    phone: str

agent = create_agent(
    model="gpt-5",
    response_format=ContactInfo
)
```

## Tool calling strategy

Yerel structured output desteği olmayan modellerde LangChain, tool calling ile aynı sonucu üretir.

`ToolStrategy` şu seçenekleri sunar:

- `schema`
- `tool_message_content`
- `handle_errors`

Bu strateji:

- şema doğrulaması yapar
- validation hatalarını isteğe göre yakalayabilir
- birden fazla şema seçeneğini `Union` ile destekleyebilir

## Hata yönetimi

`handle_errors` parametresi için seçenekler:

- `True`
- özel string
- belirli exception tipi
- exception tuple'ı
- özel callback
- `False`

Bu sayede structured output doğrulama başarısızlıkları için esnek retry ve hata mesajı davranışı kurulabilir.
