from .utils import requests, json


class MsgSender:

    def __init__(self, client_id: str, client_secret: str) -> None:
        self.client_id = client_id
        self.client_secret = client_secret
        if not self.client_id or not self.client_secret:
            raise ValueError("client_id或client_secret未配置")

    def get_token(self):
        """
        获取token。
        """
        url = f"https://oapi.dingtalk.com/gettoken?appkey={self.client_id}&appsecret={self.client_secret}"
        response = requests.get(url)
        if response.status_code != 200:
            raise ValueError("获取token失败")
        return response.json()["access_token"]


class PatchSender(MsgSender):
    """
    批量群发消息。
    [官方文档](https://open.dingtalk.com/document/orgapp/types-of-messages-sent-by-robots?spm=ding_open_doc.document.0.0.1b7d25bcVXddBZ)
    """

    def __init__(self, client_id: str, client_secret: str) -> None:
        super().__init__(client_id, client_secret)
        self.api = "https://api.dingtalk.com/v1.0/robot/oToMessages/batchSend"

    def _send_msg(self, msg_key: str, msgParam: dict, user_ids: list = []):
        """
        发送消息。
        param msg_key: 消息类型。
        param msgParam: 消息参数。
        param user_ids: 用户ID列表，默认为空。
        return: 返回此发送出消息的加密ID。
        """
        token = self.get_token()
        headers = {"x-acs-dingtalk-access-token": token}
        body = {
            "msgParam": str(msgParam),
            "msgKey": msg_key,
            "robotCode": self.client_id,
            "userIds": user_ids,
        }
        response = requests.post(self.api, headers=headers, json=body)
        if response.status_code != 200:
            print(response.json())
            raise ValueError("发送消息失败")
        return response.json()["processQueryKey"]

    def send_text(self, content: str, user_ids: list = []):
        """
        发送文本消息。
        param content: 文本内容。
        param user_ids: 用户ID列表，默认为空。
        """
        msgParam = {"content": content}
        return self._send_msg("sampleText", msgParam, user_ids)

    def send_markdown(self, title: str, content: str, user_ids: list = []):
        """
        发送markdown消息。
        param title: 标题
        param content: 内容
        param user_ids: 用户ID列表，默认为空
        """
        msgParam = {"title": title, "text": content}
        return self._send_msg("sampleMarkdown", msgParam, user_ids)

    def send_img(self, photoURL: str, user_ids: list = []):
        """
        发送图片消息。
        param photoURL: 图片链接。
        param user_ids: 用户ID列表，默认为空。
        """
        msgParam = {"photoURL": photoURL}
        return self._send_msg("sampleImage", msgParam, user_ids)

    def send_link(
        self,
        title: str,
        content: str,
        picUrl: str,
        messageUrl: str,
        user_ids: list = [],
    ):
        """
        发送链接消息。
        param title: 标题
        param content: 内容
        param picUrl: 图片链接
        param messageUrl: 消息链接
        param user_ids: 用户ID列表，默认为空
        """
        msgParam = {
            "title": title,
            "text": content,
            "picUrl": picUrl,
            "messageUrl": messageUrl,
        }
        return self._send_msg("sampleLink", msgParam, user_ids)

    def send_card_1btn(
        self,
        title: str,
        content: str,
        btn_title: str,
        btn_url: str,
        user_ids: list = [],
    ):
        """
        卡片消息：竖向一个按钮。
        param title: 标题
        param content: 内容
        param btn_title: 按钮标题
        param btn_url: 按钮链接
        param user_ids: 用户ID列表，默认为空
        """
        msgParam = {
            "title": title,
            "text": content,
            "singleTitle": btn_title,
            "singleURL": btn_url,
        }
        return self._send_msg("sampleActionCard", msgParam, user_ids)

    def send_card_2btns(
        self,
        title: str,
        content: str,
        btn_title1: str,
        btn_url1: str,
        btn_title2: str,
        btn_url2: str,
        user_ids: list = [],
    ):
        """
        卡片消息：竖向二个按钮。
        param title: 标题
        param content: 内容
        param btn_title1: 按钮1标题
        param btn_url1: 按钮1链接
        param btn_title2: 按钮2标题
        param btn_url2: 按钮2链接
        param user_ids: 用户ID列表，默认为空
        """
        msgParam = {
            "title": title,
            "text": content,
            "actionTitle1": btn_title1,
            "actionURL1": btn_url1,
            "actionTitle2": btn_title2,
            "actionURL2": btn_url2,
        }
        return self._send_msg("sampleActionCard2", msgParam, user_ids)

    def send_card_3btns(
        self,
        title: str,
        content: str,
        btn_title1: str,
        btn_url1: str,
        btn_title2: str,
        btn_url2: str,
        btn_title3: str,
        btn_url3: str,
        user_ids: list = [],
    ):
        """
        卡片消息：竖向三个按钮。
        param title: 标题
        param content: 内容
        param btn_title1: 按钮1标题
        param btn_url1: 按钮1链接
        param btn_title2: 按钮2标题
        param btn_url2: 按钮2链接
        param btn_title3: 按钮3标题
        param btn_url3: 按钮3链接
        param user_ids: 用户ID列表，默认为空
        """
        msgParam = {
            "title": title,
            "text": content,
            "actionTitle1": btn_title1,
            "actionURL1": btn_url1,
            "actionTitle2": btn_title2,
            "actionURL2": btn_url2,
            "actionTitle3": btn_title3,
            "actionURL3": btn_url3,
        }
        return self._send_msg("sampleActionCard3", msgParam, user_ids)

    def send_card_4btns(
        self,
        title: str,
        content: str,
        btn_title1: str,
        btn_url1: str,
        btn_title2: str,
        btn_url2: str,
        btn_title3: str,
        btn_url3: str,
        btn_title4: str,
        btn_url4: str,
        user_ids: list = [],
    ):
        """
        卡片消息：竖向四个按钮。
        param title: 标题
        param content: 内容
        param btn_title1: 按钮1标题
        param btn_url1: 按钮1链接
        param btn_title2: 按钮2标题
        param btn_url2: 按钮2链接
        param btn_title3: 按钮3标题
        param btn_url3: 按钮3链接
        param btn_title4: 按钮4标题
        param btn_url4: 按钮4链接
        param user_ids: 用户ID列表，默认为空
        """
        msgParam = {
            "title": title,
            "text": content,
            "actionTitle1": btn_title1,
            "actionURL1": btn_url1,
            "actionTitle2": btn_title2,
            "actionURL2": btn_url2,
            "actionTitle3": btn_title3,
            "actionURL3": btn_url3,
            "actionTitle4": btn_title4,
            "actionURL4": btn_url4,
        }
        return self._send_msg("sampleActionCard4", msgParam, user_ids)

    def send_card_5btns(
        self,
        title: str,
        content: str,
        btn_title1: str,
        btn_url1: str,
        btn_title2: str,
        btn_url2: str,
        btn_title3: str,
        btn_url3: str,
        btn_title4: str,
        btn_url4: str,
        btn_title5: str,
        btn_url5: str,
        user_ids: list = [],
    ):
        """
        卡片消息：竖向五个按钮。
        param title: 标题
        param content: 内容
        param btn_title1: 按钮1标题
        param btn_url1: 按钮1链接
        param btn_title2: 按钮2标题
        param btn_url2: 按钮2链接
        param btn_title3: 按钮3标题
        param btn_url3: 按钮3链接
        param btn_title4: 按钮4标题
        param btn_url4: 按钮4链接
        param btn_title5: 按钮5标题
        param btn_url5: 按钮5链接
        param user_ids: 用户ID列表，默认为空
        """
        msgParam = {
            "title": title,
            "text": content,
            "actionTitle1": btn_title1,
            "actionURL1": btn_url1,
            "actionTitle2": btn_title2,
            "actionURL2": btn_url2,
            "actionTitle3": btn_title3,
            "actionURL3": btn_url3,
            "actionTitle4": btn_title4,
            "actionURL4": btn_url4,
            "actionTitle5": btn_title5,
            "actionURL5": btn_url5,
        }
        return self._send_msg("sampleActionCard5", msgParam, user_ids)

    def send_card_2btns_horizontal(
        self,
        title: str,
        content: str,
        btn_title1: str,
        btn_url1: str,
        btn_title2: str,
        btn_url2: str,
        user_ids: list = [],
    ):
        """
        卡片消息：横向二个按钮。
        param title: 标题
        param content: 内容
        param btn_title1: 按钮1标题
        param btn_url1: 按钮1链接
        param btn_title2: 按钮2标题
        param btn_url2: 按钮2链接
        param user_ids: 用户ID列表，默认为空
        """
        msgParam = {
            "title": title,
            "text": content,
            "buttonTitle1": btn_title1,
            "buttonUrl1": btn_url1,
            "buttonTitle2": btn_title2,
            "buttonUrl2": btn_url2,
        }
        return self._send_msg("sampleActionCard6", msgParam, user_ids)

    def send_audio(self, mediaId: str, duration: str, user_ids: list = []):
        """
        发送音频消息。
        param mediaId: 通过上传媒体文件接口，获取media_id参数值。[如何上传?](https://open.dingtalk.com/document/orgapp/upload-media-files?spm=ding_open_doc.document.0.0.57fab17d1iIbZF)
        param duration: 音频时长，单位毫秒。
        """
        msgParam = {"mediaId": mediaId, "duration": duration}
        return self._send_msg("sampleAudio", msgParam, user_ids)

    def send_file(
        self, mediaId: str, fileName: str, fileType: str, user_ids: list = []
    ):
        """
        发送文件消息。
        param mediaId: 通过上传媒体文件接口，获取media_id参数值。[如何上传?](https://open.dingtalk.com/document/orgapp/upload-media-files?spm=ding_open_doc.document.0.0.57fab17d1iIbZF)
        param fileName: 文件名。
        param fileType: 文件类型。
        param user_ids: 用户ID列表，默认为空。
        """
        msgParam = {"mediaId": mediaId, "fileName": fileName, "fileType": fileType}
        return self._send_msg("sampleFile", msgParam, user_ids)

    def send_video(
        self,
        videoMediaId: str,
        duration: str,
        videoType: str,
        picMediaId: str,
        height: str,
        width: str,
        user_ids: list = [],
    ):
        """
        发送视频消息。
        param videoMediaId: 通过上传媒体文件接口，获取media_id参数值。[如何上传?](https://open.dingtalk.com/document/orgapp/upload-media-files?spm=ding_open_doc.document.0.0.57fab17d1iIbZF)
        param duration: 语音消息时长，单位秒。
        param videoType: 视频类型，支持mp4格式。
        param picMediaId: 视频封面图，通过上传媒体文件接口，获取media_id参数值。
        param height: 视频展示高度，单位px。
        param width: 视频展示宽度，单位px。
        """
        msgParam = {
            "videoMediaId": videoMediaId,
            "duration": duration,
            "videoType": videoType,
            "picMediaId": picMediaId,
            "height": height,
            "width": width,
        }
        return self._send_msg("sampleVideo", msgParam, user_ids)


class GroupSender(MsgSender):

    def __init__(self, client_id: str, client_secret: str) -> None:
        """
        初始化。
        param client_id: 客户端ID。
        param client_secret: 客户端密钥。
        """
        super().__init__(client_id, client_secret)
        self.api = "https://api.dingtalk.com/v1.0/robot/groupMessages/send"

    def _send_msg(self, msg_key: str, msgParam: dict, openConversationId: str):
        """
        发送消息。
        param msg_key: 消息类型。
        param msgParam: 消息参数。
        param openConversationId: 群ID。
        return: 返回此发送出消息的加密ID。
        """
        token = self.get_token()
        headers = {"x-acs-dingtalk-access-token": token}
        body = {
            "msgParam": str(msgParam),
            "msgKey": msg_key,
            "robotCode": self.client_id,
            "openConversationId": openConversationId,
        }
        response = requests.post(self.api, headers=headers, json=body)
        if response.status_code != 200:
            print(response.json())
            raise ValueError("发送消息失败")
        return response.json()["processQueryKey"]

    def send_text(self, content: str, openConversationId: str):
        """
        发送文本消息。
        param content: 文本内容。
        param openConversationId: 群ID。
        """
        msgParam = {"content": content}
        return self._send_msg("sampleText", msgParam, openConversationId)

    def send_markdown(self, title: str, content: str, openConversationId: str):
        """
        发送markdown消息。
        param title: 标题
        param content: 内容
        param openConversationId: 群ID
        """
        msgParam = {"title": title, "text": content}
        return self._send_msg("sampleMarkdown", msgParam, openConversationId)

    def send_img(self, photoURL: str, openConversationId: str):
        """
        发送图片消息。
        param photoURL: 图片链接。
        param openConversationId: 群ID。
        """
        msgParam = {"photoURL": photoURL}
        return self._send_msg("sampleImage", msgParam, openConversationId)

    def send_link(
        self,
        title: str,
        content: str,
        picUrl: str,
        messageUrl: str,
        openConversationId: str,
    ):
        """
        发送链接消息。
        param title: 标题
        param content: 内容
        param picUrl: 图片链接
        param messageUrl: 消息链接
        param openConversationId: 群ID
        """
        msgParam = {
            "title": title,
            "text": content,
            "picUrl": picUrl,
            "messageUrl": messageUrl,
        }
        return self._send_msg("sampleLink", msgParam, openConversationId)

    def send_card_1btn(
        self,
        title: str,
        content: str,
        btn_title: str,
        btn_url: str,
        openConversationId: str,
    ):
        """
        卡片消息：竖向一个按钮。
        param title: 标题
        param content: 内容
        param btn_title: 按钮标题
        param btn_url: 按钮链接
        param openConversationId: 群ID
        """
        msgParam = {
            "title": title,
            "text": content,
            "singleTitle": btn_title,
            "singleURL": btn_url,
        }
        return self._send_msg("sampleActionCard", msgParam, openConversationId)

    def send_card_2btns(
        self,
        title: str,
        content: str,
        btn_title1: str,
        btn_url1: str,
        btn_title2: str,
        btn_url2: str,
        openConversationId: str,
    ):
        """
        卡片消息：竖向二个按钮。
        param title: 标题
        param content: 内容
        param btn_title1: 按钮1标题
        param btn_url1: 按钮1链接
        param btn_title2: 按钮2标题
        param btn_url2: 按钮2链接
        param openConversationId: 群ID
        """
        msgParam = {
            "title": title,
            "text": content,
            "actionTitle1": btn_title1,
            "actionURL1": btn_url1,
            "actionTitle2": btn_title2,
            "actionURL2": btn_url2,
        }
        return self._send_msg("sampleActionCard2", msgParam, openConversationId)

    def send_card_3btns(
        self,
        title: str,
        content: str,
        btn_title1: str,
        btn_url1: str,
        btn_title2: str,
        btn_url2: str,
        btn_title3: str,
        btn_url3: str,
        openConversationId: str,
    ):
        """
        卡片消息：竖向三个按钮。
        param title: 标题
        param content: 内容
        param btn_title1: 按钮1标题
        param btn_url1: 按钮1链接
        param btn_title2: 按钮2标题
        param btn_url2: 按钮2链接
        param btn_title3: 按钮3标题
        param btn_url3: 按钮3链接
        param openConversationId: 群ID
        """
        msgParam = {
            "title": title,
            "text": content,
            "actionTitle1": btn_title1,
            "actionURL1": btn_url1,
            "actionTitle2": btn_title2,
            "actionURL2": btn_url2,
            "actionTitle3": btn_title3,
            "actionURL3": btn_url3,
        }
        return self._send_msg("sampleActionCard3", msgParam, openConversationId)

    def send_card_4btns(
        self,
        title: str,
        content: str,
        btn_title1: str,
        btn_url1: str,
        btn_title2: str,
        btn_url2: str,
        btn_title3: str,
        btn_url3: str,
        btn_title4: str,
        btn_url4: str,
        openConversationId: str,
    ):
        """
        卡片消息：竖向四个按钮。
        param title: 标题
        param content: 内容
        param btn_title1: 按钮1标题
        param btn_url1: 按钮1链接
        param btn_title2: 按钮2标题
        param btn_url2: 按钮2链接
        param btn_title3: 按钮3标题
        param btn_url3: 按钮3链接
        param btn_title4: 按钮4标题
        param btn_url4: 按钮4链接
        param openConversationId: 群ID
        """
        msgParam = {
            "title": title,
            "text": content,
            "actionTitle1": btn_title1,
            "actionURL1": btn_url1,
            "actionTitle2": btn_title2,
            "actionURL2": btn_url2,
            "actionTitle3": btn_title3,
            "actionURL3": btn_url3,
            "actionTitle4": btn_title4,
            "actionURL4": btn_url4,
        }
        return self._send_msg("sampleActionCard4", msgParam, openConversationId)

    def send_card_5btns(
        self,
        title: str,
        content: str,
        btn_title1: str,
        btn_url1: str,
        btn_title2: str,
        btn_url2: str,
        btn_title3: str,
        btn_url3: str,
        btn_title4: str,
        btn_url4: str,
        btn_title5: str,
        btn_url5: str,
        openConversationId: str,
    ):
        """
        卡片消息：竖向五个按钮。
        param title: 标题
        param content: 内容
        param btn_title1: 按钮1标题
        param btn_url1: 按钮1链接
        param btn_title2: 按钮2标题
        param btn_url2: 按钮2链接
        param btn_title3: 按钮3标题
        param btn_url3: 按钮3链接
        param btn_title4: 按钮4标题
        param btn_url4: 按钮4链接
        param btn_title5: 按钮5标题
        param btn_url5: 按钮5链接
        param openConversationId: 群ID
        """
        msgParam = {
            "title": title,
            "text": content,
            "actionTitle1": btn_title1,
            "actionURL1": btn_url1,
            "actionTitle2": btn_title2,
            "actionURL2": btn_url2,
            "actionTitle3": btn_title3,
            "actionURL3": btn_url3,
            "actionTitle4": btn_title4,
            "actionURL4": btn_url4,
            "actionTitle5": btn_title5,
            "actionURL5": btn_url5,
        }
        return self._send_msg("sampleActionCard5", msgParam, openConversationId)

    def send_card_2btns_horizontal(
        self,
        title: str,
        content: str,
        btn_title1: str,
        btn_url1: str,
        btn_title2: str,
        btn_url2: str,
        openConversationId: str,
    ):
        """
        卡片消息：横向二个按钮。
        param title: 标题
        param content: 内容
        param btn_title1: 按钮1标题
        param btn_url1: 按钮1链接
        param btn_title2: 按钮2标题
        param btn_url2: 按钮2链接
        param openConversationId: 群ID
        """
        msgParam = {
            "title": title,
            "text": content,
            "buttonTitle1": btn_title1,
            "buttonUrl1": btn_url1,
            "buttonTitle2": btn_title2,
            "buttonUrl2": btn_url2,
        }
        return self._send_msg("sampleActionCard6", msgParam, openConversationId)

    def send_audio(self, mediaId: str, duration: str, openConversationId: str):
        """
        发送音频消息。
        param mediaId: 通过上传媒体文件接口，获取media_id参数值。[如何上传?](https://open.dingtalk.com/document/orgapp/upload-media-files?spm=ding_open_doc.document.0.0.57fab17d1iIbZF)
        param duration: 音频时长，单位毫秒。
        """
        msgParam = {"mediaId": mediaId, "duration": duration}
        return self._send_msg("sampleAudio", msgParam, openConversationId)

    def send_file(
        self, mediaId: str, fileName: str, fileType: str, openConversationId: str
    ):
        """
        发送文件消息。
        param mediaId: 通过上传媒体文件接口，获取media_id参数值。[如何上传?](https://open.dingtalk.com/document/orgapp/upload-media-files?spm=ding_open_doc.document.0.0.57fab17d1iIbZF)
        param fileName: 文件名。
        param fileType: 文件类型。
        param openConversationId: 群ID。
        """
        msgParam = {"mediaId": mediaId, "fileName": fileName, "fileType": fileType}
        return self._send_msg("sampleFile", msgParam, openConversationId)

    def send_video(
        self,
        videoMediaId: str,
        duration: str,
        videoType: str,
        picMediaId: str,
        height: str,
        width: str,
        openConversationId: str,
    ):
        """
        发送视频消息。
        param videoMediaId: 通过上传媒体文件接口，获取media_id参数值。[如何上传?](https://open.dingtalk.com/document/orgapp/upload-media-files?spm=ding_open_doc.document.0.0.57fab17d1iIbZF)
        param duration: 视频消息时长，单位秒。
        param videoType: 视频类型，支持mp4格式。
        param picMediaId: 视频封面图，通过上传媒体文件接口，获取media_id参数值。
        param height: 视频展示高度，单位px。
        param width: 视频展示宽度，单位px。
        """
        msgParam = {
            "videoMediaId": videoMediaId,
            "duration": duration,
            "videoType": videoType,
            "picMediaId": picMediaId,
            "height": height,
            "width": width,
        }
        return self._send_msg("sampleVideo", msgParam, openConversationId)


if __name__ == "__main__":

    with open("config.json", "r") as f:
        config = json.load(f)

    sender = PatchSender(
        client_id=config["client_id"], client_secret=config["client_secret"]
    )

    sender.send_markdown(
        title="bot测试", content="**Hello World!**", user_ids=config["user_ids"]
    )
