# doubao-no-watermarking

维护者：`sagima`

`doubao-no-watermarking` 是一个面向本地使用场景的桌面封装项目，用于从豆包分享链接中提取图片和视频资源。当前仓库以 `sagima` 的二次整理、桌面化封装、GitHub 维护和后续发布为目标，适合继续作为公开仓库或私有仓库长期维护。

除 [LICENSE](/Users/sagima/Downloads/Demo/doubao-no-watermarking/LICENSE) 与 [legal/THIRD_PARTY_NOTICES.txt](/Users/sagima/Downloads/Demo/doubao-no-watermarking/legal/THIRD_PARTY_NOTICES.txt) 中依法必须保留的上游版权与许可说明外，当前仓库中的维护者与开发者展示信息已经统一整理为 `sagima`。

## 项目特点

- 支持图片分享链接解析，返回图片地址、宽度、高度等信息。
- 支持视频分享链接解析，返回视频播放地址、分辨率、封面地址等信息。
- 提供本地桌面启动器，适合封装为 macOS `.app` 或 Windows `.exe`。
- 提供浅蓝色桌面界面，支持查看、复制和下载解析结果。
- 保留原始解析核心逻辑，降低后续维护和问题定位成本。
- 目录已清理为适合上传 GitHub 的状态，不包含打包缓存和本地产物。

## 适用场景

- 本地自用提取工具
- 私有化内部工具
- 二次封装为桌面应用
- 作为 API 服务接入你自己的前端或工具链

## 当前仓库结构

```text
doubao-no-watermarking/
  app.py
  doubao_parser/
  src/
    desktop_app/
      launcher.py
      runtime.py
      server.py
      ui/
        index.html
  scripts/
    build_macos.sh
    build_windows.ps1
  legal/
    THIRD_PARTY_NOTICES.txt
  README.md
  LICENSE
  requirements.txt
  pyproject.toml
  uv.lock
```

各目录用途如下：

- `doubao_parser/`
  放原始解析核心逻辑，分别处理图片和视频提取。

- `src/desktop_app/server.py`
  提供 FastAPI 服务入口，对外暴露 `/parse`、`/parse-video`、`/health` 等接口。

- `src/desktop_app/launcher.py`
  桌面启动器。启动本地服务后，拉起桌面窗口或浏览器页面。

- `src/desktop_app/ui/index.html`
  当前桌面界面，已调整为浅蓝色风格，并显示“开发者：sagima”。

- `scripts/`
  双平台打包脚本。

- `legal/`
  放保留的法律文件和第三方声明。

## 功能说明

### 图片解析

输入包含 `/thread/` 的豆包对话分享链接，系统会解析出图片资源列表。

返回字段通常包括：

- `url`
- `width`
- `height`

### 视频解析

输入包含 `share_id` 与 `video_id` 的豆包视频分享链接，系统会解析出视频播放信息。

返回字段通常包括：

- `url`
- `width`
- `height`
- `definition`
- `poster_url`

## 运行环境

- Python `3.10+`
- 推荐本地网络可正常访问豆包分享页面
- macOS 或 Windows

## 安装依赖

```bash
python -m pip install -r requirements.txt
```

## 本地开发运行

### 方式一：启动 API 服务

```bash
python -m uvicorn app:app --host 127.0.0.1 --port 8000
```

启动后可访问：

- 首页：`http://127.0.0.1:8000/`
- 文档：`http://127.0.0.1:8000/docs`
- 健康检查：`http://127.0.0.1:8000/health`

### 方式二：启动桌面版

```bash
python src/desktop_app/launcher.py
```

如果你更喜欢模块方式，也可以使用：

```bash
python -m src.desktop_app.launcher
```

## API 教程

### 解析图片

请求示例：

```bash
curl "http://127.0.0.1:8000/parse?url=https://www.doubao.com/thread/xxxxx"
```

返回示例：

```json
{
  "success": true,
  "image_count": 2,
  "images": [
    {
      "url": "https://...",
      "width": 1024,
      "height": 1024
    }
  ]
}
```

### 解析视频

请求示例：

```bash
curl "http://127.0.0.1:8000/parse-video?url=https://www.doubao.com/video-sharing?share_id=xxx&video_id=xxx"
```

返回示例：

```json
{
  "success": true,
  "video": {
    "url": "https://...",
    "width": 1920,
    "height": 1080,
    "definition": "1080p",
    "poster_url": "https://..."
  }
}
```

## 桌面界面使用教程

### 图片流程

1. 打开桌面程序。
2. 切换到“图片解析”。
3. 粘贴豆包图片分享链接。
4. 点击“开始解析”。
5. 在结果区中查看图片。
6. 使用“查看”“下载”“复制地址”按钮处理结果。

### 视频流程

1. 打开桌面程序。
2. 切换到“视频解析”。
3. 粘贴豆包视频分享链接。
4. 点击“开始解析”。
5. 预览视频结果。
6. 使用“查看”“下载”“复制地址”按钮处理结果。

## 打包说明

### macOS

执行：

```bash
bash scripts/build_macos.sh
```

说明：

- 该脚本会安装 `PyInstaller` 和 `pywebview`
- 生成的应用名会使用当前包名
- 打包产物默认输出到 `dist/`

### Windows

执行：

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\build_windows.ps1
```

说明：

- 需要在 Windows 环境中执行
- 不能在当前 macOS 上直接稳定产出原生 `.exe`
- 建议在目标 Windows 机器上本地打包

## 适合上传 GitHub 的原因

当前目录已经整理为适合仓库托管的状态，重点包括：

- 已移除本地产物目录，如 `dist/` 和 `build/`
- 已移除缓存目录，如 `__pycache__/`
- 已移除系统垃圾文件，如 `.DS_Store`
- 已移除旧的打包规格文件
- 已统一维护者与开发者展示信息
- 已保留必要的开源许可证和第三方声明

## 建议的 GitHub 仓库信息

### 仓库标题

`doubao-no-watermarking`

### 仓库描述

`Desktop packaging and local delivery for Doubao media extraction, maintained by sagima.`

### 建议标签

- `python`
- `fastapi`
- `desktop-app`
- `pyinstaller`
- `doubao`
- `media-tools`

## 常见问题

### 1. 为什么 `python src/desktop_app/launcher.py` 之前报 `No module named 'src'`？

这是脚本路径启动时的导入路径问题，当前版本已经兼容：

- `python src/desktop_app/launcher.py`
- `python -m src.desktop_app.launcher`

### 2. 为什么解析失败？

常见原因有：

- 分享链接格式不正确
- 图片链接不是 `/thread/` 类型
- 视频链接缺少 `share_id` 或 `video_id`
- 目标页面结构发生变化
- 本地网络无法正常访问目标资源

### 3. 为什么 Windows 包没有在这个仓库里直接提供？

因为原生 Windows `exe` 更稳妥的方式是在 Windows 环境本地打包。当前仓库已经包含完整打包脚本，迁移到 Windows 后可直接执行。

### 4. 这个仓库是否已经适合直接上传？

从目录整洁度、维护信息、README 完整度和保留法律文件这几个角度看，当前已经具备上传条件。

## 后续可继续优化的方向

- 补充应用图标并统一品牌资源
- 增加 GitHub Actions 自动构建流程
- 增加启动失败时的图形化提示
- 优化打包体积
- 增加英文 README

## 合规说明

当前版本的品牌、桌面封装和维护者信息已整理为 `sagima`，同时保留了上游项目所要求的许可证与第三方声明文件：

- [LICENSE](/Users/sagima/Downloads/Demo/doubao-no-watermarking/LICENSE)
- [legal/THIRD_PARTY_NOTICES.txt](/Users/sagima/Downloads/Demo/doubao-no-watermarking/legal/THIRD_PARTY_NOTICES.txt)

如果你准备上传到 GitHub，可以直接使用当前仓库内容继续维护。  
推荐对外说明为：

`doubao-no-watermarking maintained by sagima. Desktop packaging and local delivery for Doubao media extraction.`
