# Agent Chat UI

[Agent Chat UI](https://github.com/langchain-ai/agent-chat-ui), herhangi bir LangChain ajanı ile etkileşim kurmak için konuşma tabanlı arayüz sağlayan bir Next.js uygulamasıdır. Gerçek zamanlı sohbet, tool görselleştirme ve time-travel debugging ile state forking gibi gelişmiş özellikleri destekler.

`create_agent` ile oluşturulan ajanlarla sorunsuz çalışır ve hem yerelde hem de LangSmith gibi dağıtılmış ortamlarda minimum kurulumla etkileşimli deneyimler sunar.

## Hızlı başlangıç

En hızlı yol hosted sürümü kullanmaktır:

1. [Agent Chat UI](https://agentchat.vercel.app) adresine gidin
2. Ajanınızın deployment URL'ini veya yerel sunucu adresini girerek bağlayın
3. Sohbete başlayın

Arayüz, tool call ve interrupt'ları otomatik algılayıp render eder.

## Yerel geliştirme

Özelleştirme gerekiyorsa projeyi yerelde çalıştırabilirsiniz:

```bash
npx create-agent-chat-app --project-name my-chat-ui
cd my-chat-ui
pnpm install
pnpm dev
```

## Ajanınıza bağlama

Agent Chat UI hem yerel hem de deploy edilmiş ajanlara bağlanabilir. Bunun için genellikle şu bilgiler gerekir:

- **Graph ID**: `langgraph.json` içindeki graph adı
- **Deployment URL**: örneğin `http://localhost:2024`
- **LangSmith API key**: isteğe bağlı; yerel Agent Server için gerekli olmayabilir

Kurulum tamamlandıktan sonra arayüz, ajanınızdaki interrupt edilmiş thread'leri de otomatik çekebilir.

Araç çağrılarını ve tool result mesajlarını kutudan çıktığı gibi render eder; gerekirse gösterilen mesajları özelleştirebilirsiniz.
