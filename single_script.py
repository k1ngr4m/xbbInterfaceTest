# coding=utf-8
from commom import base
from utils.logutil import logger
from utils.readmysql import RdTestcase
from utils.requestsutil import RequestSend

case_data = RdTestcase()

title = ''
environment = 'test1'
path = '/pro/v1/app/delete?lang=zh_CN'
request_body = '{"corpid": "", "userId": "", "platform": "web", "id": "1029"}'

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
