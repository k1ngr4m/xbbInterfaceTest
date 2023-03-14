import os

name = os.name


# 按间距中的绿色按钮以运行脚本。
def deal_dict(data):
    for k, v in data.items():
        if k == 'corpid':
            data['corpid'] = '1'
        elif k == 'userId':
            data['userId'] = '1'
        elif k == 'appId':
            data['appId'] = '${appId_name}'
        elif k == 'menuId':
            data['menuId'] = '${menuId_name}'
        elif k == 'formId':
            data['formId'] = '${formId_name}'
        if type(v) == dict:
            deal_dict(v)
        return data


if __name__ == '__main__':
    strs = '{"corpid":"123","data":{"corpid":"123","appId":"123"}}'
    data = eval(strs)
    data = deal_dict(data)
    data = str(data).replace("", '')
    print(data)
