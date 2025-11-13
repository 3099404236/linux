# AI 安全沙盒环境

让 AI 在 Docker 容器内自由执行命令，但无法影响主机系统。

## 🔒 安全特性

### ✅ 容器内 AI 可以：
- 执行任何命令（bash、python 等）
- 安装软件包
- 修改 `/workspace` 目录的文件
- 访问主机的 Ollama 服务（调用 AI 模型）
- 读取主机的指定目录（只读）

### ❌ 容器内 AI 不能：
- 访问主机的其他文件
- 修改主机系统
- 影响其他 Docker 容器
- 突破资源限制（CPU/内存）
- 获取 root 特权
- 访问主机的敏感信息

## 🚀 使用方法

### 1. 构建镜像

```bash
cd ~/linux/ai-sandbox
docker compose build
```

### 2. 启动沙盒

```bash
docker compose up -d
```

### 3. 进入沙盒

```bash
docker compose exec ai-sandbox bash
```

### 4. 在沙盒内使用 AI

#### 方案 A：Shell-GPT（推荐）

```bash
# 生成命令（预览，不执行）
sgpt "找出最大的 5 个文件"

# 生成命令并询问是否执行
sgpt --shell "列出所有 Python 进程"

# 直接执行（危险！仅在沙盒内使用）
sgpt --execute "创建一个测试目录"
```

#### 方案 B：Open Interpreter

```bash
# 启动交互式 AI
interpreter --model ollama/qwen2.5-coder:32b

# 然后和 AI 对话
你：帮我创建一个 Python 脚本，批量重命名文件
AI：[生成代码并执行]
```

#### 方案 C：Aider（代码编辑助手）

```bash
# 启动 Aider
aider --model ollama/qwen2.5-coder:32b

# AI 可以帮你修改代码、运行测试等
```

## 📂 目录说明

```
主机目录                    容器内路径              权限
~/linux/ai-sandbox/workspace → /workspace         读写（AI 可修改）
~/music                      → /readonly/music     只读（AI 只能读）
~/Downloads                  → /readonly/downloads 只读（AI 只能读）
```

### 工作区说明

- `/workspace` - AI 的自由空间，可以随意创建、修改、删除文件
- `/readonly/*` - 主机文件的只读镜像，AI 只能查看不能修改

## 🎯 使用场景示例

### 场景 1：让 AI 处理文件

```bash
# 1. 进入沙盒
docker compose exec ai-sandbox bash

# 2. 复制文件到工作区
cp /readonly/music/song.mp3 /workspace/

# 3. 让 AI 处理
sgpt --execute "分析这个 mp3 文件的元数据"
```

### 场景 2：让 AI 写代码并测试

```bash
# 启动 Aider
docker compose exec ai-sandbox aider --model ollama/qwen2.5-coder:32b

# 对话
你：写个 Python 脚本，批量转换图片格式
AI：[生成代码]
AI：[运行测试]
AI：代码已保存到 /workspace/convert.py
```

### 场景 3：批量下载视频音频

```bash
# 在沙盒内使用 yt-dlp
docker compose exec ai-sandbox bash

# 安装 yt-dlp（在沙盒内）
pip install yt-dlp

# 让 AI 生成下载命令
sgpt "用 yt-dlp 下载 B站视频音频"
```

## ⚙️ 配置调整

### 调整资源限制

编辑 `docker-compose.yml`：

```yaml
deploy:
  resources:
    limits:
      cpus: '8'        # 增加到 8 核
      memory: 16G      # 增加到 16GB
```

### 添加更多只读目录

```yaml
volumes:
  - ~/Documents:/readonly/documents:ro
  - ~/Pictures:/readonly/pictures:ro
```

### 允许 GPU 访问（用于机器学习）

```yaml
deploy:
  resources:
    reservations:
      devices:
        - driver: nvidia
          count: 1
          capabilities: [gpu]
```

## 🔐 安全最佳实践

1. **永远不要在沙盒外运行 AI 自动执行命令**
2. **定期检查 `/workspace` 目录**，确保没有生成恶意文件
3. **只挂载必要的目录**，且尽量使用只读模式
4. **定期更新容器镜像**
5. **监控资源使用**，防止滥用

## 🛑 停止和清理

```bash
# 停止沙盒
docker compose down

# 删除工作区（谨慎！）
rm -rf workspace/*

# 删除镜像
docker rmi ai-sandbox:latest
```

## 📝 快捷脚本

创建快捷命令 `~/bin/ai`：

```bash
#!/bin/bash
docker compose -f ~/linux/ai-sandbox/docker-compose.yml exec ai-sandbox sgpt "$@"
```

使用：
```bash
chmod +x ~/bin/ai
ai "找出最大的文件"
```

## ⚠️ 注意事项

1. **不要给容器 `--privileged` 权限**
2. **不要挂载敏感目录**（如 `/etc`, `/var`, `~/.ssh`）
3. **不要禁用安全选项**（如 `no-new-privileges`）
4. **定期审查 AI 生成的代码**
5. **不要在生产环境使用自动执行功能**

## 🎓 学习资源

- Shell-GPT: https://github.com/TheR1D/shell_gpt
- Open Interpreter: https://github.com/KillianLucas/open-interpreter
- Aider: https://github.com/paul-gauthier/aider
- Docker 安全: https://docs.docker.com/engine/security/

---

**这样你就可以放心让 AI 执行命令了！即使 AI 出错也不会影响主机系统。**
