# OlivOS.nb2

[NoneBot2](https://github.com/nonebot/nonebot2) 的 [OlivOS](https://github.com/OlivOS-Team/OlivOS) 兼容层插件

**注意，本兼容层无法获得 API 的返回值！**

[![License](https://img.shields.io/github/license/nonepkg/OlivOS.nb2)](LICENSE)
![Python Version](https://img.shields.io/badge/python-3.7.3+-blue.svg)
![NoneBot Version](https://img.shields.io/badge/nonebot-2.0.0a13+-red.svg)
![PyPI Version](https://img.shields.io/pypi/v/OlivOS.nb2.svg)

### 安装

#### 从 PyPI 安装（推荐）

- 使用 nb-cli  

```
nb plugin install OlivOS.nb2
```

- 使用 poetry

```
poetry add OlivOS.nb2
```

- 使用 pip

```
pip install OlivOS.nb2
```

#### 从 GitHub 安装（不推荐）

- 使用 poetry

```
poetry add git+https://github.com/nonepkg/OlivOS.nb2.git

- 使用 pip

```
pip install git+https://github.com/nonepkg/OlivOS.nb2.git
```

### 使用

目前只有 CQHTTP(OneBot) 平台的被动消息兼容层，其他平台待添加。

OlivOS 插件请放入`./data/OlivOs/app/`。
