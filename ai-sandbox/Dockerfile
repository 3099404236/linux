FROM python:3.10-slim

# 安装系统工具包
RUN apt-get update && apt-get install -y \
    # 基础工具
    curl \
    wget \
    git \
    vim \
    nano \
    build-essential \
    # 搜索和查找工具
    ripgrep \
    fd-find \
    fzf \
    silversearcher-ag \
    # 文件工具
    tree \
    bat \
    ncdu \
    # 网络工具
    jq \
    httpie \
    lynx \
    w3m \
    netcat \
    telnet \
    dnsutils \
    # 数据库客户端
    sqlite3 \
    postgresql-client \
    # 文档处理
    pandoc \
    poppler-utils \
    # 多媒体
    ffmpeg \
    imagemagick \
    # 压缩工具
    zip \
    unzip \
    gzip \
    bzip2 \
    xz-utils \
    # 监控工具
    htop \
    iotop \
    # 其他
    tmux \
    screen \
    rsync \
    && rm -rf /var/lib/apt/lists/*

# 创建 fd 符号链接（Debian 中叫 fdfind）
RUN ln -s $(which fdfind) /usr/local/bin/fd 2>/dev/null || true

# 安装 GitHub CLI
RUN curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | \
    dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg && \
    chmod go+r /usr/share/keyrings/githubcli-archive-keyring.gpg && \
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | \
    tee /etc/apt/sources.list.d/github-cli.list > /dev/null && \
    apt-get update && \
    apt-get install -y gh && \
    rm -rf /var/lib/apt/lists/*

# 安装 Python 工具和库
RUN pip install --no-cache-dir \
    # AI 工具
    ollama \
    shell-gpt \
    open-interpreter \
    aider-chat \
    # 网络和爬虫
    requests \
    httpx \
    beautifulsoup4 \
    lxml \
    html2text \
    duckduckgo-search \
    wikipedia \
    # 数据处理
    pandas \
    numpy \
    # 数据库
    sqlalchemy \
    psycopg2-binary \
    pymongo \
    redis \
    # 视频/音频
    yt-dlp \
    pydub \
    # 文档处理
    python-docx \
    openpyxl \
    PyPDF2 \
    pdfplumber \
    markdown \
    # 图像处理
    Pillow \
    # API 工具
    pyyaml \
    toml \
    # 代码分析
    ast-grep-py \
    black \
    flake8 \
    pylint \
    # 测试工具
    pytest \
    pytest-cov \
    # 其他实用工具
    python-dotenv \
    click \
    rich \
    typer \
    # 浏览器自动化（轻量级）
    playwright \
    selenium

# 安装 Playwright 浏览器（可选，比较大）
# RUN playwright install chromium

# 创建工作目录
WORKDIR /workspace

# 创建非 root 用户（安全性）
RUN useradd -m -s /bin/bash aiuser && \
    chown -R aiuser:aiuser /workspace

# 创建常用目录
RUN mkdir -p /workspace/{downloads,projects,scripts,data} && \
    chown -R aiuser:aiuser /workspace

# 切换到非 root 用户
USER aiuser

# 配置 Git（基础设置）
RUN git config --global init.defaultBranch main && \
    git config --global core.editor vim

# 配置环境变量
ENV OLLAMA_HOST=http://host.docker.internal:11434
ENV PATH="/home/aiuser/.local/bin:${PATH}"

# 创建快捷别名配置
RUN echo 'alias ll="ls -lah"' >> ~/.bashrc && \
    echo 'alias rg="rg --smart-case"' >> ~/.bashrc && \
    echo 'alias cat="bat --style=plain"' >> ~/.bashrc && \
    echo 'alias find="fd"' >> ~/.bashrc && \
    echo 'export EDITOR=vim' >> ~/.bashrc

# 默认命令
CMD ["/bin/bash"]
