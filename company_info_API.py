# code:utf-8
'''
@author: memect
@date: 16/04/2018
@mail： liukun@memect.co
@description: 获取上市公司:基本信息，利润表，资产负债表，现金流量表 python3示例代码
'''

import requests
import json
import config

HEADERS = config.HEADERS#{'Authorization': APPCODE, }



class CompanyInfoAPI:
    def __init__(self, field,eng_name):
        """field in ["资产负债表","现金流量表","基本信息","利润表"]
        eng_name in ["balance_sheet_info","cash_flows_statement_info","f10_info","income_statmenet_info"]
        """
        self.field = field
        self.eng_name=eng_name

    def _get_info(self,url, query_dict={"field": "基本信息", "period": '2017'}):
        """获取公司信息程序"""
        response = requests.request("GET", url, headers=HEADERS, params=query_dict)
        print(response.status_code)
        return response.status_code, response.text

    def get_company_info(self, company_code, period):
        URL = 'http://memect0006.market.alicloudapi.com/company/' + company_code
        querystring = {"field": self.field, "period": period}
        status_code, res_text = self._get_info(url=URL, query_dict=querystring)
        if status_code != 200:
            return False, None
        json_dict = json.loads(res_text)
        json_dict['company_code'] = company_code
        json_dict['period'] = period
        return True, json_dict

    def get_company_code_list_info(self,period):
        """根据period和field筛选符合条件的公司股票代码list。
        period in [2015,2016,2017Q3,2017]
        """
        URL = 'http://memect0006.market.alicloudapi.com/companys/codelist'
        querystring = {"field": self.field, "period": period}
        status_code, res_text = self._get_info(url=URL, query_dict=querystring)
        if status_code != 200:
            print(res_text)
            return False, None
        js_list = json.loads(res_text)
        return True,js_list
        pass

if __name__ == '__main__':
    cash_api=CompanyInfoAPI(field="现金流量表",eng_name='cash_flows_statement_info')
    res, text = cash_api.get_company_code_list_info(period="2017")
    print(res, text)
    res, text = cash_api.get_company_info(company_code='000001',period="2017")
    print(res, text)
    # get_income_statmenet_info(company_code="000001",period="2016")
    # get_balance_sheet_info(company_code="000005",period="2015")
    # get_cash_flows_statement_info(company_code="600000",period="2015")
