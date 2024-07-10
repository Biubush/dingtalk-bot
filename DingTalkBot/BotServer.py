from .utils import dingtalk_stream, json
from .MsgSender import PatchSender, GroupSender
from .AiModle import *
from .func import (
    context_reader,
    context_recorder,
    context_deleter,
    add_public_context,
    read_public_context,
    delete_public_context,
)

mygpt = GPT4Free()


class CalcBotHandler(dingtalk_stream.ChatbotHandler):
    """
    处理收到的钉钉机器人消息的类。

    方法:
        process(callback: dingtalk_stream.CallbackMessage) -> tuple[int, str]:
            处理收到的消息，提取并打印表达式，并返回处理状态和消息。
    """

    def __init__(self, PatchSender: PatchSender, GroupSender: GroupSender):
        """
        初始化处理器。

        参数:
            PatchSender (PatchSender): 消息发送器对象。
        """
        self.PatchSender = PatchSender
        self.GroupSender = GroupSender

    async def process(
        self, callback: dingtalk_stream.CallbackMessage
    ) -> tuple[int, str]:
        """
        处理收到的回调消息。

        参数:
            callback (dingtalk_stream.CallbackMessage): 钉钉机器人收到的回调消息对象。
            回调消息对象各字段说明:
            - spec_version (str): 消息规范版本。
            - type (str): 消息类型，此处为 CALLBACK。
            - headers (dingtalk_stream.Headers): 消息头部信息，包含应用程序 ID、连接 ID 等。
            - data (dict): 实际的消息数据，包含各种字段来描述收到的消息内容。
                - senderPlatform (str): 发送消息的平台，例如 Android。
                - conversationId (str): 对话 ID，标识消息所属的对话。
                - chatbotCorpId (str): 机器人所属的企业 ID。
                - chatbotUserId (str): 机器人的用户 ID。
                - msgId (str): 消息 ID，唯一标识一条消息。
                - senderNick (str): 发送者昵称。
                - isAdmin (bool): 发送者是否为管理员。
                - senderStaffId (str): 发送者的员工 ID。
                - sessionWebhookExpiredTime (int): 会话 Webhook 过期时间。
                - createAt (int): 消息创建时间戳。
                - senderCorpId (str): 发送者所属的企业 ID。
                - conversationType (str): 对话类型，例如 '1' 表示单聊。
                - senderId (str): 发送者 ID。
                - sessionWebhook (str): 会话 Webhook 地址。
                - text (dict): 文本消息内容。
                    - content (str): 文本消息的内容。
                - robotCode (str): 机器人代码。
                - msgtype (str): 消息类型，例如 'text' 表示文本消息。
            - extensions (dict): 扩展信息，一般为空字典或包含额外信息。
        返回:
            tuple[int, str]: 返回一个包含处理状态和消息的元组。
                - int: 处理状态，固定为 dingtalk_stream.AckMessage.STATUS_OK。
                - str: 处理结果消息，固定为 'OK'。


        """
        incoming_message = dingtalk_stream.ChatbotMessage.from_dict(callback.data)
        expression = incoming_message.text.content.strip()  # 提取并清理消息内容
        # 判断是否是群聊
        if callback.data["conversationType"] == "2":
            print(callback.data["conversationId"])
            # 群聊
            if expression == "/clear":
                context_deleter(callback.data["senderStaffId"])
                self.GroupSender.send_markdown(
                    title="AI回复",
                    content="**对话记录已清空**",
                    openConversationId=callback.data["conversationId"],
                )
                return dingtalk_stream.AckMessage.STATUS_OK, "OK"
            if expression == "/clear_public":
                delete_public_context()
                self.GroupSender.send_markdown(
                    title="AI回复",
                    content="**公共对话记录已清空**",
                    openConversationId=callback.data["conversationId"],
                )
                return dingtalk_stream.AckMessage.STATUS_OK, "OK"
            openConversationId = callback.data["conversationId"]
            self.GroupSender.send_markdown(
                title="AI回复",
                content="**正在思考中，请稍等**",
                openConversationId=openConversationId,
            )
            personal_context, full_warning = context_reader(
                callback.data["senderStaffId"]
            )
            public_context = read_public_context()
            context = public_context + personal_context
            if full_warning:
                self.GroupSender.send_markdown(
                    title="AI回复",
                    content="**对话长度已满，将舍弃最旧对话**",
                    openConversationId=openConversationId,
                )
            if "/public" in expression:
                # 获取public字符串后面的内容，添加到公共对话记录
                public_context = expression.split("/public")[1].strip()
                old_expression = expression
                expression = public_context
            reply = mygpt.ask(expression, context)
            self.GroupSender.send_markdown(
                title="AI回复", content=reply, openConversationId=openConversationId
            )
            if "/public" in old_expression:
                con_list = [expression, reply]
                add_public_context(con_list)
                self.GroupSender.send_markdown(
                    title="AI回复",
                    content="**已添加到公共对话记录**",
                    openConversationId=openConversationId,
                )
            else:
                context_recorder(callback.data["senderStaffId"], expression, reply)

        else:
            # 单聊
            if expression == "/clear":
                context_deleter(callback.data["senderStaffId"])
                self.PatchSender.send_markdown(
                    title="AI回复",
                    content="**对话记录已清空**",
                    user_ids=[callback.data["senderStaffId"]],
                )
                return dingtalk_stream.AckMessage.STATUS_OK, "OK"
            if expression == "/clear_public":
                delete_public_context()
                self.GroupSender.send_markdown(
                    title="AI回复",
                    content="**公共对话记录已清空**",
                    openConversationId=callback.data["conversationId"],
                )
                return dingtalk_stream.AckMessage.STATUS_OK, "OK"
            sender_id = callback.data["senderStaffId"]
            self.PatchSender.send_markdown(
                title="AI回复", content="**正在思考中，请稍等**", user_ids=[sender_id]
            )
            personal_context, full_warning = context_reader(
                callback.data["senderStaffId"]
            )
            public_context = read_public_context()
            context = public_context + personal_context
            if full_warning:
                self.PatchSender.send_markdown(
                    title="AI回复",
                    content="**对话长度已满，将舍弃最旧对话**",
                    user_ids=[sender_id],
                )
            if "/public" in expression:
                # 获取public字符串后面的内容，添加到公共对话记录
                public_context = expression.split("/public")[1].strip()
                old_expression = expression
                expression = public_context

            reply = mygpt.ask(expression, context)
            self.PatchSender.send_markdown(
                title="AI回复", content=reply, user_ids=[sender_id]
            )

            if "/public" in old_expression:
                # 获取public字符串后面的内容，添加到公共对话记录
                con_list = [expression, reply]
                add_public_context(con_list)
                self.PatchSender.send_markdown(
                    title="AI回复",
                    content="**已添加到公共对话记录**",
                    user_ids=[sender_id],
                )
            else:
                context_recorder(callback.data["senderStaffId"], expression, reply)

        return dingtalk_stream.AckMessage.STATUS_OK, "OK"


class BotServer:

    def __init__(self, client_id: str, client_secret: str) -> None:
        self.client_id = client_id
        self.client_secret = client_secret
        if not self.client_id or not self.client_secret:
            raise ValueError("client_id或client_secret未配置")

    def run(self):
        """
        服务端启动函数

        操作步骤:
            1. 创建消息发送器对象。
            2. 创建凭证对象。
            3. 创建钉钉流客户端对象。
            4. 注册回调处理程序。
            5. 启动客户端并持续运行。
        """
        # 创建消息发送器对象
        patch_sender = PatchSender(
            client_id=self.client_id, client_secret=self.client_secret
        )
        group_sender = GroupSender(
            client_id=self.client_id, client_secret=self.client_secret
        )
        # 创建凭证对象
        credential = dingtalk_stream.Credential(self.client_id, self.client_secret)
        # 创建钉钉流客户端对象
        client = dingtalk_stream.DingTalkStreamClient(credential)
        # 注册回调处理程序
        client.register_callback_handler(
            dingtalk_stream.chatbot.ChatbotMessage.TOPIC,
            CalcBotHandler(PatchSender=patch_sender, GroupSender=group_sender),
        )
        # 启动客户端并持续运行
        client.start_forever()


if __name__ == "__main__":

    with open("config.json", "r") as f:
        config = json.load(f)
    server = BotServer(
        client_id=config["client_id"], client_secret=config["client_secret"]
    )
    server.run()
