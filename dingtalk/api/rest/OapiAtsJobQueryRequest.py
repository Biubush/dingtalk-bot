'''
Created by auto_sdk on 2021.02.26
'''
from dingtalk.api.base import RestApi
class OapiAtsJobQueryRequest(RestApi):
	def __init__(self,url=None):
		RestApi.__init__(self,url)
		self.biz_code = None
		self.cursor = None
		self.query_param = None
		self.size = None

	def getHttpMethod(self):
		return 'POST'

	def getapiname(self):
		return 'dingtalk.oapi.ats.job.query'
