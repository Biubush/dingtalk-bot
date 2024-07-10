from .utils import requests,json
import dingtalk

class MediaHanler:
    def __init__(self, client_id: str, client_secret: str) -> None:
        """
        初始化媒体文件工作台
        Parameters:
            - client_id: 钉钉 API 的 client_id
            - client_secret: 钉钉 API 的 client_secret
        
        """
        self.client_id = client_id
        self.client_secret = client_secret
        if not self.client_id or not self.client_secret:
            raise ValueError("client_id或client_secret未配置")
        
    def _get_token(self):
        """
        获取token。
        """
        url = f"https://oapi.dingtalk.com/gettoken?appkey={self.client_id}&appsecret={self.client_secret}"
        response = requests.get(url)
        if response.status_code != 200:
            raise ValueError("获取token失败")
        return response.json()["access_token"]
    

class MediaUploader(MediaHanler):
    
    def _recognize(file_path:str)->str:
        """
        识别文件类型，传入路径，返回类型
        参数：
            - file_path: 文件路径
        返回值：
            - str: 文件类型
            媒体文件类型：
                - image：图片，图片最大20MB。支持上传jpg、gif、png、bmp格式。
                - voice：语音，语音文件最大2MB。支持上传amr、mp3、wav格式。
                - video：视频，视频最大20MB。支持上传mp4格式。
                - file：普通文件，最大20MB。支持上传doc、docx、xls、xlsx、ppt、pptx、zip、pdf、rar格式。
        """
        file_type = file_path.split('.')[-1]
        if file_type in ["jpg","gif","png","bmp"]:
            return "image"
        elif file_type in ["amr","mp3","wav"]:
            return "voice"
        elif file_type in ["mp4"]:
            return "video"
        else:
            return "file"
        
    def upload(self,file_path:str,store_name:str="")->str:
        """
        上传媒体文件，传入文件路径，返回媒体ID

        
        参数：
            - file_path: 文件路径


        返回值：
            - str: 媒体ID
        """
        token = self._get_token()
        req=dingtalk.api.OapiMediaUploadRequest("https://oapi.dingtalk.com/media/upload")

        req.type=self._recognize(file_path)
        if store_name=="":
            store_name = file_path.split('/')[-1]
        req.media=dingtalk.api.FileItem(store_name,open(file_path,'rb'))
        try:
            resp= req.getResponse(token)
            return resp["media_id"]
        except Exception as e:
            raise Exception(e)
        

if __name__ == "__main__":

    with open("config.json","r") as f:
        config = json.load(f)
    uploader = MediaUploader(
        client_id=config["client_id"],
        client_secret=config["client_secret"]
    )
    media_id=uploader.upload("upload_test.txt")
    print(media_id)