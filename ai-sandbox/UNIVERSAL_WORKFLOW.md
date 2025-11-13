# 通用项目自动化工作流

让 AI 自动处理任何 Git 项目，按时间归档结果。

---

## 📁 标准目录结构

```
~/projects/
├── tasks/                          # 所有任务
│   ├── 2025-01-15_143022/         # 第一个任务（按时间命名）
│   │   ├── source/                # Git 仓库内容
│   │   ├── output/                # 处理结果
│   │   └── .task_info             # 任务信息（Git链接等）
│   ├── 2025-01-20_091234/         # 第二个任务
│   │   ├── source/
│   │   ├── output/
│   │   └── .task_info
│   └── 2025-01-25_164532/         # 第三个任务
│       ├── source/
│       ├── output/
│       └── .task_info
└── scripts/
    ├── new_task.sh                 # 创建新任务
    └── ai_helper.sh                # AI 辅助脚本
```

---

## 🚀 使用方式

### 方式 1：简单版（直接告诉 AI）

```
你：从 https://github.com/user/ppt-files.git 创建新任务

AI：[自动创建时间戳目录]
    [克隆仓库到 source/]
    [读取 README.md]

    📂 任务已创建：~/projects/tasks/2025-01-15_143022/
    📄 仓库已克隆到：source/
    📖 README 内容：
    [显示 README]

你：按照 README 处理这个任务

AI：[根据 README 执行命令]
    [结果保存到 output/]
    ✅ 处理完成！
```

### 方式 2：使用脚本（更标准）

```bash
# 在 VS Code 终端或 AI 沙盒中

# 创建新任务
~/projects/scripts/new_task.sh https://github.com/user/ppt-files.git

# AI 处理（读取并执行 README）
~/projects/scripts/ai_helper.sh
```

---

## 📝 AI 工作流程

### 第 1 步：创建新任务

```bash
你：从 https://github.com/xxx/project.git 创建新任务

AI 自动执行：
1. TIMESTAMP=$(date +%Y-%m-%d_%H%M%S)
2. mkdir -p ~/projects/tasks/$TIMESTAMP/{source,output}
3. git clone <链接> ~/projects/tasks/$TIMESTAMP/source/
4. echo "Git: <链接>" > ~/projects/tasks/$TIMESTAMP/.task_info
5. cd ~/projects/tasks/$TIMESTAMP/source
6. cat README.md  # 读取文档
```

### 第 2 步：执行处理

```bash
你：按照 README 处理

AI 自动执行：
1. 读取 README.md 或 USAGE.md
2. 识别处理步骤（启动 Docker、运行脚本等）
3. 执行命令
4. 结果保存到 ../output/
```

### 第 3 步：查看结果

```bash
你：显示处理结果

AI：
📊 任务信息：
- 时间：2025-01-15 14:30:22
- Git：https://github.com/xxx/project.git
- 源文件：15 个文件
- 输出：15 个结果文件

📂 输出目录：~/projects/tasks/2025-01-15_143022/output/
```

---

## 🤖 AI 示例对话

### 示例 1：PPT OCR

```
你：从 https://github.com/user/ppt-batch1.git 创建新任务

AI：✅ 任务已创建：~/projects/tasks/2025-01-15_143022/
    📥 已克隆 12 个 PPT 文件
    📖 README 说明：需要用 PaddleOCR 处理

你：按照 README 处理

AI：🐳 启动 paddleocr 容器...
    🔄 处理 12 个 PPT...
    ✅ 完成！结果在 output/ 目录
```

### 示例 2：LaTeX 文档

```
你：从 https://github.com/user/paper-draft.git 创建新任务

AI：✅ 任务已创建：~/projects/tasks/2025-01-20_091234/
    📥 已克隆 LaTeX 源文件
    📖 README 说明：使用 xelatex 编译

你：按照 README 处理

AI：📝 编译 main.tex...
    ✅ 完成！PDF 已生成：output/main.pdf
```

### 示例 3：数据处理

```
你：从 https://github.com/user/data-analysis.git 创建新任务

AI：✅ 任务已创建：~/projects/tasks/2025-01-25_164532/
    📥 已克隆数据集和处理脚本
    📖 README 说明：运行 python process.py

你：按照 README 处理

AI：🐍 运行 Python 脚本...
    📊 处理 1000 条数据...
    ✅ 完成！结果在 output/results.csv
```

---

## 🛠️ 脚本实现

### new_task.sh（创建新任务）

```bash
#!/bin/bash
# 从 Git 仓库创建新任务

if [ $# -lt 1 ]; then
    echo "用法: $0 <git_url>"
    exit 1
fi

GIT_URL=$1
TIMESTAMP=$(date +%Y-%m-%d_%H%M%S)
TASK_DIR=~/projects/tasks/$TIMESTAMP

echo "📂 创建任务目录：$TASK_DIR"
mkdir -p $TASK_DIR/{source,output}

echo "📥 克隆仓库..."
git clone --depth 1 $GIT_URL $TASK_DIR/source/

echo "💾 保存任务信息..."
cat > $TASK_DIR/.task_info << EOF
Git URL: $GIT_URL
Created: $(date)
Task Dir: $TASK_DIR
EOF

echo "📖 读取 README..."
if [ -f $TASK_DIR/source/README.md ]; then
    cat $TASK_DIR/source/README.md
elif [ -f $TASK_DIR/source/USAGE.md ]; then
    cat $TASK_DIR/source/USAGE.md
else
    echo "⚠️  未找到 README.md 或 USAGE.md"
fi

echo ""
echo "✅ 任务已创建：$TASK_DIR"
echo "📂 源文件：$TASK_DIR/source/"
echo "📂 输出目录：$TASK_DIR/output/"
```

### ai_helper.sh（AI 辅助处理）

```bash
#!/bin/bash
# AI 辅助脚本 - 显示当前任务信息

# 查找最新任务
LATEST_TASK=$(ls -t ~/projects/tasks/ | head -1)
TASK_DIR=~/projects/tasks/$LATEST_TASK

if [ -z "$LATEST_TASK" ]; then
    echo "❌ 没有找到任务"
    exit 1
fi

echo "📋 当前任务：$LATEST_TASK"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# 显示任务信息
if [ -f $TASK_DIR/.task_info ]; then
    cat $TASK_DIR/.task_info
    echo ""
fi

# 显示文档
echo "📖 文档内容："
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
if [ -f $TASK_DIR/source/README.md ]; then
    cat $TASK_DIR/source/README.md
elif [ -f $TASK_DIR/source/USAGE.md ]; then
    cat $TASK_DIR/source/USAGE.md
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📂 源文件：$TASK_DIR/source/"
echo "📂 输出目录：$TASK_DIR/output/"
echo ""
echo "💡 接下来，请告诉 AI："
echo "   \"按照 README 处理当前任务\""
```

---

## 💡 最佳实践

### 在 Git 仓库中包含说明文档

每个 Git 仓库应该包含 `README.md` 或 `USAGE.md`：

```markdown
# 项目说明

## 处理方法

1. 启动 Docker 容器
   ```bash
   docker run -d --name myocr -v $(pwd):/data ocr:latest
   ```

2. 运行处理脚本
   ```bash
   docker exec myocr python process.py /data/input /data/output
   ```

3. 结果说明
   - 输出在 output/ 目录
   - 每个输入文件对应一个 .txt 结果
```

### AI 会自动：
1. 读取文档
2. 理解步骤
3. 执行命令（替换路径为实际路径）
4. 保存结果

---

## 🔄 完整工作流示例

```
# 第一个项目
你：从 https://github.com/user/batch1.git 创建新任务
AI：[创建 2025-01-15_143022/]

你：按照 README 处理
AI：[读取 README] [执行] [结果在 output/]

# 第二个项目（几天后）
你：从 https://github.com/user/batch2.git 创建新任务
AI：[创建 2025-01-20_091234/]

你：按照 README 处理
AI：[读取 README] [执行] [结果在 output/]

# 查看所有历史
你：列出所有任务
AI：
    2025-01-15_143022/  (batch1, 已完成)
    2025-01-20_091234/  (batch2, 已完成)
    2025-01-25_164532/  (batch3, 已完成)
```

---

## 🎯 总结

### 你需要做的：
1. 告诉 AI Git 链接
2. 说"按照 README 处理"

### AI 会自动：
1. 创建时间戳目录
2. 克隆仓库
3. 读取 README
4. 执行处理
5. 保存结果

### 优势：
- ✅ 每个任务独立，不会混淆
- ✅ 自动按时间归档
- ✅ 可以处理任何 Git 仓库
- ✅ 不需要手动管理文件
- ✅ 历史可追溯

---

**现在你只需要把这个通用工作流告诉 AI，它就知道怎么做了！**
