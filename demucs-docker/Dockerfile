FROM nvidia/cuda:11.8.0-cudnn8-runtime-ubuntu22.04

# 设置工作目录
WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    python3.10 \
    python3-pip \
    ffmpeg \
    git \
    && rm -rf /var/lib/apt/lists/*

# 创建 python 符号链接
RUN ln -s /usr/bin/python3.10 /usr/bin/python

# 配置 pip 使用清华源（加速下载）
RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple && \
    pip config set global.timeout 1000

# 安装 PyTorch (CUDA 11.8)
RUN pip install --no-cache-dir \
    torch==2.1.0 \
    torchaudio==2.1.0 \
    --index-url https://download.pytorch.org/whl/cu118

# 安装 Demucs
RUN pip install --no-cache-dir demucs

# 创建输入输出目录
RUN mkdir -p /audio/input /audio/output

# 设置工作目录
WORKDIR /audio

# 默认命令
CMD ["bash"]
