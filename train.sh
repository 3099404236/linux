#!/bin/bash
# 动物检测模型训练脚本

set -e

echo "======================================"
echo "开始训练 PP-PicoDet 动物检测模型"
echo "======================================"

cd /workspace/PaddleDetection

# 复制配置文件
cp /workspace/picodet_animals.yml configs/picodet/

# 开始训练
python tools/train.py \
    -c configs/picodet/picodet_animals.yml \
    --use_vdl=true \
    --vdl_log_dir=vdl_dir/scalar \
    --eval

echo ""
echo "======================================"
echo "训练完成！"
echo "模型保存在: output/picodet_s_320_coco_lcnet/"
echo "======================================"
