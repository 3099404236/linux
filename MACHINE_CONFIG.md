# Linux 工作站配置说明

> 本文档记录了 czf 的 Linux 工作站的所有个性化配置和特殊设置，供 AI 助手快速了解机器环境。

---

## 📋 基本信息

- **操作系统**: Ubuntu 22.04 LTS
- **用户名**: `czf`
- **密码**: `qwertyuiop`
- **主机名**: `hello`
- **局域网 IP**: `192.168.1.109`
- **显卡**: NVIDIA GPU (支持 CUDA 11.7)
- **架构**: x86_64

---

## 🌐 网络配置

### Clash 代理配置

**服务状态**:
- ✅ 已配置 systemd 服务，开机自启
- ✅ 已设置系统代理
- ✅ 默认使用 Global 模式 + 美国 02 节点

**代理端口**:
```
HTTP 代理:    127.0.0.1:7890
SOCKS5 代理:  127.0.0.1:7891
RESTful API:  127.0.0.1:9090
```

**配置文件位置**:
```
~/.config/clash/config.yaml
~/.config/clash/geoip.metadb
~/.config/clash/geosite.dat
```

**服务管理命令**:
```bash
# 查看状态
sudo systemctl status clash

# 启动/停止/重启
sudo systemctl start/stop/restart clash

# 查看日志
sudo journalctl -u clash -f
```

**切换节点**:
```bash
# 查看所有节点
curl -s http://127.0.0.1:9090/proxies/GLOBAL | python3 -c "import sys,json; [print(p) for p in json.load(sys.stdin)['all']]"

# 切换节点
curl -X PUT http://127.0.0.1:9090/proxies/GLOBAL -H "Content-Type: application/json" -d '{"name":"节点名称"}'

# 切换模式 (rule/global/direct)
curl -X PUT http://127.0.0.1:9090/configs -H "Content-Type: application/json" -d '{"mode":"global"}'
```

**系统代理设置**:
```bash
# 已永久配置，开机自动生效
# 手动检查:
gsettings get org.gnome.system.proxy mode  # 应该返回 'manual'
```

### 旧版代理（Clash Verge）

⚠️ **注意**: 还有图形界面的 Clash Verge 运行在端口 `7897`，但推荐使用命令行版本（端口 7890）。

---

## 🐳 Docker 配置

### 动物检测项目容器

**容器信息**:
```
容器名称:     paddle_animal
镜像:         paddlepaddle/paddle:2.5.1-gpu-cuda11.7
GPU 支持:     已启用 (--gpus all)
```

**重要目录映射**:
```
主机:    ~/animal_detection  →  容器: /workspace
```

**常用命令**:
```bash
# 进入容器
docker exec -it paddle_animal bash

# 启动/停止/重启容器
docker start/stop/restart paddle_animal

# 查看容器状态
docker ps -a | grep paddle_animal

# 复制文件 (主机 → 容器)
docker cp /path/on/host paddle_animal:/path/in/container

# 复制文件 (容器 → 主机)
docker cp paddle_animal:/path/in/container /path/on/host
```

### 容器内网络配置

⚠️ **重要**: 容器默认无法访问外网，需要手动配置代理！

```bash
# 在容器内运行以下命令
export http_proxy=http://192.168.1.109:7890
export https_proxy=http://192.168.1.109:7890
export all_proxy=socks5://192.168.1.109:7891

# 测试网络
curl -I https://www.google.com
```

**永久配置** (可选):
```bash
# 在容器内添加到 ~/.bashrc
echo 'export http_proxy=http://192.168.1.109:7890' >> ~/.bashrc
echo 'export https_proxy=http://192.168.1.109:7890' >> ~/.bashrc
source ~/.bashrc
```

---

## 🖥️ 显示器配置问题（已修复）

### ⚠️ 历史问题：显示器黑屏

**原因**: 自定义的 `smart-display.sh` 脚本误判显示器状态

**已采取的修复措施**:
```bash
# 1. 禁用了自动显示器检测服务
sudo systemctl disable smart-display.service
sudo systemctl stop smart-display.service

# 2. 删除了虚拟显示配置
sudo rm -f /etc/X11/xorg.conf.d/20-virtual.conf

# 3. 备份保留在
/etc/X11/xorg.conf.d/20-virtual.conf.backup
```

**相关文件**:
- `/usr/local/bin/smart-display.sh` - 自动显示器检测脚本（已禁用）
- `/etc/systemd/system/smart-display.service` - systemd 服务（已禁用）

**如果需要恢复远程无显示器访问**:
请谨慎重新启用 `smart-display.service`，并确保脚本逻辑正确。

---

## 📂 项目结构

### 动物检测项目

**主机路径**: `~/animal_detection/`

**目录结构**:
```
~/animal_detection/
├── PaddleDetection/          # PaddleDetection 框架
├── dataset/                  # 数据集
│   ├── annotations/
│   │   ├── train.json
│   │   └── val.json
│   └── images/
├── model/                    # 训练好的模型
│   ├── model.pdmodel
│   ├── model.pdiparams
│   ├── model.pdiparams.info
│   └── infer_cfg.yml
├── voc2coco.py              # VOC 转 COCO 格式脚本
├── picodet_animals.yml      # 训练配置
├── train.sh                 # 训练脚本
├── export_model.py          # 模型导出脚本
├── predict.py               # 预测脚本
└── pack_submission.sh       # 打包提交脚本
```

**容器内路径**: `/workspace/` (与 `~/animal_detection/` 映射)

---

## 🛠️ 常用工具和软件

### 已安装的命令行工具

```bash
clash          # Clash Meta 代理工具 (/usr/local/bin/clash)
docker         # Docker 容器引擎
python3        # Python 3.x
git            # 版本控制
wget/curl      # 下载工具
vim/nano       # 文本编辑器
```

### GitHub 仓库

**代码仓库**:
- 主仓库: `https://github.com/3099404236/linux.git`
- 配置仓库: `https://github.com/3099404236/linuxset.git`

**Git 配置**:
```bash
# 检查 Git 配置
git config --global user.name
git config --global user.email
```

---

## ⚡ 性能优化建议

### GPU 加速

- ✅ NVIDIA GPU 已配置
- ✅ CUDA 11.7 可用
- ✅ Docker 容器支持 GPU (`--gpus all`)

### 推理加速

- TensorRT FP16 加速已配置 (predict.py)
- 首次运行需要 1-2 分钟构建优化引擎

---

## 🚨 注意事项

### 1. 网络代理问题

**症状**: 无法访问 GitHub、Google 等国外网站

**解决方案**:
```bash
# 确认 Clash 服务运行
sudo systemctl status clash

# 确认系统代理已设置
gsettings get org.gnome.system.proxy mode

# 在终端临时启用代理
export http_proxy=http://127.0.0.1:7890
export https_proxy=http://127.0.0.1:7890
```

### 2. Docker 容器网络问题

**症状**: 容器内无法访问外网

**解决方案**: 在容器内设置代理环境变量（见上文 Docker 配置章节）

### 3. 显示器黑屏问题

**症状**: 开机后显示器黑屏，无图形界面

**解决方案**:
```bash
# SSH 登录后执行
sudo rm -f /etc/X11/xorg.conf.d/20-virtual.conf
sudo systemctl restart gdm
```

### 4. GitHub raw.githubusercontent.com 缓存

**症状**: wget 下载的脚本是旧版本

**解决方案**:
```bash
# 添加时间戳参数绕过缓存
wget -O file.sh "https://raw.githubusercontent.com/.../file.sh?t=$(date +%s)"
```

---

## 📝 环境变量

### 终端代理环境变量

```bash
# 需要访问外网时，在终端运行
export http_proxy=http://127.0.0.1:7890
export https_proxy=http://127.0.0.1:7890
export all_proxy=socks5://127.0.0.1:7891

# 或者添加到 ~/.bashrc (可选)
echo 'export http_proxy=http://127.0.0.1:7890' >> ~/.bashrc
echo 'export https_proxy=http://127.0.0.1:7890' >> ~/.bashrc
```

### CUDA 环境变量

通常已由系统配置，无需手动设置。

---

## 🔧 快速诊断命令

```bash
# 1. 检查网络连接
ping -c 4 baidu.com
curl -I https://www.google.com  # 需要代理

# 2. 检查 Clash 服务
sudo systemctl status clash
curl http://127.0.0.1:9090/configs

# 3. 检查 Docker
docker ps -a
docker exec -it paddle_animal bash

# 4. 检查 GPU
nvidia-smi

# 5. 检查磁盘空间
df -h

# 6. 检查内存
free -h
```

---

## 📞 访问方式

### SSH 访问

```bash
# 从局域网其他设备访问
ssh czf@192.168.1.109
# 密码: qwertyuiop
```

### 远程桌面

- ToDesk 已安装（自启动配置在 `~/.config/autostart/todesk.desktop`）

---

## 🎯 AI 助手使用指南

### 在本机器上工作时的最佳实践

1. **网络访问**: 优先使用已配置的 Clash 代理（端口 7890）
2. **容器操作**: 记得在容器内配置代理环境变量
3. **文件传输**: 使用 `docker cp` 或 Python HTTP 服务器
4. **代码提交**: 使用 Git 管理代码，避免丢失工作
5. **长时间任务**: 使用 `screen` 或 `tmux` 避免 SSH 断线导致任务中断

### 常见任务流程

**1. 下载外网文件**
```bash
# 确保代理启用
export http_proxy=http://127.0.0.1:7890
wget <url>
```

**2. 容器内开发**
```bash
# 进入容器
docker exec -it paddle_animal bash

# 配置网络
export http_proxy=http://192.168.1.109:7890
export https_proxy=http://192.168.1.109:7890

# 开始工作
cd /workspace
```

**3. 传输文件到 Windows**
```bash
# 方法 1: HTTP 服务器
cd ~
python3 -m http.server 8000
# 在 Windows 浏览器打开: http://192.168.1.109:8000

# 方法 2: SCP (从 Windows 运行)
scp czf@192.168.1.109:/path/to/file C:\path\to\destination
```

---

## 📅 更新日志

- **2025-11-13**: 初始版本，记录所有基础配置
  - 配置 Clash 命令行版本
  - 禁用 smart-display 服务
  - 完成动物检测项目环境搭建

---

## 💡 技巧和窍门

### 1. 快速启用代理

创建别名方便使用：
```bash
# 添加到 ~/.bashrc
alias proxyon='export http_proxy=http://127.0.0.1:7890 https_proxy=http://127.0.0.1:7890'
alias proxyoff='unset http_proxy https_proxy all_proxy'
```

### 2. 查看 Clash 实时日志

```bash
sudo journalctl -u clash -f
```

### 3. Docker 容器快速重启

```bash
docker restart paddle_animal && docker exec -it paddle_animal bash
```

---

**文档维护**: 请在修改系统配置后及时更新本文档！
