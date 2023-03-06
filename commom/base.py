# coding=utf-8
import json
from string import Template
import re


def find(data):
    # 判断data是否为字典
    if isinstance(data, dict):
        data = json.dumps(data)
        pattern = "\\${(.*)}"
        return re.findall(pattern, data)


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
