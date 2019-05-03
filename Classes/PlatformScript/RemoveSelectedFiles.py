import os
import pandas as pd

path = "C:/Users/dharmendra.mishra/OneDrive - insidemedia.net/Reports/Adwords/"

flist = pd.read_csv('C:/mediaops/mapping/adword/file_name.csv')

file_name = flist['fileName'].tolist()

for filename in os.listdir(path):
    print(filename)
    if filename not in file_name:
        os.remove(path + filename)


