from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from config import Config

class NdpGrdriveDate(Config):

    def __init__(self):
        super(NdpGrdriveDate, self).__init__()
        self.gauth = GoogleAuth()
        # self.gauth.LocalWebserverAuth()
        self.drive = GoogleDrive(self.gauth)

    def file_objects(self):
        # publisher file
        # print(file_obj["title"], file_obj["mimeType"])
        file_obj_publisher_file = self.drive.CreateFile({'id': self.section_value[15]})
        self.file_obj_publisher_file = file_obj_publisher_file
        print ('title: {}, id: {}'.format(self.file_obj_publisher_file['title'], self.file_obj_publisher_file['id']))
        print('downloading to {}'.format(self.file_obj_publisher_file))

        # Lead file(US/CA)
        file_obj_lead_file = self.drive.CreateFile({'id': self.section_value[16]})
        self.file_obj_lead_file = file_obj_lead_file
        print ('title: {}, id: {}'.format(self.file_obj_lead_file['title'], self.file_obj_lead_file['id']))
        print('downloading to {}'.format(self.file_obj_lead_file))


        #Uk Files
        file_list_uk = self.drive.ListFile({'q':"'1gzbtbqWyQEbJCfyRuYGsXKr4boOGdsrh' in parents"}).GetList()
        self.file_list_uk = file_list_uk


    def download_files(self):
        self.file_obj_publisher_file.GetContentFile(self.section_value[12] + 'Sage Global - Publisher Data - Daily.xlsx',
                                mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

        self.file_obj_lead_file.GetContentFile(self.section_value[12] + 'NDP - Sage NA Lead Gen - Content Synd Tracker.xlsx',
                                mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

    def download_uk_folder(self):
        for f in self.file_list_uk:
            print ('title: {}, id: {}'.format(f['title'], f['id']))
            fname = f['title']
            print('downloading to {}'.format(fname))
            f = self.drive.CreateFile({'id': f['id']})
            f.GetContentFile(self.section_value[14] + fname  + ".xlsx",
                             mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

    def main(self):
        self.file_objects()
        self.download_files()
        self.download_uk_folder()


if __name__ == "__main__":
    objectNdpGdrive = NdpGrdriveDate()
    objectNdpGdrive.main()