import pandas as pd
from pyxlsb import open_workbook as open_xlsb

df = []

with open_xlsb('C:/Users/dharmendra.mishra/OneDrive - insidemedia.net/Reports/NDPdataDump/GR data1.xlsb') as wb:
    with wb.get_sheet('export(1)') as sheet:
        for row in sheet.rows():
            df.append([item.v for item in row])

df = pd.DataFrame(df[1:], columns=df[0])
print (df)