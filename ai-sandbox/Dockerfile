FROM python:3.10-slim

# 使用国内镜像源（加速构建）
RUN sed -i 's/deb.debian.org/mirrors.aliyun.com/g' /etc/apt/sources.list.d/debian.sources || \
    sed -i 's/deb.debian.org/mirrors.aliyun.com/g' /etc/apt/sources.list

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
    netcat-openbsd \
    telnet \
    dnsutils \
    # 数据库客户端
    sqlite3 \
    postgresql-client \
    # 文档处理
    pandoc \
    poppler-utils \
    # LaTeX 支持（XeLaTeX 用于中文编译）
    texlive-xetex \
    texlive-fonts-recommended \
    texlive-latex-extra \
    texlive-lang-chinese \
    latexmk \
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

# 安装 Node.js (LTS 20.x)
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && \
    apt-get install -y nodejs && \
    rm -rf /var/lib/apt/lists/*

# 安装 GitHub CLI
RUN curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | \
    dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg && \
    chmod go+r /usr/share/keyrings/githubcli-archive-keyring.gpg && \
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | \
    tee /etc/apt/sources.list.d/github-cli.list > /dev/null && \
    apt-get update && \
    apt-get install -y gh && \
    rm -rf /var/lib/apt/lists/*

# 安装 Docker CLI（只安装客户端，不安装 daemon）
RUN curl -fsSL https://download.docker.com/linux/debian/gpg | \
    gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg && \
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/debian bullseye stable" | \
    tee /etc/apt/sources.list.d/docker.list > /dev/null && \
    apt-get update && \
    apt-get install -y docker-ce-cli docker-compose-plugin && \
    rm -rf /var/lib/apt/lists/*

# 安装 Go (1.21.x) - 使用国内镜像
RUN curl -fsSL https://mirrors.aliyun.com/golang/go1.21.5.linux-amd64.tar.gz -o /tmp/go.tar.gz || \
    curl -fsSL https://go.dev/dl/go1.21.5.linux-amd64.tar.gz -o /tmp/go.tar.gz && \
    tar -C /usr/local -xzf /tmp/go.tar.gz && \
    rm /tmp/go.tar.gz
ENV PATH="/usr/local/go/bin:${PATH}"
ENV GOPATH="/home/aiuser/go"
ENV PATH="${GOPATH}/bin:${PATH}"
ENV GOPROXY="https://goproxy.cn,direct"

# 配置 pip 使用国内镜像源（加速下载）
RUN pip config set global.index-url https://mirrors.aliyun.com/pypi/simple/ && \
    pip config set install.trusted-host mirrors.aliyun.com

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

# 克隆并安装用户的 pdf2ppt-converter 项目
RUN git clone https://github.com/3099404236/pdf2ppt-converter.git /tmp/pdf2ppt && \
    cd /tmp/pdf2ppt && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir -e . && \
    rm -rf /tmp/pdf2ppt/.git

# 创建安全的 Docker 包装脚本（防止删除镜像）
RUN cat > /usr/local/bin/safe-docker << 'EOF'
#!/bin/bash
# 安全的 Docker 包装脚本 - 防止删除镜像

# 拦截危险的删除命令
if [[ "$1" == "rmi" ]] || \
   [[ "$1" == "image" && "$2" == "rm" ]] || \
   [[ "$1" == "image" && "$2" == "prune" ]] || \
   [[ "$1" == "system" && "$2" == "prune" && "$*" =~ "-a" ]]; then
    echo "❌ 错误: 为了安全，禁止在沙盒中删除镜像！"
    echo "   被拦截的命令: docker $@"
    echo ""
    echo "   如果你真的需要删除镜像，请在主机上执行："
    echo "   exit  # 退出沙盒"
    echo "   docker $@  # 在主机上执行"
    exit 1
fi

# 其他命令正常执行
exec /usr/bin/docker "$@"
EOF

RUN chmod +x /usr/local/bin/safe-docker

# 创建工作目录
WORKDIR /workspace

# 创建非 root 用户（安全性）
RUN useradd -m -s /bin/bash aiuser && \
    chown -R aiuser:aiuser /workspace

# 将 aiuser 添加到 docker 组（如果存在）
RUN groupadd -f docker && usermod -aG docker aiuser

# 创建常用目录
RUN mkdir -p /workspace/{downloads,projects,scripts,data} && \
    chown -R aiuser:aiuser /workspace

# 切换到非 root 用户
USER aiuser

# 配置 npm 使用国内镜像源
RUN npm config set registry https://registry.npmmirror.com

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
    echo 'alias docker="safe-docker"' >> ~/.bashrc && \
    echo 'export EDITOR=vim' >> ~/.bashrc && \
    echo 'export PATH="/usr/local/go/bin:$HOME/go/bin:$PATH"' >> ~/.bashrc && \
    echo '' >> ~/.bashrc && \
    echo '# Docker 命令提示' >> ~/.bashrc && \
    echo 'echo "💡 提示: Docker 命令已启用，但删除镜像功能已被禁用以保护主机"' >> ~/.bashrc

# 默认命令
CMD ["/bin/bash"]
