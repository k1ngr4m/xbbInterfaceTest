# coding=utf-8
import hashlib
import json
from string import Template
import re
from config.settings import token


# 生成请求头里的sign值
def create_sign_code(request_parameters, production_token):
    request_parameters = json.dumps(request_parameters)
    parameters = request_parameters + str(production_token)
    sign = hashlib.sha256(parameters.encode('utf-8')).hexdigest()
    return sign


def get_headers(data, headers):
    sign_code = create_sign_code(data, token)
    headers['sign'] = sign_code
    return headers


def find(data):
    # 判断data是否为字典
    if isinstance(data, dict):
        data = json.dumps(data)
        pattern = "\\${(.*?)}"
        ret = re.findall(pattern, data)
        return ret


# 进行参数替换
def replace(ori_data, replace_data):
    ori_data = json.dumps(ori_data)
    s = Template(ori_data)
    return s.safe_substitute(replace_data)


# 根据var，逐层获取json格式的值
def parse_relation(var, resdata):
    if not var:
        return resdata
    else:
        resdata = resdata.get(var[0])
        del var[0]
        return parse_relation(var, resdata)


if __name__ == '__main__':
    ori_data = {"admin-token": "${token}"}
    replace_data = {'token': 'k1ngr4m'}
    print(replace(ori_data, replace_data))
