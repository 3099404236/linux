#!/bin/bash
# 打包提交文件脚本

set -e

echo "======================================"
echo "开始打包提交文件"
echo "======================================"

# 使用当前目录
WORK_DIR="$(pwd)"
SUBMIT_DIR="$WORK_DIR/submission"
rm -rf $SUBMIT_DIR
mkdir -p $SUBMIT_DIR/model
mkdir -p $SUBMIT_DIR/env

echo ""
echo "1. 复制模型文件..."
if [ ! -d "$WORK_DIR/model" ]; then
    echo "❌ 错误：找不到 model 目录！"
    exit 1
fi
cp $WORK_DIR/model/model.pdmodel $SUBMIT_DIR/model/
cp $WORK_DIR/model/model.pdiparams $SUBMIT_DIR/model/
cp $WORK_DIR/model/model.pdiparams.info $SUBMIT_DIR/model/
cp $WORK_DIR/model/infer_cfg.yml $SUBMIT_DIR/model/
echo "   已复制: model.pdmodel, model.pdiparams, model.pdiparams.info, infer_cfg.yml"

echo "2. 复制预测脚本..."
cp $WORK_DIR/predict.py $SUBMIT_DIR/

echo "3. 复制 PaddleDetection 依赖库..."
echo "   这可能需要一些时间..."

# 检查并安装 rsync
if ! command -v rsync &> /dev/null; then
    echo "   安装 rsync 工具..."
    apt-get update -qq && apt-get install -y -qq rsync > /dev/null 2>&1
fi

# 使用 rsync 复制，排除不需要的文件
if [ ! -d "$WORK_DIR/PaddleDetection" ]; then
    echo "❌ 错误：找不到 PaddleDetection 目录！"
    exit 1
fi
rsync -a --exclude='.git' \
         --exclude='output' \
         --exclude='vdl_dir' \
         --exclude='__pycache__' \
         --exclude='*.pyc' \
         --exclude='*.pyo' \
         --exclude='dataset' \
         --exclude='logs' \
         --exclude='.idea' \
         $WORK_DIR/PaddleDetection $SUBMIT_DIR/env/
echo "   PaddleDetection 复制完成"

echo "4. 检查模型大小..."
MODEL_SIZE=$(du -m $SUBMIT_DIR/model/model.pdiparams | cut -f1)
echo "模型大小: ${MODEL_SIZE}M"

if [ $MODEL_SIZE -gt 200 ]; then
    echo "❌ 警告：模型大小超过200M！"
else
    echo "✅ 模型大小符合要求"
fi

echo ""
echo "5. 创建压缩包..."
cd $SUBMIT_DIR

# 检查是否有 zip 命令，如果没有就安装
if ! command -v zip &> /dev/null; then
    echo "安装 zip 工具..."
    apt-get update -qq && apt-get install -y -qq zip unzip > /dev/null 2>&1
fi

echo "   打包 model/, env/, predict.py..."
zip -r submission.zip model/ env/ predict.py

echo ""
echo "6. 压缩包信息："
ls -lh submission.zip

echo ""
echo "======================================"
echo "✅ 打包完成！"
echo "======================================"
echo ""
echo "提交文件位置: $SUBMIT_DIR/submission.zip"
echo ""
echo "文件结构:"
unzip -l submission.zip

echo ""
echo "可以将此文件提交到AI Studio平台！"
