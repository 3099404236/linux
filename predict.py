#!/usr/bin/env python3
"""
动物检测预测脚本 - 优化版
基于 PaddleDetection 官方推理，优化速度
"""

import sys
import os
import json
import time
import yaml
import numpy as np
import cv2
from collections import defaultdict

import paddle
from paddle.inference import Config, create_predictor
from ppdet.core.workspace import load_config, merge_config
from ppdet.data.transform import Compose
from ppdet.utils.checkpoint import load_weight
from ppdet.modeling.architectures import BaseArch


class Detector:
    def __init__(self, model_dir, threshold=0.3, device='GPU',
                 enable_mkldnn=False, cpu_threads=1,
                 trt_min_shape=1, trt_max_shape=1280, trt_opt_shape=640):
        """
        初始化检测器
        """
        self.threshold = threshold

        # 加载配置
        cfg_file = os.path.join(model_dir, 'infer_cfg.yml')
        with open(cfg_file) as f:
            self.config = yaml.safe_load(f)

        # 配置推理引擎
        model_file = os.path.join(model_dir, 'model.pdmodel')
        params_file = os.path.join(model_dir, 'model.pdiparams')

        config = Config(model_file, params_file)

        # GPU 配置
        if device == 'GPU':
            config.enable_use_gpu(1000, 0)

        # 优化配置（提速）
        config.switch_ir_optim(True)
        config.enable_memory_optim()
        config.disable_glog_info()

        # TensorRT 加速（如果支持）
        if device == 'GPU':
            # 启用 TensorRT
            precision_mode = paddle.inference.PrecisionType.Float32
            config.enable_tensorrt_engine(
                workspace_size=1 << 30,
                max_batch_size=1,
                min_subgraph_size=40,
                precision_mode=precision_mode,
                use_static=False,
                use_calib_mode=False)

            # 设置动态 shape
            min_input_shape = {'image': [1, 3, trt_min_shape, trt_min_shape],
                               'scale_factor': [1, 2]}
            max_input_shape = {'image': [1, 3, trt_max_shape, trt_max_shape],
                               'scale_factor': [1, 2]}
            opt_input_shape = {'image': [1, 3, trt_opt_shape, trt_opt_shape],
                               'scale_factor': [1, 2]}
            config.set_trt_dynamic_shape_info(
                min_input_shape, max_input_shape, opt_input_shape)

        # 创建预测器
        self.predictor = create_predictor(config)

        # 获取输入输出名称
        self.input_names = self.predictor.get_input_names()
        self.output_names = self.predictor.get_output_names()

        # 预处理配置
        self.preprocess_ops = self._get_preprocess_ops()

    def _get_preprocess_ops(self):
        """获取预处理操作"""
        preprocess_list = []
        for op_info in self.config['Preprocess']:
            op_type = list(op_info.keys())[0]
            op_info[op_type]['name'] = op_type
            preprocess_list.append(op_info[op_type])
        return Compose(preprocess_list)

    def preprocess(self, image_path):
        """
        预处理图像
        """
        # 读取图像
        im = cv2.imread(image_path)
        if im is None:
            raise ValueError(f"Cannot read image: {image_path}")

        # 应用预处理
        data = {'image': im}
        data = self.preprocess_ops(data)

        return data

    def postprocess(self, np_boxes, np_boxes_num, im_shape, scale_factor, threshold):
        """
        后处理
        """
        expect_boxes = (np_boxes[:, 1] > threshold) & (np_boxes[:, 0] > -1)
        np_boxes = np_boxes[expect_boxes, :]

        results = []
        for box in np_boxes:
            class_id = int(box[0])
            score = float(box[1])

            if score < threshold:
                continue

            # 坐标 [x1, y1, x2, y2]
            xmin, ymin, xmax, ymax = box[2:6]

            # 转换为 COCO 格式 [x, y, w, h]
            w = xmax - xmin
            h = ymax - ymin

            results.append({
                'class_id': class_id,
                'score': score,
                'bbox': [float(xmin), float(ymin), float(w), float(h)]
            })

        return results

    def predict(self, image_path):
        """
        预测单张图片
        """
        # 预处理
        data = self.preprocess(image_path)

        # 准备输入
        inputs = {}
        inputs['image'] = np.array([data['image']]).astype('float32')
        inputs['im_shape'] = np.array([data['im_shape']]).astype('float32')
        inputs['scale_factor'] = np.array([data['scale_factor']]).astype('float32')

        # 推理
        for input_name in self.input_names:
            input_tensor = self.predictor.get_input_handle(input_name)
            input_tensor.copy_from_cpu(inputs[input_name])

        self.predictor.run()

        # 获取输出
        np_boxes = self.predictor.get_output_handle(self.output_names[0]).copy_to_cpu()
        np_boxes_num = self.predictor.get_output_handle(self.output_names[1]).copy_to_cpu()

        # 后处理
        results = self.postprocess(
            np_boxes, np_boxes_num,
            data['im_shape'], data['scale_factor'],
            self.threshold)

        return results


def main(data_file, output_file):
    """
    主函数
    """
    print("=" * 50)
    print("开始预测...")
    print("=" * 50)
    print(f"输入文件: {data_file}")
    print(f"输出文件: {output_file}")

    # 初始化检测器
    model_dir = 'model'
    detector = Detector(
        model_dir=model_dir,
        threshold=0.3,
        device='GPU',
        trt_min_shape=320,
        trt_max_shape=640,
        trt_opt_shape=320
    )

    # 读取图片列表
    with open(data_file, 'r') as f:
        image_paths = [line.strip() for line in f.readlines()]

    print(f"共 {len(image_paths)} 张图片")
    print("=" * 50)

    # 预测
    all_results = []
    start_time = time.time()

    # 预热（第一次推理会慢，预热后才准确）
    if len(image_paths) > 0:
        _ = detector.predict(image_paths[0])

    # 重新计时
    start_time = time.time()

    for idx, image_path in enumerate(image_paths):
        if (idx + 1) % 50 == 0:
            elapsed = time.time() - start_time
            fps = (idx + 1) / elapsed
            print(f"处理进度: {idx + 1}/{len(image_paths)}, FPS: {fps:.2f}")

        results = detector.predict(image_path)

        # 转换为 COCO 格式
        for result in results:
            all_results.append({
                'image_id': idx + 1,
                'category_id': result['class_id'] + 1,  # COCO 从 1 开始
                'bbox': result['bbox'],
                'score': result['score']
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
        print(f"\n⚠️  警告: FPS ({fps:.2f}) 低于要求 (20)，可能无法通过评测！")
    else:
        print(f"\n✅ FPS ({fps:.2f}) 满足要求！")


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("用法: python predict.py data.txt result.json")
        sys.exit(1)

    data_file = sys.argv[1]
    output_file = sys.argv[2]

    main(data_file, output_file)
