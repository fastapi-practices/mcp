## MCP 服务器

使用此插件前，根据实际情况在环境变量文件 `.env` 中添加以下内容:

```dotenv
# MCP
MCP_OPENAI_API_KEY='兼容openai的供应商API密钥'
MCP_DEEPSEEK_API_KEY='deekseek官方API密钥'
MCP_ANTHROPIC_API_KEY='Claude官方API密钥'
MCP_GEMINI_API_KEY='Gemini官方API密钥'
```

以上 MCP 环境变量均为可选，它们将用于在 MCP `/chat` 接口内请求 LLM 供应商，默认情况下，所有 `API KEY` 均为空值

`API KEY` 的设定取决于个人/团队，例如，如果你想要调用 deepseek 官方进行回复，则就必须在 `.env` 中添加
`MCP_DEEPSEEK_API_KEY='your_key'`；

