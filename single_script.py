# coding=utf-8
from commom import base
from utils.logutil import logger
from utils.readmysql import RdTestcase
from utils.requestsutil import RequestSend

case_data = RdTestcase()

title = ''
environment = 'testsae'
path = '/pro/v1/workOrderV2/workTimeRecord/staffList?lang=zh_CN'
request_body = \
'{"corpid": "ding66041eb1c6df73f535c2f4657eb6378f", "userId": "215252650523902241", "platform": "web", "appId": 897, "businessType": 21100, "formId": 10487, "saasMark": 1, "subBusinessType": 21100, "startTime": 1682380800, "endTime": 1682467200, "sortMap": {}, "timeFilter": {}, "listGroupId": 0, "defaultGroup": 1, "commonFilter": {}, "page": 1, "pageSize": 20, "del": 0, "conditions": [], "statusFilter": 0, "isRelatedCustomers": "false", "": 1}'
res_data = None
conf_key = case_data.loadConfkey('xbb', environment)
url = conf_key['value'] + path
headers = eval(conf_key['headers'])
method = 'post'
data = eval(request_body)
case_name = title

data = base.get_data(data)
headers = base.get_headers(data, headers)

try:
    logger.info("正在执行{}用例".format(case_name))
    res_data = RequestSend().send(url, method, data=data, headers=headers)
    logger.info("用例执行成功，请求的结果为\n\t{}".format(res_data))
except:
    logger.info("用例执行失败，请查看日志。")
