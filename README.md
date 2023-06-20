# ChatGPT Dingtalk Bot


[![License](https://img.shields.io/github/license/anyidea/chatgpt-dingtalk-bot)](https://github.com/anyidea/chatgpt-dingtalk-bot/blob/main/LICENSE)
[![Build Status](https://github.com/anyidea/chatgpt-dingtalk-bot/actions/workflows/ci.yml/badge.svg)](https://github.com/anyidea/chatgpt-dingtalk-bot/actions/workflows/ci.yml)
[![Python Version](https://img.shields.io/badge/python->=3.9-blue)](https://www.python.org/)
[![Docker Image Size (latest by date)](https://img.shields.io/docker/image-size/aidenlu/chatgpt-dingtalk-bot)](https://hub.docker.com/r/aidenlu/chatgpt-dingtalk-bot)
[![Docker Pulls](https://img.shields.io/docker/pulls/aidenlu/chatgpt-dingtalk-bot)](https://hub.docker.com/r/aidenlu/chatgpt-dingtalk-bot)
[![Built with Cookiecutter](https://img.shields.io/badge/built%20with-Cookiecutter-ff69b4.svg?logo=cookiecutter)](https://github.com/wccdev/cookiecutter-pypackage/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

> 🚀 官方API版本ChatGPT集成到钉钉机器人, 支持单聊和群聊, 特别感谢 [ChatGPT](https://github.com/acheong08/ChatGPT)项目


* Documentation: <https://anyidea.github.io/chatgpt-dingtalk-bot>
* GitHub: <https://github.com/anyidea/chatgpt-dingtalk-bot>
* Free software: MIT


> **Note**
>
> - ChatGPT目前尚未向中国`大陆`和`香港`等地区提供服务，因此运行该项目
> 需要Proxy服务或者直接运行在海外云服务器上(`日本`、`韩国`、`美国`等机房)
>


## Features

* API版本`ChatGPT`(**不是免费**)，没有那些花里胡哨的功能，很简洁！
* 支持打字机特效（注意：需要额外消耗钉钉api调用次数）
* 支持机器人群聊和单聊模式，支持上下文聊天
* 使用钉钉机器人Stream模式推送消息，配置简单，不依赖也不需要暴露公网IP，无需向公网开放端口
* 支持`Docker`一键部署

## Installation

### 拉取Git仓库代码运行
> 运行该项目需要Python3.9以上的环境，请先确保环境已经满足要求
1. 请先安装Python包管理工具[Poetry](https://python-poetry.org/docs/#installation)
```bash
curl -sSL https://install.python-poetry.org | python3 -
```
2. 拉取github仓库代码
```bash
git clone https://github.com/anyidea/chatgpt-dingtalk-bot.git
```
3. 进入项目根目录, 安装项目依赖环境
```bash
poetry install --only main --no-root
```
4. 启动应用
```bash
poetry run python -m chatbot
```

### Docker 运行

- 通过`.env`文件来批量设置环境变量
```bash
docker run -d --name=chatgpt-dingtalk-bot --restart=unless-stopped \
--env-file .env \
aidenlu/chatgpt-dingtalk-bot:api
```
>
>
> 复制`.env.dist`文件，并改名为`.env`，填写账号密码GPT_API_KEY
> `API KEY`需要登陆OpenAI管理后台获取: https://platform.openai.com/account/api-keys

- 或者通过`-e`/`--env`参数来设置环境变量
```bash
docker run -d --name=chatgpt-dingtalk-bot --restart unless-stopped \
-e GPT_API_KEY=<key> \
-e DINGTALK_APP_KEY=<app_key> \
-e DINGTALK_APP_SECRET=<app_secret> \
-e GPT_MODEL=gpt-3.5-turbo \
aidenlu/chatgpt-dingtalk-bot:api
```
> **Note**
>
> **gpt-4**模型需要用户已开通访问权限，

### 配置钉钉机器人
1. 在钉钉管理后台添加企业内部应用(需要有管理后台权限)
> ⚠️  机器人不要命名为chatgpt之类的，会被钉钉风控
---
<img src="https://raw.githubusercontent.com/anyidea/chatgpt-dingtalk-bot/api/.github/assets/create_app.png" width="100%" height="60%">

2. 应用内机器人添加单聊和群聊权限
---

<img src="![image](https://github.com/anyidea/chatgpt-dingtalk-bot/assets/48710760/52f5d040-0e26-4fb5-986c-a529f91a8c9a)" width="100%" height="60%">


3. 点击应用内机器人配置页
---

<img src="https://raw.githubusercontent.com/anyidea/chatgpt-dingtalk-bot/api/.github/assets/click_bot.png" width="100%" height="60%">


4. 配置机器人并开启stream模式
---

<img src="https://raw.githubusercontent.com/anyidea/chatgpt-dingtalk-bot/api/.github/assets/config_bot.png" width="100%" height="60%">

<img src="https://raw.githubusercontent.com/anyidea/chatgpt-dingtalk-bot/api/.github/assets/enable_stream.png" width="100%" height="60%">

<img src="https://raw.githubusercontent.com/anyidea/chatgpt-dingtalk-bot/api/.github/assets/stream_chat.gif" width="100%" height="60%">


> **Warning**
>
> 钉钉虽然支持Markdown格式消息，但仅支持部分语法且移动端和PC端展示会有差异，建议使用text文本消息


## Credits

This package was created with [Cookiecutter](https://github.com/cookiecutter/cookiecutter) and the [wccdev/cookiecutter-pypackage](https://github.com/wccdev/cookiecutter-pypackage) project template.
