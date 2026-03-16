# Tool Calling

Ajanlar hava durumu API'leri, hesap makineleri, web araması, veritabanı sorguları ve daha birçok harici aracı çağırabilir. Sonuçlar genellikle ham JSON olarak gelir. Bu desen, her araç çağrısı için yükleme ve hata durumlarıyla birlikte yapılandırılmış, tür güvenli UI kartları nasıl oluşturulacağını açıklar.

## Tool calling nasıl çalışır?

LangGraph ajanı harici veriye ihtiyaç duyduğunda, bir AI mesajının parçası olarak bir veya daha fazla **tool call** üretir. Her araç çağrısı şunları içerir:

- `name`: çağrılan araç
- `args`: araca geçirilen yapılandırılmış argümanlar
- `id`: çağrıyı sonuçla eşleştiren benzersiz kimlik

Araç çalıştırıldıktan sonra sonuç `ToolMessage` olarak döner ve `useStream`, bunları tek bir `toolCalls` dizisinde birleştirir.

## `useStream` kurulumu

```ts
import type { BaseMessage } from "@langchain/core/messages";

interface AgentState {
  messages: BaseMessage[];
}
```

React örneği:

```tsx
import { useStream } from "@langchain/react";

const AGENT_URL = "http://localhost:2024";

export function Chat() {
  const stream = useStream<typeof myAgent>({
    apiUrl: AGENT_URL,
    assistantId: "tool_calling",
  });
}
```

## `ToolCallWithResult` tipi

Her `toolCalls` girdisi şu yapıya sahiptir:

```ts
interface ToolCallWithResult {
  call: {
    id: string;
    name: string;
    args: Record<string, unknown>;
  };
  result: ToolMessage | undefined;
  state: "pending" | "completed" | "error";
}
```

## Mesaj bazında araç çağrılarını filtreleme

Bir AI mesajı birden fazla araç çağrısı üretebilir. Doğru kartları ilgili mesajın altında göstermek için `call.id`, mesajın `tool_calls` alanıyla eşleştirilir.

```tsx
const messageToolCalls = toolCalls.filter((tc) =>
  message.tool_calls?.find((t) => t.id === tc.call.id)
);
```

## Uzmanlaşmış araç kartları

Ham JSON göstermek yerine araç adına göre özel kartlar oluşturmak önerilir:

```tsx
switch (toolCall.call.name) {
  case "get_weather":
    return <WeatherCard args={toolCall.call.args} result={toolCall.result} />;
  case "calculator":
    return <CalculatorCard args={toolCall.call.args} result={toolCall.result} />;
  default:
    return <GenericToolCard toolCall={toolCall} />;
}
```

## Weather card örneği

```tsx
function WeatherCard({
  args,
  result,
}: {
  args: { location: string };
  result: ToolMessage;
}) {
  const data = JSON.parse(result.content as string);
}
```

## Yükleme ve hata durumları

Her zaman `pending`, `completed` ve `error` durumlarını ele alın:

```tsx
function LoadingCard({ name }: { name: string }) {
  return <div>Running {name}...</div>;
}
```

## Tür güvenli araç argümanları

Araçlar yapılandırılmış şemalarla tanımlandıysa `ToolCallFromTool` yardımcı tipi ile `args` alanını tam tipli hale getirebilirsiniz. Böylece araç şeması değiştiğinde UI bileşenleri derleme anında hata verir.

## Akışla birlikte satır içi gösterim

Araç çağrıları, akış metni ile iç içe gelebilir. `useStream` sayesinde:

1. Metin akarken görünür
2. Tool call üretildiği anda yükleme kartı görünür
3. Araç tamamlanınca aynı kart sonuçla güncellenir

## Çoklu eşzamanlı araç çağrıları

Ajanlar aynı anda birden çok araç çağırabilir. Bu durumda `toolCalls` içinde birden fazla `pending` öğe olur ve her biri bağımsız tamamlanır.

## En iyi uygulamalar

- Her üç durumu da ele alın: `pending`, `completed`, `error`
- JSON ayrıştırmasını `try/catch` ile güvenli yapın
- Bilinmeyen araçlar için genel bir fallback kartı sunun
- Yükleme sırasında araç adını ve argümanlarını gösterin
- Kartları sohbet içinde kompakt tutun
