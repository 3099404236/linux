#!/bin/bash
# 列出所有任务

TASKS_BASE=~/projects/tasks

if [ ! -d $TASKS_BASE ]; then
    echo "❌ 任务目录不存在：$TASKS_BASE"
    exit 1
fi

TASK_COUNT=$(ls $TASKS_BASE 2>/dev/null | wc -l)

if [ $TASK_COUNT -eq 0 ]; then
    echo "📂 还没有任何任务"
    echo "💡 使用 new_task.sh 创建新任务"
    exit 0
fi

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📋 所有任务列表（共 $TASK_COUNT 个）"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

for task_id in $(ls -t $TASKS_BASE); do
    TASK_DIR=$TASKS_BASE/$task_id

    # 读取 Git URL
    GIT_URL=""
    if [ -f $TASK_DIR/.task_info ]; then
        GIT_URL=$(grep "Git URL:" $TASK_DIR/.task_info | cut -d' ' -f3-)
    fi

    # 统计文件
    SOURCE_COUNT=$(find $TASK_DIR/source -type f 2>/dev/null | wc -l)
    OUTPUT_COUNT=$(find $TASK_DIR/output -type f 2>/dev/null | wc -l)

    # 计算目录大小
    DIR_SIZE=$(du -sh $TASK_DIR 2>/dev/null | cut -f1)

    echo "📦 $task_id"
    [ -n "$GIT_URL" ] && echo "   🔗 $GIT_URL"
    echo "   📥 源文件：$SOURCE_COUNT 个"
    echo "   📤 输出：$OUTPUT_COUNT 个"
    echo "   💾 大小：$DIR_SIZE"
    echo "   📂 $TASK_DIR"
    echo ""
done

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "💡 查看任务详情："
echo "   cd $TASKS_BASE/<任务ID>"
echo ""
