#!/usr/bin/env python3
"""
动物检测预测脚本 - 使用官方推理代码
"""

import sys
import os
import json
import time

# 添加 PaddleDetection 路径（相对路径，适配提交环境）
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(script_dir, 'env', 'PaddleDetection'))

from deploy.python.infer import Detector, get_test_images
import yaml


def main(data_file, output_file):
    """
    主函数
    """
    print("=" * 50)
    print("开始预测...")
    print("=" * 50)
    print(f"输入文件: {data_file}")
    print(f"输出文件: {output_file}")

    # 读取图片列表
    with open(data_file, 'r') as f:
        image_paths = [line.strip() for line in f.readlines()]

    # 处理图片路径：如果是相对路径，转换为基于 data_file 所在目录的路径
    data_dir = os.path.dirname(os.path.abspath(data_file))
    processed_paths = []
    for path in image_paths:
        if not os.path.isabs(path):  # 如果是相对路径
            # 尝试相对于 data_file 所在目录
            abs_path = os.path.join(data_dir, path)
            if os.path.exists(abs_path):
                processed_paths.append(abs_path)
            else:
                # 如果还是找不到，保持原路径（可能在其他位置）
                processed_paths.append(path)
        else:
            processed_paths.append(path)

    image_paths = processed_paths

    print(f"共 {len(image_paths)} 张图片")
    print("=" * 50)

    # 初始化检测器（使用官方 Detector）
    # 禁用优化以兼容旧版本 PaddlePaddle
    detector = Detector(
        model_dir='model',
        device='GPU',
        run_mode='paddle',  # 使用原生 Paddle 推理
        threshold=0.3,
        enable_mkldnn=False,  # 禁用 MKLDNN 优化
        cpu_threads=1  # 使用单线程，避免某些优化
    )

    # 预测
    all_results = []
    start_time = time.time()

    # 预热
    if len(image_paths) > 0:
        _ = detector.predict_image([image_paths[0]], visual=False)

    # 重新计时
    start_time = time.time()

    for idx, image_path in enumerate(image_paths):
        if (idx + 1) % 50 == 0:
            elapsed = time.time() - start_time
            fps = (idx + 1) / elapsed
            print(f"处理进度: {idx + 1}/{len(image_paths)}, FPS: {fps:.2f}")

        # 预测
        results = detector.predict_image([image_path], visual=False)

        # 转换为 COCO 格式
        if results and 'boxes' in results:
            boxes = results['boxes']
            for box in boxes:
                # box 格式: [class_id, score, x1, y1, x2, y2]
                if len(box) >= 6:
                    class_id = int(box[0])
                    score = float(box[1])
                    x1, y1, x2, y2 = box[2:6]

                    if score < 0.3:
                        continue

                    # 转换为 COCO 格式 [x, y, w, h]
                    w = x2 - x1
                    h = y2 - y1

                    all_results.append({
                        'image_id': idx + 1,
                        'category_id': class_id + 1,  # COCO 从 1 开始
                        'bbox': [float(x1), float(y1), float(w), float(h)],
                        'score': score
                    })

    # 计算最终 FPS
    total_time = time.time() - start_time
    fps = len(image_paths) / total_time

    print("=" * 50)
    print(f"预测完成！")
    print(f"总耗时: {total_time:.2f} 秒")
    print(f"FPS: {fps:.2f}")
    print(f"检测到 {len(all_results)} 个目标")
    print("=" * 50)

    # 保存结果
    with open(output_file, 'w') as f:
        json.dump(all_results, f)

    print(f"结果已保存到: {output_file}")

    # 检查 FPS
    if fps < 20:
        print(f"\n⚠️  警告: FPS ({fps:.2f}) 低于要求 (20)")
    else:
        print(f"\n✅ FPS ({fps:.2f}) 满足要求！")


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("用法: python predict.py data.txt result.json")
        sys.exit(1)

    data_file = sys.argv[1]
    output_file = sys.argv[2]

    main(data_file, output_file)
