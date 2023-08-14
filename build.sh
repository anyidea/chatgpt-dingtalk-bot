#!/user/bin/bash

docker buildx build -t aidenlu/chatgpt-dingtalk-bot:api --platform linux/arm64,linux/amd64 . --push
