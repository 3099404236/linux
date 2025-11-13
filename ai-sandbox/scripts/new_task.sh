#!/bin/bash
# 从 Git 仓库创建新任务
# 用法: ./new_task.sh <git_url>

set -e

if [ $# -lt 1 ]; then
    echo "❌ 用法: $0 <git_url>"
    echo ""
    echo "示例:"
    echo "  $0 https://github.com/user/project.git"
    exit 1
fi

GIT_URL=$1
TIMESTAMP=$(date +%Y-%m-%d_%H%M%S)
TASKS_BASE=~/projects/tasks
TASK_DIR=$TASKS_BASE/$TIMESTAMP

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🚀 创建新任务"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# 创建目录结构
echo "📂 创建任务目录：$TASK_DIR"
mkdir -p $TASK_DIR/{source,output}

# 克隆仓库
echo "📥 克隆仓库..."
if git clone --depth 1 $GIT_URL $TASK_DIR/source/ 2>/dev/null; then
    echo "✅ 克隆成功"
else
    echo "❌ 克隆失败，请检查 Git URL"
    rm -rf $TASK_DIR
    exit 1
fi

# 保存任务信息
echo "💾 保存任务信息..."
cat > $TASK_DIR/.task_info << EOF
Git URL: $GIT_URL
Created: $(date '+%Y-%m-%d %H:%M:%S')
Task ID: $TIMESTAMP
Source: $TASK_DIR/source/
Output: $TASK_DIR/output/
EOF

# 统计文件
FILE_COUNT=$(find $TASK_DIR/source -type f | wc -l)

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ 任务创建成功！"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📋 任务 ID：$TIMESTAMP"
echo "📂 任务目录：$TASK_DIR"
echo "📥 源文件：$FILE_COUNT 个文件"
echo "📂 输出目录：$TASK_DIR/output/"
echo ""

# 尝试读取文档
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📖 查找项目文档..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

DOC_FOUND=0

if [ -f $TASK_DIR/source/README.md ]; then
    echo "✅ 找到 README.md"
    echo ""
    cat $TASK_DIR/source/README.md
    DOC_FOUND=1
elif [ -f $TASK_DIR/source/USAGE.md ]; then
    echo "✅ 找到 USAGE.md"
    echo ""
    cat $TASK_DIR/source/USAGE.md
    DOC_FOUND=1
elif [ -f $TASK_DIR/source/readme.md ]; then
    echo "✅ 找到 readme.md"
    echo ""
    cat $TASK_DIR/source/readme.md
    DOC_FOUND=1
fi

if [ $DOC_FOUND -eq 0 ]; then
    echo "⚠️  未找到 README.md 或 USAGE.md"
    echo "💡 请手动查看项目文件：$TASK_DIR/source/"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "💡 下一步："
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "1. 在 VS Code 中打开：$TASK_DIR"
echo "2. 告诉 AI："按照 README 处理任务""
echo "3. 或运行：~/projects/scripts/process_task.sh"
echo ""
