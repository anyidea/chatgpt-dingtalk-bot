# chatgpt-dingtalk-bot


[![License](https://img.shields.io/github/license/anyidea/chatgpt-dingtalk-bot)](https://github.com/anyidea/chatgpt-dingtalk-bot/blob/main/LICENSE)
[![Python](https://img.shields.io/pypi/pyversions/chatgpt-dingtalk-bot.svg)](https://pypi.org/project/chatgpt-dingtalk-bot/)
[![Build Status](https://github.com/anyidea/chatgpt-dingtalk-bot/actions/workflows/ci.yml/badge.svg)](https://github.com/anyidea/chatgpt-dingtalk-bot/actions/workflows/ci.yml)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)




A dingtalk chatbot powered by chatGPT.


* Documentation: <https://anyidea.github.io/chatgpt-dingtalk-bot>
* GitHub: <https://github.com/anyidea/chatgpt-dingtalk-bot>
* Free software: MIT


## Features

* 将ChatGPT集成到钉钉机器人，支持群聊和单聊模式
* 支持Docker一键部署
* 支持多配置账号，通过连接池来避免单账号限制


## Quick start
1. 复制`.env.dist`文件，并改名为`.env`，填写账号密码GPT_ACCOUNTS或者GPT_ACCESS_TOKENS，二选一即可，支持多个账号和token

2. 拉取镜像并运行
```commandline
docker run -d --restart unless-stopped --env-file .env -p 8090:8090 aidenlu/chatgpt-dingtalk-bot
```

3. 在钉钉管理后台添加企业内部app, 并添加机器人(需要配置机器人权限)，然后配置url(http://your-ip-address:8090/chat)和ip白名单，最后点击上线机器人即可。
[](https://raw.githubusercontent.com/wccdev/filez-python-sdk/master/.github/assets/20230228005625.jpg)
[](https://raw.githubusercontent.com/wccdev/filez-python-sdk/master/.github/assets/20230228005746.jpg)
[](https://raw.githubusercontent.com/wccdev/filez-python-sdk/master/.github/assets/20230228005824.jpg)

## Credits

This package was created with [Cookiecutter](https://github.com/cookiecutter/cookiecutter) and the [wccdev/cookiecutter-pypackage](https://github.com/wccdev/cookiecutter-pypackage) project template.
