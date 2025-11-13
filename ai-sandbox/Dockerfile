FROM python:3.10-slim

# 安装系统工具
RUN apt-get update && apt-get install -y \
    curl \
    git \
    vim \
    wget \
    build-essential \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# 安装 Ollama 客户端库
RUN pip install --no-cache-dir \
    ollama \
    shell-gpt \
    open-interpreter \
    aider-chat

# 创建工作目录
WORKDIR /workspace

# 创建非 root 用户（安全性）
RUN useradd -m -s /bin/bash aiuser && \
    chown -R aiuser:aiuser /workspace

# 切换到非 root 用户
USER aiuser

# 配置环境变量
ENV OLLAMA_HOST=http://host.docker.internal:11434

# 默认命令
CMD ["/bin/bash"]
