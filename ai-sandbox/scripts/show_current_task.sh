#!/bin/bash
# 显示当前任务信息（最新的任务）

set -e

TASKS_BASE=~/projects/tasks

if [ ! -d $TASKS_BASE ]; then
    echo "❌ 任务目录不存在：$TASKS_BASE"
    exit 1
fi

# 查找最新任务
LATEST_TASK=$(ls -t $TASKS_BASE 2>/dev/null | head -1)

if [ -z "$LATEST_TASK" ]; then
    echo "❌ 没有找到任何任务"
    echo "💡 使用 new_task.sh 创建新任务"
    exit 1
fi

TASK_DIR=$TASKS_BASE/$LATEST_TASK

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📋 当前任务信息"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# 显示任务信息
if [ -f $TASK_DIR/.task_info ]; then
    cat $TASK_DIR/.task_info
else
    echo "⚠️  未找到任务信息文件"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📊 文件统计"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
SOURCE_COUNT=$(find $TASK_DIR/source -type f 2>/dev/null | wc -l)
OUTPUT_COUNT=$(find $TASK_DIR/output -type f 2>/dev/null | wc -l)
echo "📥 源文件：$SOURCE_COUNT 个"
echo "📤 输出文件：$OUTPUT_COUNT 个"

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📖 项目文档"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if [ -f $TASK_DIR/source/README.md ]; then
    cat $TASK_DIR/source/README.md
elif [ -f $TASK_DIR/source/USAGE.md ]; then
    cat $TASK_DIR/source/USAGE.md
elif [ -f $TASK_DIR/source/readme.md ]; then
    cat $TASK_DIR/source/readme.md
else
    echo "⚠️  未找到文档"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📂 目录路径"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "源文件：$TASK_DIR/source/"
echo "输出：  $TASK_DIR/output/"
echo ""
