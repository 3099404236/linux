#!/usr/bin/env python3
"""
导出推理模型脚本
将训练好的模型导出为推理格式（用于比赛提交）
"""

import os
import sys

def export_model(config_file, weights_file, output_dir):
    """
    导出推理模型
    Args:
        config_file: 配置文件路径
        weights_file: 权重文件路径
        output_dir: 输出目录
    """
    cmd = f"""
cd /workspace/PaddleDetection && \
python tools/export_model.py \
    -c {config_file} \
    -o weights={weights_file} \
    --output_dir={output_dir}
    """

    print(f"导出命令:")
    print(cmd)
    print("\n执行导出...")

    ret = os.system(cmd)

    if ret == 0:
        print(f"\n✅ 模型导出成功！")
        print(f"导出路径: {output_dir}")
        print(f"\n导出的文件:")
        os.system(f"ls -lh {output_dir}")
    else:
        print(f"\n❌ 模型导出失败！")
        sys.exit(1)


if __name__ == '__main__':
    # 配置
    config_file = 'configs/picodet/picodet_animals.yml'
    weights_file = '/workspace/PaddleDetection/output/picodet_animals/best_model'
    output_dir = '/workspace/model'

    print("=" * 50)
    print("开始导出推理模型")
    print("=" * 50)

    export_model(config_file, weights_file, output_dir)

    print("\n" + "=" * 50)
    print("导出完成！")
    print("=" * 50)
