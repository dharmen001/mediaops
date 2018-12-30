import pandas as pd

x = pd.read_excel('C:/Users/dharmendra.mishra/OneDrive - insidemedia.net/Reports/NDPdataDump/DMC_Static_Conversions.xlsx',
                error_bad_lines=False, converters={"Advertiser ID": str})
print(x)