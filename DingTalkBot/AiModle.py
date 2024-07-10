from g4f.client import Client
from g4f import Provider
import json
from sparkai.llm.llm import ChatSparkLLM, ChunkPrintHandler
from sparkai.core.messages import ChatMessage


class GPT4Free:

    def __init__(self):
        """
        初始化g4f_ai
        """

    def ask(self, msg: str, context: list = []) -> str:
        """
        调用g4f进行问答
        param msg: 用户输入的问题
        param context: 上下文，格式为[[用户问题1,机器人回答1],[用户问题2,机器人回答2],...]
        return: AI的回答
        """
        client = Client(provider=Provider.Blackbox)
        messages = []
        messages.append({"role": "system", "content": "你是一个中文问答助手，无特殊情况不要用英语回复"})
        for thismsg in context:
            messages.append({"role": "user", "content": thismsg[0]})
            messages.append({"role": "assistant", "content": thismsg[1]})
        messages.append({"role": "user", "content": msg})
        response = client.chat.completions.create(
            model="gpt-3.5-turbo", messages=messages
        )
        rt_text = response.choices[0].message.content
        last_dollar_index = rt_text.rfind("$")
        result = rt_text[last_dollar_index + 1 :]
        return result


class SparkAI:
    """
    星火认知大模型
    """

    def __init__(self, spark_app_id: str, spark_api_key: str, spark_api_secret: str):
        """
        初始化
        param spark_app_id: 星火认知大模型的app_id
        param spark_api_key: 星火认知大模型的api_key
        param spark_api_secret: 星火认知大模型的api_secret
        """
        self.app_id = spark_app_id
        self.api_key = spark_api_key
        self.api_secret = spark_api_secret

    def _ask(self, api_url: str, llm_domain: str, msg: str, context: list = []) -> str:
        """
        调用接口进行问答
        param api_url: 对应大模型的URL
        param llm_domain: 对应大模型的domain
        """
        spark = ChatSparkLLM(
            spark_api_url=api_url,
            spark_app_id=self.app_id,
            spark_api_key=self.api_key,
            spark_api_secret=self.api_secret,
            spark_llm_domain=llm_domain,
            streaming=False,
            max_tokens=8192,
        )
        messages = []
        for thismsg in context:
            messages.append(ChatMessage(role="user", content=thismsg[0]))
            messages.append(ChatMessage(role="assistant", content=thismsg[1]))
        messages.append(ChatMessage(role="user", content=msg))
        handler = ChunkPrintHandler()
        a = spark.generate([messages], callbacks=[handler])
        return a.generations[0][0].text

    def sparkUltra(self, msg: str, context: list = []) -> str:
        """
        调用星火认知大模型Spark4.0Ultra进行问答
        param msg: 用户输入的问题
        """
        return self._ask(
            "wss://spark-api.xf-yun.com/v4.0/chat", "4.0Ultra", msg, context
        )

    def sparkMax(self, msg: str, context: list = []) -> str:
        """
        调用星火认知大模型Spark Max进行问答
        param msg: 用户输入的问题
        """
        return self._ask(
            "wss://spark-api.xf-yun.com/v3.5/chat", "generalv3.5", msg, context
        )

    def sparkPro(self, msg: str, context: list = []) -> str:
        """
        调用星火认知大模型Spark Pro进行问答
        param msg: 用户输入的问题
        """
        return self._ask(
            "wss://spark-api.xf-yun.com/v3.1/chat", "generalv3", msg, context
        )

    def sparkV2(self, msg: str, context: list = []) -> str:
        """
        调用星火认知大模型Spark V2进行问答
        param msg: 用户输入的问题
        """
        return self._ask(
            "wss://spark-api.xf-yun.com/v2.1/chat", "generalv2", msg, context
        )

    def sparkLite(self, msg: str, context: list = []) -> str:
        """
        调用星火认知大模型Spark Lite进行问答
        param msg: 用户输入的问题
        """
        return self._ask(
            "wss://spark-api.xf-yun.com/v1.1/chat", "general", msg, context
        )


if __name__ == "__main__":
    with open("config.json", "r") as f:
        config = json.load(f)
    ai_config = config["AI"]
    spark_ai = SparkAI(
        ai_config["app_id"], ai_config["api_key"], ai_config["api_secret"]
    )
    print(spark_ai.sparkUltra("你好"))
