# !/usr/bin/python
# coding=utf-8


from config_ini import Config
import pandas as pd
import pymysql


class SqlClass(Config):

    def __init__(self):
        super(SqlClass, self).__init__()

        # connect to my sql using pymysql connector
        conn = pymysql.connect(host='{}'.format(self.section_value[30]), user='root', password='Welcome2020.', db='tableau')
        create_table = open('C:/mediaops/SQL/CreatetableAdwords.sql')
        tableau_table = create_table.read()
        x = pd.read_sql(tableau_table, conn)
        print(x)


if __name__ == "__main__":
    mysql_client = SqlClass()