# Chatgpt Dingtalk Bot


[![License](https://img.shields.io/github/license/anyidea/chatgpt-dingtalk-bot)](https://github.com/anyidea/chatgpt-dingtalk-bot/blob/main/LICENSE)
[![Python Version](https://img.shields.io/badge/python->=3.8-blue)](https://www.python.org/)
[![Build Status](https://github.com/anyidea/chatgpt-dingtalk-bot/actions/workflows/ci.yml/badge.svg)](https://github.com/anyidea/chatgpt-dingtalk-bot/actions/workflows/ci.yml)
[![Built with Cookiecutter](https://img.shields.io/badge/built%20with-Cookiecutter-ff69b4.svg?logo=cookiecutter)](https://github.com/wccdev/cookiecutter-pypackage/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)




将Web版ChatGPT集成到钉钉机器人,支持单聊和群聊@


* Documentation: <https://anyidea.github.io/chatgpt-dingtalk-bot>
* GitHub: <https://github.com/anyidea/chatgpt-dingtalk-bot>
* Free software: MIT


## Features

* 浏览器版本ChatGPT, 完整版本，非api版本
* 支持群聊和单聊模式
* 支持Docker一键部署
* 支持配置多个账号，通过连接池来避免单账号的限制


## Quick start
1. 复制`.env.dist`文件，并改名为`.env`，填写账号密码GPT_ACCOUNTS或者GPT_ACCESS_TOKENS，二选一即可，支持多个账号和token

2. 拉取镜像并运行
```commandline
docker run -d --restart unless-stopped --env-file .env -p 8090:8090 aidenlu/chatgpt-dingtalk-bot
```

3. 在钉钉管理后台添加企业内部app, 并添加机器人(需要配置机器人权限)，然后配置url(http://your-ip-address:8090/chat)和ip白名单，最后点击上线机器人即可。
![1](https://raw.githubusercontent.com/anyidea/chatgpt-dingtalk-bot/main/.github/assets/20230228005625.jpg)
![2](https://raw.githubusercontent.com/anyidea/chatgpt-dingtalk-bot/main/.github/assets/20230228005746.jpg)
![3](https://raw.githubusercontent.com/anyidea/chatgpt-dingtalk-bot/main/.github/assets/20230228005824.jpg)

## Credits

This package was created with [Cookiecutter](https://github.com/cookiecutter/cookiecutter) and the [wccdev/cookiecutter-pypackage](https://github.com/wccdev/cookiecutter-pypackage) project template.
