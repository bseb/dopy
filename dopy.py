#!/usr/bin/env python3

try:
    import requests as r
    from requests.auth import HTTPBasicAuth
except ImportError:
    print('Requests module missing,please install Requests')


class dopy():
    BasicAuth = HTTPBasicAuth(APIToken, ' ')
    APIURL = "https://api.digitalocean.com/v2"

    def __init__(self, APIToken):
        self.APIToken = APIToken

    def GetAccountDetails(self):
        ActInfo = r.get(self.APIURL + "/account", auth=self.BasicAuth)
        AccountDetail = ActInfo.json()
        return AccountDetail

    def GetDropletList(self):
        List = r.get(self.APIURL + "/droplets", auth=self.BasicAuth)
        DropletList = List.json()
        return DropletList

    def GetAccountActions(self):
        Actions = r.get(self.APIURL + "/actions", auth=self.BasicAuth)
        ActionList = Actions.json()
        return ActionList

    def ListAvailableImages(self):
        Images = r.get(self.APIURL + "/images?page=1&per_page=999&type=distribution", auth=self.BasicAuth)
        AvailableImages = Images.json()
        return AvailableImages

    def CreateDroplet(self, name="example", region="nyc3", size="512mb",
                      image="centos-7-0-x64", **kwargs):
        parms = {"name": name, "region": region, "size": size, "image": image}
        parms.update(kwargs)
        Create = r.post(self.APIURL + "/droplets", auth=self.BasicAuth,
                        parms=self.DropletParms)
        CreatedDroplet = Create.json()
        return CreatedDroplet
