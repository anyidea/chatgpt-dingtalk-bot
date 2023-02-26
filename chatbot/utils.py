import uuid


def get_conversation_id(convo_id: str):
    """
    将钉钉会话id转成uuid
    """
    return str(uuid.uuid5(uuid.NAMESPACE_DNS, convo_id))
