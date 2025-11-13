# VS Code 远程开发 + AI 助手配置指南

完整的 LaTeX 开发工作流：笔记本 VS Code → 远程 Linux → AI 编译调整

---

## 📋 工作流概述

```
笔记本 VS Code
    ↓ (SSH 远程连接)
Linux 电脑 (192.168.1.109)
    ↓
~/projects/latex-notes/*.tex
    ↓ (VS Code 侧边栏 AI 助手)
AI 沙盒编译 LaTeX → PDF
    ↓
查看 PDF → 让 AI 调整字体 → 重新编译
```

---

## 🚀 第一步：配置 VS Code Remote SSH

### 1.1 在笔记本上安装 VS Code 扩展

打开 VS Code，安装以下扩展：
- **Remote - SSH** (Microsoft)
- **LaTeX Workshop** (James Yu) - LaTeX 编辑支持
- **Continue** - AI 代码助手

### 1.2 配置 SSH 连接

按 `F1` → 输入 "Remote-SSH: Open SSH Configuration File"

添加你的 Linux 机器配置：

```ssh-config
Host linux-dev
    HostName 192.168.1.109
    User user
    Port 22
    # 如果有 SSH 密钥，取消注释下面这行
    # IdentityFile ~/.ssh/id_rsa
```

### 1.3 连接到 Linux

1. 按 `F1` → 输入 "Remote-SSH: Connect to Host"
2. 选择 `linux-dev`
3. 输入密码（或使用 SSH 密钥）
4. 连接成功后，VS Code 窗口左下角会显示 "SSH: linux-dev"

---

## 🤖 第二步：配置 Continue AI 助手

### 2.1 打开 Continue 配置

在 VS Code 侧边栏点击 Continue 图标 → 点击设置图标

### 2.2 配置连接到本地 Ollama

编辑 `~/.continue/config.json`（或通过界面配置）：

```json
{
  "models": [
    {
      "title": "Qwen2.5-Coder 32B",
      "provider": "ollama",
      "model": "qwen2.5-coder:32b",
      "apiBase": "http://192.168.1.109:11434"
    }
  ],
  "tabAutocompleteModel": {
    "title": "Qwen2.5-Coder",
    "provider": "ollama",
    "model": "qwen2.5-coder:32b",
    "apiBase": "http://192.168.1.109:11434"
  }
}
```

### 2.3 测试连接

在 Continue 侧边栏输入：
```
你好，请帮我测试一下连接
```

如果回复正常，说明配置成功！

---

## 📝 第三步：LaTeX 工作流

### 3.1 创建项目目录

在 Linux 上：
```bash
mkdir -p ~/projects/latex-notes
cd ~/projects/latex-notes
```

在 VS Code 中：
- File → Open Folder → 选择 `/home/user/projects/latex-notes`

### 3.2 创建示例 LaTeX 文件

创建 `test.tex`：

```latex
\documentclass{article}
\usepackage{xeCJK}
\setCJKmainfont{Noto Sans CJK SC}  % 中文字体

\title{测试文档}
\author{Your Name}
\date{\today}

\begin{document}

\maketitle

\section{介绍}
这是一个测试文档，用于验证中文 LaTeX 编译。

\section{内容}
\subsection{小节标题}
这里是正文内容，包含中文字符。

\end{document}
```

### 3.3 让 AI 帮你编译

在 VS Code 的 Continue 侧边栏输入：

```
帮我编译 test.tex，使用 xelatex 编译器（支持中文）
```

AI 会在沙盒中执行：
```bash
cd /workspace/projects/latex-notes
xelatex test.tex
```

### 3.4 查看生成的 PDF

在 VS Code 文件浏览器中，右键 `test.pdf` → "Open"

或者让 AI 帮你：
```
帮我用 evince 打开生成的 PDF（在 Linux 桌面上显示）
```

### 3.5 让 AI 调整格式

```
帮我把所有章节标题（\section）的字体大小改成 18pt
```

AI 会修改 .tex 文件，然后重新编译。

---

## 🎯 常用 AI 命令示例

### 编译相关

```
编译 document.tex，使用 xelatex
```

```
重新编译，并清理临时文件（.aux, .log）
```

```
用 latexmk 自动编译并监听文件变化
```

### 格式调整

```
把正文字体大小从 11pt 改成 12pt
```

```
调整页边距：上下 2.5cm，左右 3cm
```

```
把所有章节标题改成加粗红色
```

### 内容处理

```
帮我生成一个三行两列的表格模板
```

```
插入一个图片，路径是 images/plot.png，宽度 0.8\textwidth
```

```
在文档开头添加摘要（abstract）部分
```

---

## 🔄 完整工作流示例

### 场景：写论文并调整格式

1. **在笔记本上打开 VS Code，连接到 Linux**
   - F1 → Remote-SSH: Connect to Host → linux-dev

2. **打开项目**
   - File → Open Folder → ~/projects/my-paper

3. **编写 LaTeX**
   - 创建 `paper.tex`，写内容

4. **提交到 GitHub**
   ```bash
   # 在 VS Code 终端
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/your-repo.git
   git push -u origin main
   ```

5. **让 AI 编译**
   - Continue 侧边栏：`编译 paper.tex`

6. **查看 PDF，发现问题**
   - 章节标题太小

7. **让 AI 调整**
   - Continue：`把所有 \section 的字体改成 16pt`

8. **AI 自动重新编译**
   - 查看新的 PDF，满意！

9. **提交更改**
   ```bash
   git add .
   git commit -m "Adjust section font size"
   git push
   ```

---

## 🐛 常见问题

### Q1: Continue 连接不上 Ollama？

**检查 Ollama 是否运行：**
```bash
# 在 Linux 上
systemctl status ollama

# 如果没运行，启动它
systemctl start ollama
```

**检查防火墙：**
```bash
sudo ufw allow 11434
```

### Q2: XeLaTeX 找不到中文字体？

**安装中文字体：**
```bash
sudo apt install fonts-noto-cjk
```

**或者在 .tex 中指定系统已有的字体：**
```latex
\setCJKmainfont{WenQuanYi Micro Hei}  % 文泉驿微米黑
```

### Q3: LaTeX 编译出错怎么办？

**让 AI 帮你调试：**
```
编译失败了，帮我看看错误信息并修复
```

AI 会读取 `.log` 文件，分析错误，并尝试修复。

### Q4: 想要 AI 在沙盒内编译，而不是直接在主机？

**进入沙盒编译：**
```bash
# 在 Linux 终端
cd ~/linux/ai-sandbox
docker compose up -d
docker compose exec ai-sandbox bash

# 在沙盒内
cd /workspace/projects/latex-notes
xelatex test.tex
```

**或者让 Continue AI 自动执行：**
```
在 ai-sandbox 容器内编译 /workspace/projects/latex-notes/test.tex
```

---

## 💡 高级技巧

### 技巧 1：自动编译监听

让 AI 设置自动编译（文件改动时自动重新编译）：

```
用 latexmk -pvc 监听 test.tex，自动编译
```

### 技巧 2：批量处理

```
把 chapters/ 目录下的所有 .tex 文件合并成一个 main.tex
```

### 技巧 3：转换格式

```
把 document.tex 编译成 PDF，然后转换成 PPTX
```

（会使用你的 pdf2ppt-converter 工具！）

---

## 📚 推荐资源

- **LaTeX 中文文档**: https://www.latexstudio.net/
- **Overleaf 模板库**: https://www.overleaf.com/latex/templates
- **Continue 文档**: https://continue.dev/docs
- **Ollama 模型库**: https://ollama.com/library

---

## 🎉 开始使用

现在你已经配置完成！试试这个简单的测试：

1. 在 VS Code 中创建 `hello.tex`
2. 在 Continue 侧边栏输入：
   ```
   帮我写一个简单的中文 LaTeX 文档，标题是"你好世界"，
   然后编译成 PDF
   ```
3. AI 会自动生成代码、保存文件、编译、显示结果

享受你的 AI 辅助 LaTeX 工作流吧！🚀
