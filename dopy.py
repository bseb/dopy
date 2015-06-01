#!/usr/bin/env python3

import json
try:
    import requests as r
    from requests.auth import HTTPBasicAuth
except ImportError:
    print('Requests module missing,please install Requests')


class Dopy():
    APIURL = "https://api.digitalocean.com/v2"
    jsonheaders = {'content-type': 'application/json'}

    def __init__(self, APIToken):
        self.APIToken = APIToken
        self.BasicAuth = HTTPBasicAuth(APIToken, ' ')

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
        Images = r.get(self.APIURL + "/images?page=1&per_page=999&" +
                       "type=distribution", auth=self.BasicAuth)
        AvailableImages = Images.json()
        return AvailableImages

    def CreateDroplet(self, name="example", region="nyc3", size="512mb",
                      image="centos-7-0-x64", **kwargs):
        DropParms = {"name": name, "region": region, "size": size,
                     "image": image}
        DropParms.update(kwargs)
        Create = r.post(self.APIURL + "/droplets", auth=self.BasicAuth,
                        headers=self.jsonheaders,
                        data=json.dumps(DropParms))
        CreatedDroplet = Create.json()
        return CreatedDroplet

    def GetDropletInfo(self, id):
        Info = r.get(self.APIURL + "/droplets/" + id, auth=self.BasicAuth)
        DropletInfo = Info.json()
        return DropletInfo

    def GetDropletActions(self, id):
        Actions = r.get(self.APIURL + "/droplets/" + id + "/actions",
                        auth=self.BasicAuth)
        DropletActions = Actions.json()
        return DropletActions

    def ListDropletSnapshots(self, id):
        Snapshots = r.get(self.APIURL + "/droplets/" + id + "/snapshots",
                          auth=self.BasicAuth)
        DropletSnapshots = Snapshots.json()
        return DropletSnapshots

    def ListDropletBackups(self, id):
        Backups = r.get(self.APIURL + "/droplets/" + id + "/Backups",
                        auth=self.BasicAuth)
        DropletBackups = Backups.json()
        return DropletBackups

    def DestroyDroplet(self, id):
        Delete = r.delete(self.APIURL + "/droplets/" + id, auth=self.BasicAuth)
        return Delete

    def ListDropletUpgrade(self):
        Upgrade = r.get(self.APIURL + "/droplet_upgrades", auth=self.BasicAuth)
        DropletUpgrades = Upgrade.json()
        return DropletUpgrades

    def DropletPowerControl(self, id, action):
        ValidActions = ["power_cycle", "shutdown", "power_off", "power_on",
                        "reboot"]
        if action not in ValidActions:
            raise DopyError("%s is not a valid action" % action)
        command = {"type": action}
        Dpower = r.post(self.APIURL + "/droplets/" + id + "/actions",
                        params=command, auth=self.BasicAuth)
        DropPower = Dpower.json()
        return DropPower
    # Valid values of action are "power_cycle" "shutdown" "power_off" "power_on"

    def ListKeys(self):
        Keys = r.get(self.APIURL + "/account/keys", auth=self.BasicAuth)
        KeyList = Keys.json()
        return KeyList


class DopyError(Exception):
    pass
