import pandas as pd
import zipfile

path = "C:/Users/dharmendra.mishra/OneDrive - insidemedia.net/Reports/ndpoutput/"
writer_file = pd.ExcelWriter(path + "file.xlsx", engine="xlsxwriter", datetime_format="YYYY-MM-DD")
read_advertiser_mapping = pd.read_csv("C:/mediaops/mapping/ndpdata/advertiserMarketMapping.csv",
                                      encoding="utf-8")

print(read_advertiser_mapping.shape)

# x = read_advertiser_mapping.to_excel(writer_file)
# writer_file.save()
# writer_file.close()
# exit()

read_dmc_static_zf = zipfile.ZipFile("C:/Users/dharmendra.mishra/OneDrive - insidemedia.net/"
                                     "Reports/NDPdataDump/DMC_Static_Conversions.zip")
read_dmc_static = pd.read_csv(read_dmc_static_zf.open(zipfile.ZipFile.namelist(read_dmc_static_zf)[0]),
                              skiprows=9, skipfooter=1, engine='python', encoding="utf-8")

print(read_dmc_static.shape)

# x = read_dmc_static.to_excel(writer_file)
# writer_file.save()
# writer_file.close()
# exit()

merge_df = pd.merge(read_dmc_static, read_advertiser_mapping, on='Advertiser ID')
print(merge_df.shape)

# x = merge_df.to_excel(writer_file)
# writer_file.save()
# writer_file.close()