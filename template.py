# template.py

# -*- coding: utf-8 -*-
"""
模板文件 template.py

本文件仅包含注释，示例如何在插件中通过键名
获取原始消息体（msg_obj）中的任意键对应的值，
并兼容 dict、对象属性、嵌套结构等各种情况。
"""

# -------------------------------------------------------------------
# 1. 准备工作：假设已有以下变量
# -------------------------------------------------------------------
# event: AstrMessageEvent 对象
# msg_obj = event.message_obj  # 原始消息体

# -------------------------------------------------------------------
# 2. 定义统一取值函数
# -------------------------------------------------------------------
# def get_field_value(obj, key):
#     """
#     通用获取 obj 中键 key 对应值。
#     支持以下情况：
#       1. obj 是 dict：返回 obj.get(key)
#       2. obj 有属性 key：返回 getattr(obj, key)
#       3. obj 是列表或元组：遍历每项递归获取（若 key 为索引或通用键）
#       4. 嵌套路径：支持 key1.key2.key3 形式
#     :param obj: dict、对象、列表等
#     :param key: 单个键名 或 嵌套路径（用 . 分隔）
#     :return: 对应值或 None
#     """
#     # 处理嵌套路径
#     parts = key.split(".")
#     current = obj
#     for part in parts:
#         if current is None:
#             return None
#         # 列表索引情况：part 如果能转换为整数，则当列表索引
#         if isinstance(current, (list, tuple)):
#             try:
#                 idx = int(part)
#                 current = current[idx]
#                 continue
#             except Exception:
#                 # 非 index，则对列表中每项尝试获取
#                 results = []
#                 for item in current:
#                     val = get_field_value(item, part)
#                     if val is not None:
#                         results.append(val)
#                 return results if results else None
#         # dict 情况
#         if isinstance(current, dict):
#             current = current.get(part)
#             continue
#         # 对象属性情况
#         if hasattr(current, part):
#             current = getattr(current, part)
#             continue
#         # Enum 或其他类型通过 str 转取
#         try:
#             current = current[part]
#         except Exception:
#             return None
#     return current

# -------------------------------------------------------------------
# 3. 使用示例
# -------------------------------------------------------------------
# 以下示例展示如何获取多种情况的字段：
# timestamp = get_field_value(msg_obj, "timestamp")
# sender_id = get_field_value(msg_obj, "sender.user_id")
# first_message_type = get_field_value(msg_obj, "message.0.type")
# all_plain_texts = get_field_value(msg_obj, "message.text")
#
# 上述调用可同时处理：
#   • sender 作为对象或 dict
#   • message 列表中指定索引或全部项
#   • 嵌套字典、对象属性

# -------------------------------------------------------------------
# 4. 结合 to_json 友好输出（可选）
# -------------------------------------------------------------------
# 如果希望将取出的值转换为 JSON 兼容格式，可：
# formatted = to_json(get_field_value(msg_obj, key))
# print(json.dumps(formatted, indent=2, ensure_ascii=False))

# -------------------------------------------------------------------
# 5. 集成到 handle_message 中
# -------------------------------------------------------------------
# async def handle_message(self, event: AstrMessageEvent):
#     msg_obj = event.message_obj
#     # 定义需要获取的键或路径列表
#     keys = [
#         "timestamp",
#         "self_id",
#         "sender.user_id",
#         "sender.nickname",
#         "message.0.type",
#         "message.text",
#         "raw_message.sender.nickname",
#     ]
#     for key in keys:
#         value = get_field_value(msg_obj, key)
#         logger.info(f"字段 {key} => {value}")

# -------------------------------------------------------------------
# 6. 拓展与注意事项
# -------------------------------------------------------------------
# - 嵌套路径可根据需要任意组合，如 "raw_message.message.2.data.url"
# - 列表索引越界或不存在时返回 None
# - 列表通用取值返回 list 结果，结果为空时视为 None
# - 若需捕获异常或默认值，可在函数内部添加 try/except、default 参数
# - 推荐将该模板函数移至 util 模块，方便复用
