# Chatgpt Dingtalk Bot


[![License](https://img.shields.io/github/license/anyidea/chatgpt-dingtalk-bot)](https://github.com/anyidea/chatgpt-dingtalk-bot/blob/main/LICENSE)
[![Python Version](https://img.shields.io/badge/python->=3.8-blue)](https://www.python.org/)
[![Build Status](https://github.com/anyidea/chatgpt-dingtalk-bot/actions/workflows/ci.yml/badge.svg)](https://github.com/anyidea/chatgpt-dingtalk-bot/actions/workflows/ci.yml)
[![Docker Image Size (latest by date)](https://img.shields.io/docker/image-size/aidenlu/chatgpt-dingtalk-bot)](https://hub.docker.com/r/aidenlu/chatgpt-dingtalk-bot)
[![Docker Pulls](https://img.shields.io/docker/pulls/aidenlu/chatgpt-dingtalk-bot)](https://hub.docker.com/r/aidenlu/chatgpt-dingtalk-bot)
[![Built with Cookiecutter](https://img.shields.io/badge/built%20with-Cookiecutter-ff69b4.svg?logo=cookiecutter)](https://github.com/wccdev/cookiecutter-pypackage/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

> 🚀 Web版ChatGPT集成到钉钉机器人, 支持单聊和群聊, 特别感谢 [ChatGPT](https://github.com/acheong08/ChatGPT)项目


* Documentation: <https://anyidea.github.io/chatgpt-dingtalk-bot>
* GitHub: <https://github.com/anyidea/chatgpt-dingtalk-bot>
* Free software: MIT


## Features

* 浏览器版本ChatGPT(非api版本)
* 使用Fastapi框架，支持异步
* 支持机器人群聊和单聊模式(暂只支持账号登录模式)
* 支持Docker一键部署
* 支持配置多个账号，通过连接池来避免单账号的限制


## Quick start
1. 复制`.env.dist`文件，并改名为`.env`，填写账号密码GPT_ACCOUNTS或者GPT_ACCESS_TOKENS，二选一即可，支持多个账号和token

2. 拉取Docker镜像并运行
```commandline
docker run -d --restart unless-stopped --env-file .env -p 8090:8090 aidenlu/chatgpt-dingtalk-bot
```

3. 在钉钉管理后台添加企业内部机器人，然后配置消息接收地址和出口IP白名单，最后需要手动点击上线机器人。
> 机器人不要命名为chatgpt之类的，会被钉钉屏蔽
<div align=center>
<img src="https://raw.githubusercontent.com/anyidea/chatgpt-dingtalk-bot/main/.github/assets/20230228005625.jpg" ali width="80%" height="80%">


<img src="https://raw.githubusercontent.com/anyidea/chatgpt-dingtalk-bot/main/.github/assets/20230228005746.jpg" width="80%" height="80%">


<img src="https://raw.githubusercontent.com/anyidea/chatgpt-dingtalk-bot/main/.github/assets/20230228005824.jpg" width="80%" height="80%">


<img src="https://raw.githubusercontent.com/anyidea/chatgpt-dingtalk-bot/main/.github/assets/20230228010827.jpg" width="80%" height="80%">
</div>


## Credits

This package was created with [Cookiecutter](https://github.com/cookiecutter/cookiecutter) and the [wccdev/cookiecutter-pypackage](https://github.com/wccdev/cookiecutter-pypackage) project template.
