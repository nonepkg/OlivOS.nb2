<div align="center">
    <img width="200" src="docs/logo.png" alt="logo"></br>

# OlivOS.nb2

[NoneBot2](https://github.com/nonebot/nonebot2) 的 [OlivOS](https://github.com/OlivOS-Team/OlivOS) 兼容层插件

**注意，本兼容层无法获得 API 的返回值！**

[![License](https://img.shields.io/github/license/nonepkg/OlivOS.nb2)](LICENSE)
![Python Version](https://img.shields.io/badge/python-3.7.3+-blue.svg)
![NoneBot Version](https://img.shields.io/badge/nonebot-2.0.0a13+-red.svg)
![PyPI Version](https://img.shields.io/pypi/v/OlivOS.nb2.svg)

</div>

## 安装

### 从 PyPI 安装（推荐）

- 使用 nb-cli  

```sh
nb plugin install OlivOS.nb2
```

- 使用 poetry

```sh
poetry add OlivOS.nb2
```

- 使用 pip

```sh
pip install OlivOS.nb2
```

### 从 GitHub 安装（不推荐）

- 使用 poetry

```sh
poetry add git+https://github.com/nonepkg/OlivOS.nb2.git
```

- 使用 pip

```sh
pip install git+https://github.com/nonepkg/OlivOS.nb2.git
```

## 使用

目前只有 OneBotV11（CQHTTP）平台的兼容层，其他平台待添加（Telegram 平台实验中）。

OlivOS 插件请放入`./data/OlivOS/app/`。

## 插件兼容名单

**这里的插件指 OlivOS 插件。**未在此名单并不意味着无法加载，只是加载后可能出现位未知问题。

- [OlivOS-Team/OlivaDiceCore](https://github.com/OlivOS-Team/OlivaDiceCore)
- [OlivOS-Team/OlivaDiceJoy](https://github.com/OlivOS-Team/OlivaDiceJoy)
- [OlivOS-Team/OlivaDiceLogger](https://github.com/OlivOS-Team/OlivaDiceLogger)
- [Fishroud/OlivaBilibiliPlugin](https://github.com/Fishroud/OlivaBilibiliPlugin)

### 已证实不兼容

- [lunzhiPenxil/OlivOSOnebotV11](https://github.com/lunzhiPenxil/OlivOSOnebotV11) 使用 Thread
- [OlivOS-Team/OlivaDiceMaster](https://github.com/OlivOS-Team/OlivaDiceMaster) 使用 Thread
