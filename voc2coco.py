#!/usr/bin/env python3
"""
VOC格式转COCO格式脚本
用于野生动物检测数据集
"""
import os
import json
import xml.etree.ElementTree as ET
from sklearn.model_selection import train_test_split
from tqdm import tqdm

def convert_voc_to_coco(xml_dir, img_dir, output_json, class_names):
    """将VOC格式转换为COCO格式"""

    categories = []
    for i, name in enumerate(class_names):
        categories.append({
            'id': i + 1,
            'name': name,
            'supercategory': 'animal'
        })

    images = []
    annotations = []
    ann_id = 1

    xml_files = [f for f in os.listdir(xml_dir) if f.endswith('.xml')]

    for img_id, xml_file in enumerate(tqdm(xml_files), 1):
        xml_path = os.path.join(xml_dir, xml_file)
        tree = ET.parse(xml_path)
        root = tree.getroot()

        # 图片信息
        filename = root.find('filename').text
        size = root.find('size')
        width = int(size.find('width').text)
        height = int(size.find('height').text)

        images.append({
            'id': img_id,
            'file_name': filename,
            'width': width,
            'height': height
        })

        # 标注信息
        for obj in root.findall('object'):
            name = obj.find('name').text
            if name not in class_names:
                continue

            category_id = class_names.index(name) + 1
            bndbox = obj.find('bndbox')
            xmin = float(bndbox.find('xmin').text)
            ymin = float(bndbox.find('ymin').text)
            xmax = float(bndbox.find('xmax').text)
            ymax = float(bndbox.find('ymax').text)

            w = xmax - xmin
            h = ymax - ymin
            area = w * h

            annotations.append({
                'id': ann_id,
                'image_id': img_id,
                'category_id': category_id,
                'bbox': [xmin, ymin, w, h],
                'area': area,
                'iscrowd': 0
            })
            ann_id += 1

    coco_format = {
        'images': images,
        'annotations': annotations,
        'categories': categories
    }

    with open(output_json, 'w') as f:
        json.dump(coco_format, f, indent=2)

    print(f"转换完成！保存到: {output_json}")
    print(f"图片数量: {len(images)}, 标注数量: {len(annotations)}")
    return [img['file_name'] for img in images]

if __name__ == '__main__':
    # 配置路径
    data_root = '/workspace/wild_animal_temp/wild_animals'
    xml_dir = os.path.join(data_root, 'xml')
    img_dir = os.path.join(data_root, 'image')
    class_names = ['monkey', 'panda', 'wolf']

    # 获取所有文件
    all_files = [f for f in os.listdir(xml_dir) if f.endswith('.xml')]
    print(f"总共 {len(all_files)} 个样本")

    # 划分训练集和验证集 (7:3)
    train_files, val_files = train_test_split(all_files, test_size=0.3, random_state=42)

    print(f"训练集: {len(train_files)} 个样本")
    print(f"验证集: {len(val_files)} 个样本")

    # 创建输出目录
    os.makedirs('/workspace/dataset/annotations', exist_ok=True)
    os.makedirs('/workspace/dataset/images', exist_ok=True)

    # 转换训练集
    print("\n转换训练集...")
    train_xml_dir = '/tmp/train_xml'
    os.makedirs(train_xml_dir, exist_ok=True)
    for f in train_files:
        os.system(f'cp {os.path.join(xml_dir, f)} {train_xml_dir}/')
    convert_voc_to_coco(train_xml_dir, img_dir, '/workspace/dataset/annotations/train.json', class_names)

    # 转换验证集
    print("\n转换验证集...")
    val_xml_dir = '/tmp/val_xml'
    os.makedirs(val_xml_dir, exist_ok=True)
    for f in val_files:
        os.system(f'cp {os.path.join(xml_dir, f)} {val_xml_dir}/')
    convert_voc_to_coco(val_xml_dir, img_dir, '/workspace/dataset/annotations/val.json', class_names)

    # 复制所有图片到dataset目录
    print("\n复制图片...")
    os.system(f'cp {img_dir}/* /workspace/dataset/images/')

    print("\n数据集准备完成！")
    print("目录结构:")
    print("/workspace/dataset/")
    print("  ├── annotations/")
    print("  │   ├── train.json")
    print("  │   └── val.json")
    print("  └── images/")
    print("      └── (所有图片)")
