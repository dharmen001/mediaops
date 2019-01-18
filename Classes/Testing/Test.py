import pandas as pd

df = pd.DataFrame()
xlfname = 'C:/Users/dharmendra.mishra/OneDrive - insidemedia.net/Reports/outputuklist/MasterSheet.xlsx'
xl = pd.ExcelFile(xlfname)

for sheet in xl.sheet_names:
    df_tmp = xl.parse(sheet)
    df = df.append(df_tmp, ignore_index=True)

print(len(df))

csvfile = 'sample.csv'
df.to_csv(csvfile, index=False)