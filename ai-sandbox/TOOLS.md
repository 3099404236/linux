# AI 沙盒工具清单

本文档列出 AI 沙盒中所有可用的工具，模拟 Claude Code 的完整能力。

---

## 🔍 搜索和查找工具

### ripgrep (rg) - 代码搜索
```bash
# 搜索代码中的关键字（智能大小写）
rg "function.*main"

# 搜索特定文件类型
rg "TODO" --type python

# 搜索并显示上下文
rg "error" -C 3
```

### fd - 文件查找
```bash
# 查找文件
fd "*.py"

# 查找目录
fd --type d "test"

# 忽略 .gitignore
fd --hidden "config"
```

### fzf - 模糊搜索
```bash
# 交互式搜索文件
vim $(fzf)

# 搜索历史命令
history | fzf

# 搜索进程
ps aux | fzf
```

### ag (The Silver Searcher) - 快速搜索
```bash
# 快速搜索代码
ag "pattern" /path/to/code
```

---

## 📄 文件工具

### bat - 增强的 cat
```bash
# 显示文件（带语法高亮）
bat file.py

# 显示行号和 Git 变更
bat --style=numbers,changes file.py
```

### tree - 目录树
```bash
# 显示目录结构
tree

# 限制层级
tree -L 2

# 只显示目录
tree -d
```

### ncdu - 磁盘使用分析
```bash
# 交互式磁盘使用分析
ncdu /workspace
```

---

## 🌐 网络工具

### httpie - 友好的 HTTP 客户端
```bash
# GET 请求
http https://api.github.com/users/torvalds

# POST JSON
http POST https://httpbin.org/post name=john age=30

# 带认证
http https://api.example.com Authorization:"Bearer TOKEN"
```

### curl - 通用下载工具
```bash
# 下载文件
curl -O https://example.com/file.zip

# 查看响应头
curl -I https://example.com

# POST 请求
curl -X POST -H "Content-Type: application/json" \
  -d '{"key":"value"}' https://api.example.com
```

### lynx / w3m - 文本浏览器
```bash
# 查看网页（文本模式）
lynx -dump https://example.com

# 交互式浏览
w3m https://example.com
```

### netcat (nc) - 网络瑞士军刀
```bash
# 测试端口
nc -zv host.docker.internal 7890

# 监听端口
nc -l 8080

# 发送数据
echo "test" | nc localhost 8080
```

### nslookup / dig - DNS 查询
```bash
# 查询域名
nslookup google.com

# 详细 DNS 信息
dig google.com
```

---

## 🗄️ 数据库工具

### sqlite3 - SQLite 客户端
```bash
# 连接数据库
sqlite3 database.db

# 执行查询
sqlite3 database.db "SELECT * FROM users;"

# 导出为 CSV
sqlite3 -header -csv database.db "SELECT * FROM users;" > users.csv
```

### psql - PostgreSQL 客户端
```bash
# 连接数据库
psql -h localhost -U username -d database

# 执行查询
psql -h host -U user -d db -c "SELECT * FROM table;"
```

---

## 📝 文档处理

### pandoc - 文档转换
```bash
# Markdown 转 HTML
pandoc input.md -o output.html

# Markdown 转 PDF
pandoc input.md -o output.pdf

# 转换文档格式
pandoc input.docx -o output.md
```

### pdftotext - PDF 提取文本
```bash
# 提取 PDF 文本
pdftotext document.pdf output.txt

# 保持布局
pdftotext -layout document.pdf
```

---

## 🎨 多媒体工具

### ffmpeg - 音视频处理
```bash
# 转换格式
ffmpeg -i input.mp4 output.avi

# 提取音频
ffmpeg -i video.mp4 -vn -acodec copy audio.aac

# 压缩视频
ffmpeg -i input.mp4 -vcodec libx264 -crf 28 output.mp4
```

### imagemagick - 图像处理
```bash
# 调整大小
convert input.jpg -resize 800x600 output.jpg

# 格式转换
convert image.png image.jpg

# 批量处理
mogrify -resize 50% *.jpg
```

---

## 📦 压缩工具

```bash
# ZIP
zip archive.zip file1 file2
unzip archive.zip

# TAR.GZ
tar -czf archive.tar.gz directory/
tar -xzf archive.tar.gz

# TAR.BZ2
tar -cjf archive.tar.bz2 directory/
tar -xjf archive.tar.bz2
```

---

## 🔧 开发工具

### git - 版本控制
```bash
# 完整的 Git 功能
git clone https://github.com/user/repo.git
git add .
git commit -m "message"
git push
```

### gh - GitHub CLI
```bash
# 克隆仓库
gh repo clone user/repo

# 创建 PR
gh pr create

# 查看 issue
gh issue list

# 创建 gist
gh gist create file.txt
```

### jq - JSON 处理
```bash
# 格式化 JSON
echo '{"name":"John","age":30}' | jq .

# 提取字段
curl https://api.github.com/users/torvalds | jq '.name'

# 过滤数组
echo '[1,2,3,4,5]' | jq 'map(select(. > 2))'
```

---

## 🐍 Python 工具和库

### AI 工具
- **ollama** - Ollama Python 客户端
- **shell-gpt** - AI 命令行助手
- **open-interpreter** - AI 代码执行
- **aider-chat** - AI 代码编辑器

### 网络和爬虫
- **requests** / **httpx** - HTTP 客户端
- **beautifulsoup4** - HTML 解析
- **lxml** - XML/HTML 处理
- **html2text** - HTML 转文本
- **duckduckgo-search** - DuckDuckGo 搜索
- **wikipedia** - Wikipedia API

### 数据处理
- **pandas** - 数据分析
- **numpy** - 科学计算

### 数据库
- **sqlalchemy** - ORM 工具
- **psycopg2** - PostgreSQL 驱动
- **pymongo** - MongoDB 客户端
- **redis** - Redis 客户端

### 多媒体
- **yt-dlp** - 视频下载（支持B站）
- **pydub** - 音频处理
- **Pillow** - 图像处理

### 文档处理
- **python-docx** - Word 文档
- **openpyxl** - Excel 文档
- **PyPDF2** / **pdfplumber** - PDF 处理
- **markdown** - Markdown 解析

### 代码分析
- **ast-grep-py** - AST 代码搜索
- **black** - 代码格式化
- **flake8** - 代码检查
- **pylint** - 静态分析

### 测试
- **pytest** - 测试框架
- **pytest-cov** - 测试覆盖率

### 浏览器自动化
- **playwright** - 现代浏览器自动化
- **selenium** - 经典浏览器自动化

---

## 📊 监控工具

### htop - 交互式进程查看器
```bash
htop
```

### iotop - I/O 监控
```bash
iotop
```

---

## 🛠️ 终端工具

### tmux - 终端复用器
```bash
# 创建会话
tmux new -s session_name

# 列出会话
tmux ls

# 连接会话
tmux attach -t session_name
```

### screen - 屏幕管理
```bash
# 创建会话
screen -S session_name

# 列出会话
screen -ls

# 重新连接
screen -r session_name
```

---

## 🎯 使用示例

### 场景 1：搜索代码并分析

```bash
# 使用 AI 搜索代码
sgpt "找出所有包含 TODO 的 Python 文件"

# AI 会执行：
rg "TODO" --type python

# 然后分析结果
```

### 场景 2：处理数据

```bash
# 让 AI 处理 CSV 数据
sgpt "读取 data.csv，计算平均值，并生成报告"

# AI 会使用 pandas 处理数据
```

### 场景 3：自动化网页抓取

```bash
# 使用 Open Interpreter
interpreter

你：帮我从 HackerNews 首页抓取所有文章标题和链接
AI：[使用 beautifulsoup4 爬取]
AI：[保存到 CSV]
AI：完成！共抓取 30 篇文章
```

### 场景 4：视频下载和处理

```bash
sgpt "下载这个 B站视频的音频，然后去除人声"

# AI 会：
# 1. 使用 yt-dlp 下载音频
# 2. 调用 demucs 去人声（如果可用）
# 3. 保存结果
```

### 场景 5：数据库查询

```bash
sgpt "连接 PostgreSQL，查询最近注册的 10 个用户"

# AI 会使用 psql 或 psycopg2 执行查询
```

---

## 🔄 工具对比：AI 沙盒 vs Claude Code

| 功能 | AI 沙盒 | Claude Code |
|------|---------|-------------|
| **文件操作** | ✅ 完整支持 | ✅ |
| **代码搜索** | ✅ ripgrep, fd, fzf | ✅ |
| **Git 操作** | ✅ git, gh | ✅ |
| **网络搜索** | ✅ duckduckgo, wikipedia | ✅ |
| **Web 抓取** | ✅ requests, bs4, playwright | ✅ |
| **数据库** | ✅ PostgreSQL, SQLite, MongoDB | ✅ |
| **文档处理** | ✅ pandoc, PDF tools | ✅ |
| **多媒体** | ✅ ffmpeg, imagemagick | ⚠️ 有限 |
| **浏览器自动化** | ✅ playwright, selenium | ⚠️ 有限 |
| **AI 能力** | ✅ 本地 Qwen2.5-Coder | ✅ Claude |
| **MCP 集成** | ⚠️ 通过 API 手动实现 | ✅ 原生支持 |

---

## 💡 快速命令参考

```bash
# 搜索代码
rg "pattern" --type python

# 查找文件
fd "*.js"

# 模糊查找
fzf

# 查看文件（语法高亮）
bat file.py

# 目录结构
tree -L 2

# HTTP 请求
http GET https://api.example.com

# JSON 处理
cat data.json | jq '.users[0]'

# 下载视频
yt-dlp "https://www.bilibili.com/video/BV1xxx"

# 数据库查询
sqlite3 db.sqlite "SELECT * FROM users;"

# 文档转换
pandoc input.md -o output.pdf

# Git 操作
gh pr create

# AI 辅助
sgpt "你的需求"
```

---

## 🚀 下一步

这个工具集已经接近 Claude Code 的能力！

**还可以添加：**
- Docker CLI（在沙盒内操作主机 Docker）
- Kubernetes CLI (kubectl)
- Terraform
- Ansible
- 更多语言的开发工具（Node.js, Go, Rust）

根据你的需求，随时可以扩展！
