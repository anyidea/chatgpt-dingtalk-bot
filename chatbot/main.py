import logging
from dingtalk_stream import AckMessage
import dingtalk_stream
from copy import deepcopy
from .templates import INTERACTIVE_CARD_JSON_SAMPLE
import time

from .utils import init_chatbot
from .config import dingtalk_settings


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


class CardBotHandler(dingtalk_stream.AsyncChatbotHandler):
    """
    接收回调消息。
    回复一个卡片，然后更新卡片的文本和图片。
    """

    def __init__(self, logger: logging.Logger = None, max_workers: int = 8):
        super(CardBotHandler, self).__init__(max_workers=max_workers)
        if logger:
            self.logger = logger

        # Initialize chatbot
        self.chatbot = init_chatbot()

    def process(self, callback: dingtalk_stream.CallbackMessage):
        '''
        多线程场景，process函数不要用 async 修饰
        :param message:
        :return:
        '''

        incoming_message = dingtalk_stream.ChatbotMessage.from_dict(callback.data)
        card = deepcopy(INTERACTIVE_CARD_JSON_SAMPLE)
        card["contents"][0]["id"] = f"text_{int(time.time() * 100)}"

        for i, query in enumerate(
            self.chatbot.ask_stream(
                incoming_message.text.content.strip(),
                role=incoming_message.sender_staff_id,
                convo_id=incoming_message.conversation_id,
            )
        ):
            card["contents"][0]["text"] += query
            # 先回复一个文本卡片
            if i == 0:
                card_biz_id = self.reply_card(
                    card,
                    incoming_message,
                    False,
                )
            elif i % 5 == 0:
                self.update_card(
                    card_biz_id,
                    card,
                )

        self.update_card(
            card_biz_id,
            card,
        )

        return AckMessage.STATUS_OK, 'OK'


def main():
    logger = setup_logger()

    credential = dingtalk_stream.Credential(
        dingtalk_settings.app_key, dingtalk_settings.app_secret
    )
    client = dingtalk_stream.DingTalkStreamClient(credential)
    client.register_callback_hanlder(
        dingtalk_stream.chatbot.ChatbotMessage.TOPIC, CardBotHandler(logger)
    )
    client.start_forever()


if __name__ == '__main__':
    main()
