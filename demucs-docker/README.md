# Demucs 人声分离 Docker 版本

基于 GPU 加速的音乐人声/伴奏分离工具

## 🎵 功能

- ✅ 分离人声和伴奏
- ✅ 4 轨分离：人声、鼓、贝斯、其他乐器
- ✅ GPU 加速（需要 NVIDIA GPU）
- ✅ 支持多种音频格式（mp3, wav, flac 等）

## 🚀 快速开始

### 1. 构建镜像

```bash
cd ~/linux/demucs-docker
docker compose build
```

### 2. 准备音乐文件

将你的音乐文件放到 `~/music/` 目录

```bash
mkdir -p ~/music
cp 你的歌曲.mp3 ~/music/
```

### 3. 运行分离

#### 方法 A：使用 docker compose（推荐）

```bash
# 启动容器
docker compose up -d

# 进入容器
docker compose exec demucs bash

# 在容器内运行分离（去人声，只保留伴奏）
demucs --two-stems=vocals -o /audio/output /audio/input/你的歌曲.mp3

# 结果会保存在 ~/music/separated/ 目录
```

#### 方法 B：直接运行（一行命令）

```bash
docker compose run --rm demucs \
  demucs --two-stems=vocals -o /audio/output /audio/input/你的歌曲.mp3
```

## 📖 使用说明

### 基本命令

```bash
# 1. 分离人声和伴奏（最常用）
demucs --two-stems=vocals -o /audio/output /audio/input/歌曲.mp3
# 输出：
#   - vocals.wav     (人声)
#   - no_vocals.wav  (伴奏) ← 你要的卡拉OK伴奏

# 2. 4轨完整分离（人声、鼓、贝斯、其他）
demucs -o /audio/output /audio/input/歌曲.mp3

# 3. 批量处理整个目录
demucs --two-stems=vocals -o /audio/output /audio/input/*.mp3

# 4. 使用最高质量模型（htdemucs_ft，更慢但效果更好）
demucs --two-stems=vocals -n htdemucs_ft -o /audio/output /audio/input/歌曲.mp3
```

### 模型选择

- `htdemucs` - 默认，质量好，速度快（推荐）
- `htdemucs_ft` - 微调版，质量最好，速度稍慢
- `mdx_extra` - 额外训练的模型，适合某些特殊歌曲

```bash
# 使用特定模型
demucs -n htdemucs_ft --two-stems=vocals /audio/input/歌曲.mp3
```

## 📂 目录结构

```
~/music/                    # 输入目录（你的音乐文件）
└── 歌曲.mp3

~/music/separated/          # 输出目录（分离结果）
└── htdemucs/
    └── 歌曲/
        ├── vocals.wav      # 人声
        ├── no_vocals.wav   # 伴奏
        ├── drums.wav       # 鼓（4轨模式）
        ├── bass.wav        # 贝斯（4轨模式）
        └── other.wav       # 其他（4轨模式）
```

## ⚙️ 高级选项

```bash
# 指定输出格式
demucs --two-stems=vocals --mp3 --mp3-bitrate=320 /audio/input/歌曲.mp3

# 调整处理质量和速度
demucs --two-stems=vocals --shifts=1 /audio/input/歌曲.mp3
# shifts 越大质量越好但越慢（默认为1，可设置0-10）

# 使用 CPU（如果没有 GPU）
demucs --two-stems=vocals --device cpu /audio/input/歌曲.mp3
```

## 🎯 常见使用场景

### 场景 1：制作卡拉OK伴奏

```bash
# 只保留伴奏，去除人声
demucs --two-stems=vocals -o /audio/output /audio/input/歌曲.mp3
# 使用 no_vocals.wav 作为伴奏
```

### 场景 2：提取无损人声

```bash
# 只保留人声
demucs --two-stems=vocals -o /audio/output /audio/input/歌曲.mp3
# 使用 vocals.wav
```

### 场景 3：重新混音

```bash
# 分离所有音轨
demucs -o /audio/output /audio/input/歌曲.mp3
# 得到 vocals, drums, bass, other 四个音轨
# 可以用 DAW 重新混音
```

## 🔧 故障排查

### 1. GPU 不可用

检查 GPU：
```bash
docker compose exec demucs nvidia-smi
```

如果失败，确保：
- NVIDIA 驱动已安装
- nvidia-docker2 已安装

### 2. 内存不足

如果处理大文件时内存不足，可以：
```bash
# 减小 shifts 值
demucs --two-stems=vocals --shifts=0 /audio/input/歌曲.mp3
```

### 3. 速度太慢

```bash
# 使用更快的模型
demucs -n mdx --two-stems=vocals /audio/input/歌曲.mp3
```

## 📊 性能参考

在 22GB 显存的 GPU 上：
- 一首 3-5 分钟的歌曲：约 10-30 秒
- 使用 htdemucs 模型
- GPU 占用：约 2-4GB

## 💡 技巧

1. **批量处理**：可以用通配符一次处理多个文件
   ```bash
   demucs --two-stems=vocals /audio/input/*.mp3
   ```

2. **保持原始音质**：输出为 WAV 格式保证无损

3. **节省空间**：如果只需要伴奏，处理完可以删除人声文件

4. **预览效果**：先用一小段音频测试效果，满意再处理完整文件

## 🛑 停止和清理

```bash
# 停止容器
docker compose down

# 删除镜像（如果不需要了）
docker rmi demucs-gpu:latest
```

## 📞 支持的音频格式

- MP3
- WAV
- FLAC
- OGG
- M4A
- WMA

## 🎓 更多信息

- Demucs 官方文档：https://github.com/facebookresearch/demucs
- 模型详细说明：https://github.com/facebookresearch/demucs#models
