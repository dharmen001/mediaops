from suds.client import Client


class Auth:
    '''
    classdocs
    '''

    def __init__(self, username, password, appkey, url):
        self.username = username
        self.password = password
        self.appkey = appkey
        self.url = url

        client = Client(url, faults=False)
        response = client.service.ClientLogin(username, password, appkey)

        self.code = response[0]
        if response[0] == 200:
            self.token = response[1]
        else:
            self.token = None

    def getStatus(self):
        return self.code


if __name__ == "__main__":
    obj = Auth('Kshitij.Bhati_IBMGlobal', 'Adops@18', 'abc', 'https://adapi.uat.sizmek.com/sas/login/login')
    print(obj.getStatus())