# TP Shop API 自动化工具

## 概述
TP Shop API 自动化工具是一个用于自动化测试 TP Shop 相关 API 的工具。该工具使用 Python 编写，依赖 PyQt5 进行图形界面开发，同时使用了 `requests` 等库进行 API 调用。

## 环境要求
- Python 3.8.20
- 虚拟环境：`E:\\miniconda\\envs\\test`
- 主要依赖库：
  - PyQt5
  - requests
  - h2
  - hpack
  - certifi
  - zstandard

## 安装步骤
1. 创建并激活虚拟环境：
```bash
conda create -n test python=3.8.20
conda activate test
```
2. 安装依赖库：
```bash
pip install -r requirements.txt
```
（请确保 `requirements.txt` 文件包含项目所需的所有依赖库）

## 项目结构
```plaintext
TP_shop_Auto/
├── TP_shop_Api_auto/
│   ├── build/
│   ├── dist/
│   ├── gui/
│   │   └── main_window.py
│   ├── pages/
│   │   ├── admin_page.py
│   │   └── shop_page.py
│   ├── utils/
│   │   └── config.py
│   ├── run.py
│   └── TP_Shop_Tool.spec
└── ...
```

## 运行项目
### 开发环境运行
```bash
python run.py
```

### 打包成可执行文件
使用 PyInstaller 进行打包：
```bash
pyinstaller TP_Shop_Tool.spec
```
打包后的可执行文件位于 `dist` 目录下。

## 注意事项
- 请确保在正确的虚拟环境中运行项目。
- 打包时可能需要根据实际情况调整 `TP_Shop_Tool.spec` 文件。

## 贡献
如果你想为这个项目做出贡献，请遵循以下步骤：
1. Fork 这个仓库。
2. 创建一个新的分支 (`git checkout -b feature/your-feature`)。
3. 提交你的更改 (`git commit -am 'Add some feature'`)。
4. 推送到分支 (`git push origin feature/your-feature`)。
5. 创建一个新的 Pull Request。
```


        