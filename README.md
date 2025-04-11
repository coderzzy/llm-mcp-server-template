# llm-mcp-server-template
LLM-MCP server 开发的模版项目

## MCP
- https://modelcontextprotocol.io/introduction
- MCP Server：https://modelcontextprotocol.io/quickstart/server
- MCP Client：https://modelcontextprotocol.io/quickstart/client
- OpenAI 使用 MCP：https://openai.github.io/openai-agents-python/mcp/

## 项目相关

### 环境准备
```
# 安装 uv 包管理工具，若已有，则跳过
curl -LsSf https://astral.sh/uv/install.sh | sh
source ~/.local/bin/env
uv --version

# 安装python3.10，若已有，则跳过
uv python list
uv python install 3.10

# client 目录，创建虚拟环境, 若已有，则跳过
uv venv --python 3.10
source .venv/bin/activate
uv add openai-agents socksio

# client 目录，正常运行
source .venv/bin/activate
export OPENAI_API_KEY=sk-xxx
python openai_client.py

```

ing...
初步计划：
- server：使用 nodejs，openai接口
- client：使用 python

https://www.cnblogs.com/smartloli/p/18801374
