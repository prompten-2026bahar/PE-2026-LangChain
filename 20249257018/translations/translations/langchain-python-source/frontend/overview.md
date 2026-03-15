Build rich, interactive frontends for agents created with `createAgent`. These patterns cover everything from basic message rendering to advanced workflows like human-in-the-loop approval and time travel debugging.

## [](#architecture) Architecture

Every pattern follows the same architecture: a `createAgent` backend streams state to a frontend via the `useStream` hook.

On the backend, `createAgent` produces a compiled LangGraph graph that exposes
a streaming API. On the frontend, the `useStream` hook connects to that API
and provides reactive state, including messages, tool calls, interrupts, and
history, that you render with any framework.

agent.py

types.ts

Chat.tsx


```
from langchain import create_agent
from langgraph.checkpoint.memory import MemorySaver

agent = create_agent(
    model="openai:gpt-5.4",
    tools=[get_weather, search_web],
    checkpointer=MemorySaver(),
)
```

`useStream` is available for React, Vue, Svelte, and Angular:


```
import { useStream } from "@langchain/react";   // React
import { useStream } from "@langchain/vue";      // Vue
import { useStream } from "@langchain/svelte";   // Svelte
import { useStream } from "@langchain/angular";  // Angular
```

## [](#patterns) Patterns

### [](#render-messages-and-output) Render messages and output

[## Markdown messages

Parse and render streamed markdown with proper formatting and code highlighting.](/oss/python/langchain/frontend/markdown-messages)[## Structured output

Render typed agent responses as custom UI components instead of plain text.](/oss/python/langchain/frontend/structured-output)[## Reasoning tokens

Display model thinking processes in collapsible blocks.](/oss/python/langchain/frontend/reasoning-tokens)[## Generative UI

Render AI-generated user interfaces from natural language prompts using json-render.](/oss/python/langchain/frontend/generative-ui)

### [](#display-agent-actions) Display agent actions

[## Tool calling

Show tool calls as rich, type-safe UI cards with loading and error states.](/oss/python/langchain/frontend/tool-calling)[## Human-in-the-loop

Pause the agent for human review with approve, reject, and edit workflows.](/oss/python/langchain/frontend/human-in-the-loop)

### [](#manage-conversations) Manage conversations

[## Branching chat

Edit messages, regenerate responses, and navigate conversation branches.](/oss/python/langchain/frontend/branching-chat)[## Message queues

Queue multiple messages while the agent processes them sequentially.](/oss/python/langchain/frontend/message-queues)

### [](#advanced-streaming) Advanced streaming

[## Join & rejoin streams

Disconnect from and reconnect to running agent streams without losing progress.](/oss/python/langchain/frontend/join-rejoin)[## Time travel

Inspect, navigate, and resume from any checkpoint in the conversation history.](/oss/python/langchain/frontend/time-travel)

---

[Edit this page on GitHub](https://github.com/langchain-ai/docs/edit/main/src/oss/langchain/frontend/overview.mdx) or [file an issue](https://github.com/langchain-ai/docs/issues/new/choose).

[Connect these docs](/use-these-docs) to Claude, VSCode, and more via MCP for real-time answers.
