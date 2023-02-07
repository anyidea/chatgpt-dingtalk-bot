import time

import httpx

from .config import settings


class DingtalkCorpAPI:
    """
    钉钉企业内部应用接口SDK
    """

    def __init__(self, app_key: str = None, app_secret: str = None):
        self._app_key = app_key or settings.dingtalk_app_key
        self._app_secret = app_secret or settings.dingtalk_app_secret
        self._access_token = ""
        self.expires_at = 0

    async def get_access_token(
        self, app_key: str = None, app_secret: str = None
    ) -> str:
        """
        获取企内部应用access token
        接口文档: https://open.dingtalk.com/document/orgapp-server/obtain-orgapp-token
        :param app_key: 应用的唯一标识key
        :param app_secret: 应用的密钥。AppKey和AppSecret可在钉钉开发者后台的应用详情页面获取。
        :return: 企业微应用访问凭证,凭证到期时间(单位:秒)
        """
        if time.time() > self.expires_at:
            url = "https://oapi.dingtalk.com/gettoken"
            params = {
                "appkey": app_key or self._app_key,
                "appsecret": app_secret or self._app_secret,
            }
            async with httpx.AsyncClient() as client:
                resp = await client.get(url, params=params)
                assert resp.status_code == 200, "获取access_token失败"
                ret = resp.json()
                self._access_token, self.expires_at = (
                    ret["access_token"],
                    time.time() + ret["expires_in"],
                )

        return self._access_token

    async def robot_batch_send(
        self,
        robot_code: str,
        user_ids: list[str],
        msg_key: str = "sampleText",
        msg_param: dict = None,
    ) -> None:
        """钉钉机器人群发单聊消息"""
        url = "https://api.dingtalk.com/v1.0/robot/oToMessages/batchSend"
        access_token = await self.get_access_token()
        headers = {
            "x-acs-dingtalk-access-token": access_token,
            "host": "api.dingtalk.com",
        }
        json = {
            "robotCode": robot_code,
            "userIds": user_ids,
            "msgKey": msg_key,
            "msgParam": msg_param,
        }

        async with httpx.AsyncClient() as client:
            resp = await client.post(url, json=json, headers=headers)
            assert resp.status_code == 200, "发送单聊消息失败"

    async def robot_webhook_send(self, webhook_url: str, json: dict) -> None:
        """
        发送钉钉群聊消息
        """
        async with httpx.AsyncClient() as client:
            resp = await client.post(webhook_url, json=json)
            assert resp.status_code == 200, "发送群聊消息失败"
