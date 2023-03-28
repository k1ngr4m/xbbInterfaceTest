import os

name = os.name


# 按间距中的绿色按钮以运行脚本。
def deal_dict(data):
    for k, v in data.items():
        if k == 'corpid':
            data['corpid'] = ''
        elif k == 'userId':
            data['userId'] = ''
        elif k == 'appId':
            data['appId'] = '${appId_name}'
        elif k == 'menuId':
            data['menuId'] = '${menuId_name}'
        elif k == 'formId':
            data['formId'] = '${formId_name}'
        if type(v) == dict:
            deal_dict(v)
        elif type(v) == list:
            for i in range(len(v)):
                print(v[i].items)
                deal_dict(v[i])
    return data


if __name__ == '__main__':
    # strs = '{"dataList":{"text_1":"这是当当","array_3":[{"addTime":1679971161,"appId":997,"businessType":0,"color":"#FF813D","corpid":"ding66041eb1c6df73f535c2f4657eb6378f","creatorId":"215252650523902241","del":0,"enable":0,"formId":10372,"groupId":1007,"id":1487,"name":"默认标签","sort":0,"updateTime":1679971161}],"amountDetail":null},"serialNo":"","isBatch":0}'
    # strs = strs.replace("true", "True").replace("false", "False").replace("null", "None")
    # data = eval(strs)
    # data = deal_dict(data)
    # data = str(data).replace("", '')
    # print(data)
    str = "{'corpid':'','userId':'','platform':'web','appId':'${appId_name}','menuId':'${menuId_name}','formId':'${formId_name}','saasMark':2,'distributorMark':0,'businessType':0,'subBusinessType':404,'dataId':None,'dataList':{'text_1':'这是当当','text_2':'这是多多','num_1':4869,'date_1':1679328000,'text_3':{'text':'选项值2','value':'b540f4af-f7de-a331-6774-bb6d1e8f295b','color':'#646566'},'array_1':[{'text':'选项值2','color':'#646566','value':'5b652755-369b-802b-74fa-a8b65b742b1f'},{'text':'选项值3','color':'#646566','value':'3a605b5f-6cf5-20e9-ee9b-6430d9e08610'}],'text_4':{'text':'选项值1','value':'85f4a914-00f6-7fc1-a325-2b063364806d','color':'#646566'},'array_2':[{'text':'选项值2','color':'#646566','value':'7f3a3e3c-a7fa-e092-a690-c42cefcd7b0a'},{'text':'选项值3','color':'#646566','value':'f1d3c1e4-8956-9607-e5cb-202e50e90dce'}],'address_1':{'city':'杭州市','address':'三墩镇紫荆花北路188号1幢','district':'西湖区','province':'浙江省','location':{'lon':120.093007,'lat':30.308184}},'geo_1':None,'file_1':['https://cdn3.xbongbong.com/xbbProTest/ding66041eb1c6df73f535c2f4657eb6378f/215252650523902241/jpg/167997337719724199fb06b762d0d93e67264386621d5.jpg?1679973377197'],'file_2':[{'filename':'Snipaste_2023-03-23_20-36-07.png','attachIndex':'https://cdn3.xbongbong.com/xbbProTest/ding66041eb1c6df73f535c2f4657eb6378f/215252650523902241/png/167997338600608838581c93aea5365e33b966dd685f2.png','uid':1679973385995,'ext':'png','size':65202,'successFlag':True,'showDelete':False,'uploadProgress':100,'uploadFileName':'xbbProTest/ding66041eb1c6df73f535c2f4657eb6378f/215252650523902241/png/167997338600608838581c93aea5365e33b966dd685f2.png'}],'text_5':None,'array_3':'${lableList_name}','amountDetail':None},'serialNo':'','isBatch':0}"
    data = eval(str)
    print(data)