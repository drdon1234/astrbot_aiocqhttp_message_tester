import json
from enum import Enum
from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star, register
from astrbot.api import logger

def to_json(obj, seen=None):
    if seen is None:
        seen = set()
    if isinstance(obj, (str, int, float, bool, type(None))):
        return obj
    oid = id(obj)
    if oid in seen:
        return f"<循环引用 {type(obj).__name__}>"
    seen.add(oid)
    if isinstance(obj, list):
        return [to_json(i, seen) for i in obj]
    if isinstance(obj, dict):
        return {k: to_json(v, seen) for k, v in obj.items()}
    if hasattr(obj, "user_id") and hasattr(obj, "nickname"):
        return {"user_id": obj.user_id, "nickname": obj.nickname}
    if isinstance(obj, Enum):
        return obj.value
    if hasattr(obj, "file_") and hasattr(obj, "url"):
        return {
            "type": obj.type,
            "name": getattr(obj, "name", ""),
            "file_": obj.file_,
            "url": obj.url,
        }
    if hasattr(obj, "text") and hasattr(obj, "convert"):
        return {"type": obj.type, "text": obj.text, "convert": obj.convert}
    if hasattr(obj, "id") and hasattr(obj, "chain"):
        return {"type": obj.type, "id": obj.id, "chain": to_json(obj.chain, seen)}
    if hasattr(obj, "file") and hasattr(obj, "subType"):
        return {
            "type": obj.type,
            "file": obj.file,
            "subType": obj.subType,
            "url": obj.url,
        }
    return str(obj)

def merge_fields(obj):
    keys = [
        "timestamp",
        "self_id",
        "sender",
        "type",
        "session_id",
        "message_id",
        "message",
        "message_str",
        "raw_message",
    ]
    return {
        key: to_json(obj.get(key) if isinstance(obj, dict) else getattr(obj, key, None))
        for key in keys
    }

def json_block(title, json_obj):
    bar = "=" * 25
    end = "=" * 64
    body = json.dumps(json_obj, indent=2, ensure_ascii=False)
    return f"\n\n{bar} {title} {bar}\n{body}\n{end}"

@register("astrbot_aiocqhttp_message_tester", "drdon1234", "使用 logger 完整打印消息结构", "1.1")
class MessageTester(Star):
    def __init__(self, context: Context, config: dict):
        super().__init__(context)
        self.catch_sender_id = config.get("catch_sender_id", "")

    @filter.event_message_type(filter.EventMessageType.ALL)
    async def handle_message(self, event: AstrMessageEvent):
        if str(event.get_sender_id()) != self.catch_sender_id:
            return
        msg_obj = event.message_obj
        raw_log = (
            f"\n\n{'=' * 14} 收到指定用户 \"{self.catch_sender_id}\" 的消息 {'=' * 14}\n"
            f"\n{'=' * 25} 原始消息体 {'=' * 25}\n"
            f"{msg_obj}\n"
            f"{'=' * 64}"
        )
        parsed = merge_fields(msg_obj)
        logger.info(raw_log + json_block("解析后消息体", parsed))
