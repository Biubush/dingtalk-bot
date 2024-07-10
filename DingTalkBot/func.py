from .utils import json, os, re


def context_recorder(user_id: str, user_msg: str, bot_msg: str):
    """
    记录用户和机器人的对话,对话限定最长20段来回,超过长度则删除最旧的，将新的对话追加到文件末尾
    按照json格式存储，存入一个列表[user_msg,bot_msg]
    param user_id: 用户ID
    param user_msg: 用户输入的消息
    param bot_msg: 机器人回复的消息
    """
    folder_path = "contexts"
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    file_path = f"contexts/{user_id}.json"
    try:
        with open(file_path, "r") as f:
            record = json.load(f)
    except:
        record = []
    record.append([user_msg, bot_msg])
    if len(record) > 20:
        record.pop(0)
    with open(file_path, "w") as f:
        json.dump(record, f)


def context_reader(user_id: str) -> tuple:
    """
    读取用户和机器人的对话
    param user_id: 用户ID
    return: 对话记录列表,对话记录是否已满
    """
    folder_path = "contexts"
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    file_path = f"contexts/{user_id}.json"
    try:
        with open(file_path, "r") as f:
            record = json.load(f)
    except:
        record = []
    full = False
    if len(record) >= 20:
        full = True
    return record, full


def add_public_context(context: list):
    """
    添加公共对话记录,可以用于预设机器人
    param context: 对话记录列表,每个元素为一个列表[user_msg,bot_msg],最多50个元素
    """
    folder_path = "contexts"
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    file_path = f"contexts/public.json"
    try:
        with open(file_path, "r") as f:
            record = json.load(f)
    except:
        record = []
    record.extend(context)
    if len(record) > 50:
        record = record[-50:]
    with open(file_path, "w") as f:
        json.dump(record, f)


def read_public_context() -> list:
    """
    读取公共对话记录
    return: 对话记录列表
    """
    folder_path = "contexts"
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    file_path = f"contexts/public.json"
    try:
        with open(file_path, "r") as f:
            record = json.load(f)
    except:
        record = []
    return record

def delete_public_context():
    """
    删除公共对话记录
    """
    folder_path = "contexts"
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    file_path = f"contexts/public.json"
    try:
        os.remove(file_path)
    except:
        pass

def context_deleter(user_id: str):
    """
    删除用户和机器人的对话记录
    param user_id: 用户ID
    """
    folder_path = "contexts"
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    file_path = f"contexts/{user_id}.json"
    try:
        os.remove(file_path)
    except:
        pass
