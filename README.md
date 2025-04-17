# llm-mcp-server-template
LLM-MCP server 开发的模版项目
- server为数字比大小能力
- client为各模型、各种调用方式

## MCP
- https://modelcontextprotocol.io/introduction
- 简单理解，
    - 模型(client)是大脑，负责规划和执行文本类任务，如第一步写代码，第二步执行，第三步分析。
    - MCP(Server)是工具，负责提供模型需要的其他能力，如数学计算、文件读写、网络请求等。
 
 ### MCP-Server
 - 主要负责实现mcp能力，如数学计算、文件读写、网络请求等
 - https://modelcontextprotocol.io/quickstart/server
 - 开发过程中，可以使用 mcp-server-inspector 工具协助调试
 - 几种类型的server：
    - 1、本地Stdio，client直接调用本地的server文件
    - 2、远程聚合平台SSE，如Glama.ai、MCP.so等

 ### MCP-Client
- 主要负责协调模型和mcp-server，最终实现"模型调用了mcp能力"
- 几种类型的client：
    - 1、直接用现成的客户端软件，如Cursor、MCP Inspector等。
    - 2、云平台上的各种智能体agent，如阿里云百炼应用管理。
    - 3、自己写脚本支持
        - 3.1、模型的sdk已经支持了mcp，使用脚本方便的进行调用
            - 如claude，https://modelcontextprotocol.io/quickstart/client
            - 如openai，https://openai.github.io/openai-agents-python/mcp/
        - 3.2、模型的sdk没有支持mcp，需要自己实现
            - 3.2.1、使用框架，如langchain-mcp-adapter(https://github.com/langchain-ai/langchain-mcp-adapters)
            - 3.2.2、完全原生，具体包括多轮请求：
                - a、使用 prompt 请求模型，告知模型任务和 mcp servers 的介绍，模型返回调用server的接口和参数
                - b、使用上一轮返回的信息，请求tools，获取结果
                - c、使用上一轮返回的信息，请求模型，获取结果
                - d、重复b、c，直到模型返回最终结果

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

cd server
# server 目录，创建虚拟环境, 若已有，则跳过
uv venv --python 3.10
source .venv/bin/activate
uv add "mcp[cli]" httpx

# server目录，开发的时候用mcp-server-inspect调试
mcp dev math.py

cd client
# client 目录，创建虚拟环境, 若已有，则跳过
uv venv --python 3.10
source .venv/bin/activate
uv add openai openai-agents socksio
touch .env  # 在.env文件中，设置OPENAI_API_KEY等

# client 目录，正常运行
source .venv/bin/activate
python openai_client.py
```

### 项目结果
MCP Server，mcp-server-inspect调试页面：
![mcp-server-inspect](https://github.com/coderzzy/llm-mcp-server-template/blob/main/README_files/MCP_Inspector.jpg)

MCP Client，不使用mcp和使用mcp的对比:
- 命令行调用结果：
![openai_client_result1](https://github.com/coderzzy/llm-mcp-server-template/blob/main/README_files/openai_client_result1.jpg)
- openai的dashboard上的log记录, mcp确实是两次调用:
![openai_client_result2](https://github.com/coderzzy/llm-mcp-server-template/blob/main/README_files/openai_client_result2.jpg)

## TODO
~~1、 mcp-server，本地开发和调试~~  
2、mcp-server，发布远程托管平台  
~~3、mcp-client，使用openai-agent-sdk调用server~~  
4、mcp-client，使用anthropic-sdk调用本地server  
5、mcp-client，使用langchain-mcp-adapter调用server  