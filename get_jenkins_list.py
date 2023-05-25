import json
import requests


# env_find = 'test3'
env_list = ['test1', 'test2', 'test3', 'test4', 'testsae']
url = 'http://192.168.10.203:8801/cdp/jenkins/build/list'
headers = {
    'Accept': 'application/json, text/plain, */*',
    'Content-Type': 'application/json;charset=UTF-8',
    'Accept-Language': 'zh-CN,zh,q=0.9',
    'Host': '192.168.10.203:8801',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'
}
data = {"condition": {"type": "", "loginUser": "false"}, "pageNum": 1, "pageSize": 1000}
res = requests.post(url=url, headers=headers, data=json.dumps(data))

if res.status_code == 200:
    res_data = res.json()
    dataList = res_data["result"]["dataList"]
    for env_find in env_list:
        isFind = False
        for i in range(len(dataList)):
            statusName = dataList[i]["statusName"]
            creatorName = dataList[i]["creatorName"]
            jenkinsJobName = dataList[i]["jenkinsJobName"]
            startTime = dataList[i]["startTime"]
            paramater = dataList[i]["paramater"]
            if statusName == '成功' and jenkinsJobName == 'PRO测试环境(构建入口)':
                for j in range(len(paramater)):
                    if 'test_server_choice' in str(paramater[j]):
                        env = paramater[j]['values'][0]
                        if env == env_find:
                            isFind = True
                            print("创建者:" + creatorName)
                            print("环境:" + env)
                            print("开始时间:" + startTime)
                    if isFind:
                        if 'pro_branch' in str(paramater[j]):
                            pro_branch = paramater[j]['values'][0]
                            print("后端分支:" + pro_branch)
                            print("~~~~~~~~")
                            break
                if isFind:
                    break
