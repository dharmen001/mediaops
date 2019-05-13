import os
import pandas as pd
from Classes.DataReaders.config_ini import Config


class RemoveSelectedFiles(Config):
    def __init__(self):
        super(RemoveSelectedFiles, self).__init__()
        self.path = None

    def file_manipulators(self):

        path = self.section_value[37]
        flist = pd.read_csv(self.section_value[34] + 'file_name.csv')

        file_name = flist['fileName'].tolist()
        file_id_name = flist['idName'].tolist()
        print(file_name)

        # for i, j in zip(file_name, file_id_name):
        for filename in os.listdir(path):
            if filename not in file_name:
                os.remove(path + filename)
            # if i in filename:
                #     os.rename("{}/{}".format(path, filename), "{}/{}".format(path, j))

        for i, j in zip(file_name, file_id_name):
            for filename in os.listdir(path):
                print(filename)
                if i in filename:
                    print("{}{}".format(path, j))
                    print("{}".format(filename))
                    os.rename("{}/{}".format(path, filename), "{}/{}".format(path, j))


if __name__ == "__main__":
    RemoveFiles = RemoveSelectedFiles()
    RemoveFiles.file_manipulators()


