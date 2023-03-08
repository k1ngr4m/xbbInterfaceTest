# coding=utf-8
import datetime
import json

import pytest
import commom.base as Base
from commom import base
from config.settings import DynamicParam
from utils.logutil import logger
from utils.readmysql import RdTestcase
from utils.requestsutil import RequestSend

attribute = DynamicParam()
case_data = RdTestcase()
case_list = case_data.is_run_data('xbb')
current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')


class TestApi:
    def setup_class(self):
        logger.info(f"***** 开始执行测试用例，开始时间为：{current_time} *****")

    def teardown_class(self):
        logger.info(f"***** 执行测试用例完成，完成时间为：{current_time} *****")

    @pytest.mark.parametrize('case', case_list)
    def test_run(self, case):
        res_data = None
        conf_key = case_data.loadConfkey('xbb', 'test1')
        url = conf_key['value'] + case['url']
        headers = eval(conf_key['headers'])
        method = case['method']
        cookies = eval(case['cookies'])
        data = eval(case['request_body'])
        relation = str(case['relation'])
        case_name = case['title']

        # 根据关联获取参数中是否有变量需要被替换
        cookies = self.correlation(cookies)
        data = base.get_data(data)
        data = self.correlation(data)
        headers = base.get_headers(data, headers)
        headers = self.correlation(headers)

        try:
            logger.info("正在执行{}用例".format(case_name))
            res_data = RequestSend().send(url, method, data=data, headers=headers, cookies=cookies)
            logger.info("用例执行成功，请求的结果为{}".format(res_data))
        except:
            logger.info("用例执行失败，请查看日志。")
            assert False

        # 判断res_data是否存在
        if res_data:
            # 判断relation不为空
            if relation != "None":
                # 设置token的值为响应结果的信息
                self.set_relation(relation, res_data)
        self.assert_response(case, res_data)
        return res_data

    # 响应结果关联设置函数
    def set_relation(self, relation, res_data):
        try:
            if relation:
                relation = relation.split(",")
                for i in relation:
                    var = i.split("=")
                    var_name = var[0]
                    var_tmp = var[1].split(".")
                    res = Base.parse_relation(var_tmp, res_data)
                    print(f"{var_name}={res}")
                    setattr(DynamicParam, var_name, res)
        except Exception as e:
            print(e)

    # 根据关联，获取该变量内容
    def correlation(self, data):
        res_data = Base.find(data)
        if res_data:
            replace_dict = {}
            for i in res_data:
                data_temp = getattr(DynamicParam, str(i), "None")
                replace_dict.update({str(i): data_temp})
            data = json.loads(Base.replace(data, replace_dict))
        return data

    def assert_response(self, case, res_data):
        is_pass = False
        try:
            assert int(res_data['body']['code']) == int(case['expected_code'])
            logger.info("用例断言成功")
            is_pass = True
        except Exception as e:
            is_pass = False
            print(e)
            logger.info("用例断言失败")
        finally:
            case_data.updateResults(res_data, is_pass, str(case['id']))
            assert is_pass
        return is_pass


if __name__ == '__main__':
    pytest.main(['-s', '-v', 'test_run.py'])
