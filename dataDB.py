# code:utf-8
'''
@author: memect
@date: 16/04/2018
@mail： liukun@memect.co
@description: 将数据存储到数据库中
'''
import sqlite3
import json
from pypinyin import lazy_pinyin
from company_info_API import CompanyInfoAPI


class DBTable:
    def __init__(self, tname=''):
        self._tablename = tname

    @property
    def tablename(self):
        return self._tablename

    def get_table_sql(self, info_dict):
        key_name_list = get_info_key(info_dict)
        str_key_name_list = ' varchar(100) ,\n'.join(key_name_list)
        sql = """
                create table {0}(
                public_date varchar(100),
                {1} varchar(100)
                )
                """
        print(sql.format(self._tablename, str_key_name_list))
        return str_key_name_list

    def _check_companycode_period(self, company_code='000001', period='2017'):
        db_conn = get_conn()
        cursor = db_conn.cursor()
        sql = "select count(*) from {0} where company_code=? and period=?".format(self._tablename)
        cursor.execute(sql, (company_code, period))
        res = cursor.fetchone()
        existance = True
        if res[0] == 0:
            existance = False
        cursor.close()
        db_conn.close()
        return existance

    def get_companycode_period_list(self):
        db_conn = get_conn()
        cursor = db_conn.cursor()
        sql = "select distinct company_code,period from {0} order by company_code,period".format(self._tablename)
        cursor.execute(sql)
        code_period_list = [(row[0], row[1]) for row in cursor]
        cursor.close()
        db_conn.close()
        return code_period_list

    def get_data_list(self):
        db_conn = get_conn()
        cursor = db_conn.cursor()
        sql = "select * from {0} order by company_code,period".format(self._tablename)
        cursor.execute(sql)
        data_list = cursor.fetchall()
        title = [x[0] for x in cursor.description]
        cursor.close()
        db_conn.close()
        return title, data_list

    def _execute_insert_action(self, info_dict={}):
        db_conn = get_conn()
        cursor = db_conn.cursor()
        sorted_column_headers_list = []
        sorted_column_values_list = []
        for k, v in info_dict.items():
            sorted_column_headers_list.append(k.replace(":", "").replace("(", "_").replace(")", "_"))
            sorted_column_values_list.append(str(v))  # 防止v是数组或者其他格式。
        placeholders = ', '.join(['?'] * len(sorted_column_headers_list))
        columns = ', '.join(sorted_column_headers_list)
        insert_sql = "INSERT INTO %s ( %s ) VALUES ( %s ) " % (self._tablename, columns, placeholders)
        cursor.execute(insert_sql, sorted_column_values_list)
        cursor.close()
        db_conn.commit()
        db_conn.close()
        print(insert_sql)

    def _execute_update_action(self, info_dict={}):
        company_code = info_dict['company_code']
        period = info_dict['period']
        db_conn = get_conn()
        cursor = db_conn.cursor()
        sorted_column_headers_list = []
        sorted_column_values_list = []
        for k, v in info_dict.items():
            sorted_column_headers_list.append(k.replace(":", "").replace("(", "_").replace(")", "_") + "=?")
            sorted_column_values_list.append(str(v))  # 防止v是数组或者其他格式。
        placeholders = ', '.join(sorted_column_headers_list)
        update_sql = "update %s set %s where company_code=? and period=?" % (self._tablename, placeholders)
        sorted_column_values_list.extend([company_code, period])
        cursor.execute(update_sql, sorted_column_values_list)
        cursor.close()
        db_conn.commit()
        db_conn.close()
        print(update_sql)

    def insert_or_update_data_to_db(self, info_dict):
        company_code = info_dict['company_code']
        period = info_dict['period']
        existance = self._check_companycode_period(company_code=company_code,
                                                   period=period)
        if existance:
            self._execute_update_action(info_dict=info_dict)
        else:
            self._execute_insert_action(info_dict=info_dict)

def get_conn():
    return sqlite3.connect("companyinfo.db")

def get_info_key(json_dict):
    xx = [key.replace(":","").replace("(","_").replace(")","_") for key in json_dict.keys()]
    return sorted(xx, key=lambda v: ''.join(lazy_pinyin(v)))

def _json_to_dict(text):
    json_dict = json.loads(text)
    return json_dict

if __name__ == '__main__':
    # get_f10_companycode_period_list()
    # _check_companycode_period()
    # get_f10_info()
    balanceapi = CompanyInfoAPI(field="资产负债表", eng_name="balance_sheet_info")
    balancetable = DBTable(tname='balance_sheet_info_table')
    res, info_dict = balanceapi.get_company_info(company_code='000002', period='2017')
    balancetable.insert_or_update_data_to_db(info_dict)
    balancetable.get_table_sql(info_dict)

    # insert_or_update_data_to_f10(info_dict=info_dict)
    # create_cash_flows_statement_info_talbe()
    # create_income_statmenet_info_table()
