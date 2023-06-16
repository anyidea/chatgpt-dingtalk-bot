# !/usr/bin/env python

import sys

sys.path.append("../../")
sys.path.append("../")
sys.path.append(".")

import argparse
import logging
from dingtalk_stream import AckMessage, interactive_card
import dingtalk_stream
import time
import copy, asyncio


INTERACTIVE_CARD_JSON_SAMPLE_1 = {
    "config": {"autoLayout": True, "enableForward": True},
    "header": {
        "title": {"type": "text", "text": "钉钉卡片"},
        "logo": "@lALPDfJ6V_FPDmvNAfTNAfQ",
    },
    "contents": [
        {
            "type": "text",
            "text": "钉钉，让进步发生",
            "id": "text_1686025745169",
        },
    ],
}


def setup_logger():
    logger = logging.getLogger()
    handler = logging.StreamHandler()
    handler.setFormatter(
        logging.Formatter(
            '%(asctime)s %(name)-8s %(levelname)-8s %(message)s [%(filename)s:%(lineno)d]'
        )
    )
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    return logger


def define_options():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--client_id',
        dest='client_id',
        required=True,
        help='app_key or suite_key from https://open-dev.digntalk.com',
    )
    parser.add_argument(
        '--client_secret',
        dest='client_secret',
        required=True,
        help='app_secret or suite_secret from https://open-dev.digntalk.com',
    )
    options = parser.parse_args()
    return options


class CardBotHandler(dingtalk_stream.AsyncChatbotHandler):
    """
    接收回调消息。
    回复一个卡片，然后更新卡片的文本和图片。
    """

    def __init__(self, logger: logging.Logger = None, max_workers: int = 8):
        super(CardBotHandler, self).__init__(max_workers=max_workers)
        if logger:
            self.logger = logger

    def process(self, callback: dingtalk_stream.CallbackMessage):
        '''
        多线程场景，process函数不要用 async 修饰
        :param message:
        :return:
        '''

        incoming_message = dingtalk_stream.ChatbotMessage.from_dict(callback.data)

        print(incoming_message, 2222, callback.data)

        texts = ["第一行文本"]

        # 先回复一个文本卡片
        card_biz_id = self.reply_card(
            INTERACTIVE_CARD_JSON_SAMPLE_1,
            incoming_message,
            False,
        )

        images = [
            "@lADPDe7s2ySi18PNA6XNBXg",
            "@lADPDf0i1beuNF3NAxTNBXg",
            "@lADPDe7s2ySRnIvNA6fNBXg",
        ]

        for i in "的更加快一点，光辉你还好么？？？？asdasdasdasdasdasdasfskdahfk13123h1uh23uihasd":
            time.sleep(1)
            INTERACTIVE_CARD_JSON_SAMPLE_1["contents"][0]["text"] += i

            self.update_card(
                card_biz_id,
                INTERACTIVE_CARD_JSON_SAMPLE_1,
            )

        return AckMessage.STATUS_OK, 'OK'


def main():
    logger = setup_logger()
    options = define_options()

    credential = dingtalk_stream.Credential(options.client_id, options.client_secret)
    client = dingtalk_stream.DingTalkStreamClient(credential)
    client.register_callback_hanlder(
        dingtalk_stream.chatbot.ChatbotMessage.TOPIC, CardBotHandler(logger)
    )
    client.start_forever()


if __name__ == '__main__':
    main()
