# Model Context Protocol (MCP)

[Model Context Protocol (MCP)](https://modelcontextprotocol.io/introduction), uygulamaların LLM'lere araç ve bağlam sağlamasını standartlaştıran açık bir protokoldür. LangChain ajanları, [`langchain-mcp-adapters`](https://github.com/langchain-ai/langchain-mcp-adapters) kütüphanesi ile MCP sunucularında tanımlı araçları kullanabilir.

## Hızlı başlangıç

```bash
pip install langchain-mcp-adapters
```

`langchain-mcp-adapters`, bir veya daha fazla MCP sunucusundaki araçların ajan tarafından kullanılmasını sağlar.

`MultiServerMCPClient`, varsayılan olarak **stateless** çalışır: her tool çağrısında yeni bir MCP oturumu açılır, araç yürütülür ve oturum kapatılır.

## Birden çok MCP sunucusuna erişim

```python
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.agents import create_agent

client = MultiServerMCPClient(
    {
        "math": {
            "transport": "stdio",
            "command": "python",
            "args": ["/path/to/math_server.py"],
        },
        "weather": {
            "transport": "http",
            "url": "http://localhost:8000/mcp",
        }
    }
)
```

## Özel sunucular

Özel MCP sunucuları oluşturmak için `FastMCP` önerilir:

```bash
pip install fastmcp
```

Basit bir matematik sunucusu, `@mcp.tool()` dekoratörüyle `add` ve `multiply` gibi araçlar tanımlayabilir.

## Transport türleri

### HTTP

`http` veya `streamable-http`, istemci-sunucu iletişimini HTTP üzerinden yapar. Gerekirse özel header'lar ve özel kimlik doğrulama mekanizmaları geçirilebilir.

### stdio

İstemci, sunucuyu alt süreç olarak başlatır ve standart giriş/çıkış ile haberleşir. Yerel araçlar ve basit kurulumlar için uygundur.

## Stateful sessions

Varsayılan stateless davranış yerine, bağlamı oturumlar boyunca korumak istiyorsanız `client.session()` ile kalıcı bir `ClientSession` açabilirsiniz:

```python
async with client.session("server_name") as session:
    tools = await load_mcp_tools(session)
```

Bu yaklaşım, oturum bağlamı tutan stateful MCP sunucularında gereklidir.

## Temel özellikler

### Tools

MCP araçları, veritabanı sorgulama, API çağrısı veya harici sistemlerle etkileşim gibi yürütülebilir işlevler sunar. LangChain, bu araçları doğrudan kendi `tools` yapısına dönüştürür.

### Structured content

MCP araçları insan tarafından okunabilir metne ek olarak yapılandırılmış içerik de döndürebilir. Adaptör bunu `MCPToolArtifact` içine sarar ve `ToolMessage.artifact` üzerinden erişilebilir hale getirir.

Özetle MCP, araçların standardize edilmesi ve çoklu sunuculardan güvenli biçimde ajana bağlanması için güçlü bir entegrasyon katmanıdır.
