# coding=utf-8

import tableauserverclient as TSC
import argparse
import requests
import pandas as pd
import csv


parser = argparse.ArgumentParser()
args = parser.parse_args()

tableau_auth = TSC.TableauAuth('simon.mccarthy@ogilvy.com', 'Alr3adyH0me', site_id='neoogilvy')
server = TSC.Server('https://10az.online.tableau.com')
server.auth.sign_in(tableau_auth)
server.version = '2.7'
print(server.version)
# print(server.projects.get())

with server.auth.sign_in(tableau_auth):
    all_workbooks, pagination_item = server.workbooks.get()
    print("\nThere are {} workbooks on site: ".format(pagination_item.total_available))
    print([workbook.name for workbook in all_workbooks])

    if all_workbooks:
        sample_workbook = all_workbooks[3]
        server.workbooks.populate_views(sample_workbook)
        print("\nName of views in {}: ".format(sample_workbook.name))
        sample_view = ([view.name for view in sample_workbook.views])
        print (sample_view[12])

        sample_view_id = [view.id for view in sample_workbook.views]
        print (sample_view_id[12])

        server.workbooks.populate_connections(sample_workbook)
        print("\nConnections for {}: ".format(sample_workbook.name))
        print(["{0}({1})".format(connection.id, connection.datasource_name)
               for connection in sample_workbook.connections])

        view_id = '6144dcb6-8041-46f3-83b9-ba7e94f3267d'
        server_url = 'https://10az.online.tableau.com'
        src_url = "https://10az.online.tableau.com/#/site/neoogilvy/views/SageGlobal2018DataAudit/" \
                  "AccountAdvertisersList.csv"

        src_url_new = "/views/SageGlobal2018DataAudit/AccountAdvertisersList.csv"

        r = requests.get(src_url_new)
        with open('acc.csv', 'wb') as f:
            f.write(r.content)












