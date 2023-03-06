# coding=utf-8
import datetime
import json
from utils.mysqlutil import MysqlUtil
from utils.logutil import logger

mysql = MysqlUtil()


class RdTestcase:
    # 加载所有测试用例
    def load_all_case(self, web):
        sql = f"select * from 'test_case_list' where web = '{web}'"
        results = mysql.get_fetchall(sql)
        return results

    # 筛选可执行的用例
    def is_run_data(self, web):
        run_list = [case for case in self.load_all_case(web) if case['isdel'] == 1]
        return run_list

    # 获取配置信息
    def loadConfkey(self, web, key):
        sql = f"select * from 'test_config' where web='{web}' and 'key'='{key}'"
        results = mysql.get_fetchone(sql)
        return results

    # 更新测试结果
    def updateResults(self, response, is_pass, case_id):
        current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        sql = f"insert into test_result_record (case_id,times,response,result) values ('{case_id}','{current_time}','{json.dumps(response, ensure_ascii=False)}','{is_pass}')"
        rows = mysql.sql_execute(sql)
        logger.debug(sql)
        return rows


if __name__ == '__main__':
    test = RdTestcase()
    res = test.updateResults({
        'code': 200,
        'body': {'error': 1,
                 'message': '用户名和密码不能为空'},
        'cookies': {}},
        'True', '4565'
    )
    print(res)
