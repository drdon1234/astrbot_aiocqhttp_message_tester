from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star, register
from astrbot.api import logger

@register("astrbot_aiocqhttp_message_tester", "drdon1234", "使用 logger 完整打印消息结构", "1.0")
class MessageTester(Star):
    def __init__(self, context: Context, config: dict):
        super().__init__(context)
        self.catch_sender_id = config.get("catch_sender_id", "")

    @filter.event_message_type(filter.EventMessageType.ALL)
    async def handle_message(self, event: AstrMessageEvent):
        try:
            if event.get_sender_id() == self.catch_sender_id:
                msg_obj = event.message_obj
                logger.info("=== 开始打印消息结构 ===")
                parsed_chain = getattr(msg_obj, "message", [])
                logger.info("Parsed message components:")
                for idx, comp in enumerate(parsed_chain, start=1):
                    logger.info(f"  Component #{idx}: {comp!r}")
                raw = getattr(msg_obj, "raw_message", None)
                if raw is not None:
                    logger.info("Raw message data:")
                    logger.info(f"  {raw!r}")
                logger.info("=== 打印结束 ===")
        except Exception as e:
            logger.error(f"打印消息结构出错：{e}")
