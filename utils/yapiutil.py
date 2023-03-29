import json
import os.path
import requests as requests
import re
from utils.readmysql import RdTestcase


class Yapi:
    def __init__(self):
        self.url = 'http://yapi.xbongbong.com'
        self.token = '841a5e8fb8251976ba069eef55158a12213f715d9465eeb26ac0f1052bcce1a6'  # 项目token（记得改）
        self.interface_detail_filename = r'utils/data/interface_detail.json'
        self.sql = RdTestcase()
        self.sql.truncateTable(self.sql.case_table_name)
        self.id = 0

    # 替换数据
    def replace_data(self, init_data, expected_to_be_replace, need_replace_to_data):
        page_pattern = re.compile(expected_to_be_replace)
        matchers = page_pattern.findall(str(init_data))
        for matcher in matchers:
            init_data = str(init_data).replace(str(matcher), str(need_replace_to_data))
        return init_data

    # 获取菜单列表
    def get_cat_menu(self):
        url = self.url + '/api/interface/getCatMenu'
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        body = {
            'project_id': 735,  # 项目id
            'token': self.token
        }
        try:
            response = requests.get(url=url, params=body, headers=headers).json()
            # print(response)
            errcode = response['errcode']
            # 成功获取data
            if errcode == 0:
                data = response['data']
                # print(data)
                for i in range(len(data)):
                    cat_id = data[i]['_id']
                    name = data[i]['name']
                    uid = data[i]['uid']
                    # 打印项目信息
                    print(f'cat_id:{cat_id}\tuid:{uid}\t\tname:{name}')
                    self.get_interface_list_cat(cat_id)
                    self.update_database()
            # 返回数据错误
            else:
                print(errcode)
        except Exception as e:
            print(e)

    def get_interface_list_cat(self, catid):
        url = self.url + '/api/interface/list_cat'
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        body = {
            'catid': catid,  # 分组id
            'token': self.token,
            'page': 1,
            'limit': 50
        }
        interface_data_list = []
        try:
            response = requests.get(url=url, params=body, headers=headers).json()
            if response['errcode'] == 0:
                data = response['data']
                data_list = data['list']
                for i in range(len(data_list)):
                    interface_id = data_list[i]['_id']
                    data_dict = self.get_interface_detail(interface_id)
                    self.id = self.id + 1
                    data_dict['id'] = self.id
                    interface_data_list.append(data_dict)
            else:
                print(response['errcode'])
        except Exception as e:
            print(e)
        print(interface_data_list)
        self.save_data_list(interface_data_list)

    def get_interface_detail(self, interface_id):
        url = self.url + '/api/interface/get'
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        body = {
            'id': interface_id,  # 接口id
            'token': self.token
        }
        try:
            response = requests.get(url=url, params=body, headers=headers).json()
            if response['errcode'] == 0:
                data = response['data']
                method = str(data['method']).lower()
                title = data['title']
                path = data['path']
                req_body_other = eval(data['req_body_other'])
                relation = data['markdown']
                status = data['status']

                if status == 'done':
                    status = int(1)
                else:
                    status = int(0)

                interface_data_dict = {
                    'id': 0,
                    'title': title,
                    'method': method,
                    'path': path,
                    'req_body': req_body_other,
                    'relation': relation,
                    'isdel': status
                }
                return interface_data_dict
            else:
                print(response['errcode'])
        except Exception as e:
            print(e)

    def save_data_list(self, data_list):
        if not os.path.exists(self.interface_detail_filename):
            with open(self.interface_detail_filename, 'a', encoding='utf-8') as file:
                file.close()
        with open(self.interface_detail_filename, 'w', encoding='utf-8') as file:
            result = json.dumps(data_list, ensure_ascii=False)
            file.write(result)

    def update_database(self):
        with open(self.interface_detail_filename, 'r', encoding='utf-8') as file:
            case_str = file.read()
            case_str = case_str.replace("false", "False")
            case_list = eval(case_str)
            for i in range(len(case_list)):
                case_dict = case_list[i]
                id = case_dict['id']
                title = case_dict['title']
                method = case_dict['method']
                url = case_dict['path']
                request_body = str(case_dict['req_body']).replace("'", '"').replace('"None"', 'None').replace('"False"','False').replace('"True"', 'True')
                relation = case_dict['relation']
                isdel = case_dict['isdel']
                self.sql.update_case_from_yapi(id, title, url, method, request_body, relation, isdel)
            file.close()

    def updateDatabase(self):
        self.get_cat_menu()


if __name__ == '__main__':
    yapi = Yapi()
    yapi.updateDatabase()
