#!/usr/bin/env python3

try:
    import requests as r
    from requests.auth import HTTPBasicAuth
except ImportError:
    print('Requests module missing,please install Requests')
APIToken = '42dc8d249b95eb359e68ebd1390b2c81d6c2f347ab5351d49acb751ac16f4206'
BasicAuth = HTTPBasicAuth(APIToken, ' ')
APIURL = "https://api.digitalocean.com/v2"


class dopy():
    def __init__(self, APIToken):
        self.APIToken = APIToken

    def GetAccountDetails(self):
        ActInfo = r.get(APIURL + "/account", auth=BasicAuth)
        AccountDetail = ActInfo.json()
        return AccountDetail

    def GetDropletList(self):
        List = r.get(APIURL + "/droplets", auth=BasicAuth)
        DropletList = List.json()
        return DropletList

    def GetAccountActions(self):
        Actions = r.get(APIURL + "/actions", auth=BasicAuth)
        ActionList = Actions.json()
        return ActionList

    def ListAvailableImages(self):
        Images = r.get(APIURL + "/images?page=1&per_page=999&type=distribution", auth=BasicAuth)
        AvailableImages = Images.json()
        return AvailableImages

    def CreateDroplet(self):
        self.DropletParms = {"name": "example",
                             "region": "nyc3",
                             "size": "512mb",
                             "image": "centos-7-0-x64"}
        Create = r.post(APIURL + "/droplets", auth=BasicAuth, params=self.DropletParms)
        CreatedDroplet = Create.json()
        return CreatedDroplet
