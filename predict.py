#!/usr/bin/env python3
"""
动物检测预测脚本 - 用于AI Studio比赛提交
要求：
- 读取 data.txt（图片路径列表）
- 输出 result.json（COCO格式检测结果）
- 速度要求：≥20 FPS（V100）
"""

import sys
import os
import json
import time
import paddle
import numpy as np
from PIL import Image
from paddle.inference import Config, create_predictor


class AnimalDetector:
    def __init__(self, model_dir, threshold=0.5):
        """
        初始化检测器
        Args:
            model_dir: 模型文件目录
            threshold: 置信度阈值
        """
        self.threshold = threshold

        # 配置推理引擎
        model_file = os.path.join(model_dir, 'model.pdmodel')
        params_file = os.path.join(model_dir, 'model.pdiparams')

        config = Config(model_file, params_file)
        config.enable_use_gpu(1000, 0)  # GPU显存（MB），设备ID
        config.switch_ir_optim(True)     # 开启IR优化
        config.enable_memory_optim()     # 开启内存优化

        # 创建预测器
        self.predictor = create_predictor(config)

        # 获取输入输出
        self.input_names = self.predictor.get_input_names()
        self.output_names = self.predictor.get_output_names()

        # 类别映射
        self.class_names = ['monkey', 'panda', 'wolf']

        # 预处理参数
        self.mean = [0.485, 0.456, 0.406]
        self.std = [0.229, 0.224, 0.225]
        self.input_size = (320, 320)

    def preprocess(self, image_path):
        """
        图像预处理
        Args:
            image_path: 图片路径
        Returns:
            处理后的图像tensor, 原始图像尺寸
        """
        # 读取图像
        img = Image.open(image_path).convert('RGB')
        orig_size = img.size  # (width, height)

        # Resize
        img = img.resize(self.input_size, Image.BILINEAR)

        # 转numpy并归一化
        img = np.array(img).astype('float32') / 255.0

        # 标准化
        img = (img - self.mean) / self.std

        # HWC -> CHW
        img = img.transpose(2, 0, 1)

        # 增加batch维度
        img = img[np.newaxis, :]

        return img.astype('float32'), orig_size

    def postprocess(self, outputs, orig_size, image_id):
        """
        后处理：将模型输出转换为COCO格式
        Args:
            outputs: 模型输出
            orig_size: 原始图像尺寸 (width, height)
            image_id: 图像ID
        Returns:
            检测结果列表
        """
        results = []

        # 解析输出
        # PaddleDetection输出格式: [class_id, score, x1, y1, x2, y2]
        boxes = outputs[0]  # shape: [N, 6]

        if len(boxes) == 0:
            return results

        # 坐标缩放（从320x320恢复到原始尺寸）
        scale_x = orig_size[0] / self.input_size[0]
        scale_y = orig_size[1] / self.input_size[1]

        for box in boxes:
            class_id = int(box[0])
            score = float(box[1])

            if score < self.threshold:
                continue

            # 坐标
            x1, y1, x2, y2 = box[2:6]

            # 恢复到原始尺寸
            x1 = float(x1 * scale_x)
            y1 = float(y1 * scale_y)
            x2 = float(x2 * scale_x)
            y2 = float(y2 * scale_y)

            # 转换为COCO格式 [x, y, width, height]
            w = x2 - x1
            h = y2 - y1

            result = {
                'image_id': image_id,
                'category_id': class_id + 1,  # COCO格式类别ID从1开始
                'bbox': [x1, y1, w, h],
                'score': score
            }
            results.append(result)

        return results

    def predict(self, image_path, image_id):
        """
        预测单张图片
        Args:
            image_path: 图片路径
            image_id: 图像ID
        Returns:
            检测结果列表
        """
        # 预处理
        img_tensor, orig_size = self.preprocess(image_path)

        # 推理
        input_handle = self.predictor.get_input_handle(self.input_names[0])
        input_handle.copy_from_cpu(img_tensor)

        self.predictor.run()

        # 获取输出
        outputs = []
        for output_name in self.output_names:
            output_handle = self.predictor.get_output_handle(output_name)
            output = output_handle.copy_to_cpu()
            outputs.append(output)

        # 后处理
        results = self.postprocess(outputs, orig_size, image_id)

        return results


def main(data_file, output_file):
    """
    主函数
    Args:
        data_file: 输入文件，包含图片路径列表
        output_file: 输出文件，COCO格式JSON
    """
    print(f"开始预测...")
    print(f"输入文件: {data_file}")
    print(f"输出文件: {output_file}")

    # 初始化检测器
    model_dir = 'model'  # 模型目录
    detector = AnimalDetector(model_dir, threshold=0.3)

    # 读取图片列表
    with open(data_file, 'r') as f:
        image_paths = [line.strip() for line in f.readlines()]

    print(f"共 {len(image_paths)} 张图片需要预测")

    # 预测所有图片
    all_results = []
    start_time = time.time()

    for idx, image_path in enumerate(image_paths):
        if (idx + 1) % 100 == 0:
            print(f"处理进度: {idx + 1}/{len(image_paths)}")

        results = detector.predict(image_path, idx + 1)
        all_results.extend(results)

    # 计算FPS
    total_time = time.time() - start_time
    fps = len(image_paths) / total_time

    print(f"\n预测完成！")
    print(f"总耗时: {total_time:.2f}秒")
    print(f"FPS: {fps:.2f}")
    print(f"检测到 {len(all_results)} 个目标")

    # 保存结果
    with open(output_file, 'w') as f:
        json.dump(all_results, f)

    print(f"结果已保存到: {output_file}")


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("用法: python predict.py data.txt result.json")
        sys.exit(1)

    data_file = sys.argv[1]
    output_file = sys.argv[2]

    main(data_file, output_file)
