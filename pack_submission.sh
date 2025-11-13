#!/bin/bash
# 打包提交文件脚本

set -e

echo "======================================"
echo "开始打包提交文件"
echo "======================================"

# 创建提交目录
SUBMIT_DIR="/workspace/submission"
rm -rf $SUBMIT_DIR
mkdir -p $SUBMIT_DIR/model
mkdir -p $SUBMIT_DIR/env

echo ""
echo "1. 复制模型文件..."
cp /workspace/model/model.pdmodel $SUBMIT_DIR/model/
cp /workspace/model/model.pdiparams $SUBMIT_DIR/model/

echo "2. 复制预测脚本..."
cp /workspace/predict.py $SUBMIT_DIR/

echo "3. 检查模型大小..."
MODEL_SIZE=$(du -m $SUBMIT_DIR/model/model.pdiparams | cut -f1)
echo "模型大小: ${MODEL_SIZE}M"

if [ $MODEL_SIZE -gt 200 ]; then
    echo "❌ 警告：模型大小超过200M！"
else
    echo "✅ 模型大小符合要求"
fi

echo ""
echo "4. 创建压缩包..."
cd $SUBMIT_DIR
zip -r submission.zip model/ predict.py

echo ""
echo "5. 压缩包信息："
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
