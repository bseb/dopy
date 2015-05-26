#!/usr/bin/env python3

try:
    import requests as r
    from requests.auth import HTTPBasicAuth
except ImportError:
    print('Requests module missing,please install Requests')


class dopy():
    APIURL = "https://api.digitalocean.com/v2"

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
        Images = r.get(self.APIURL + "/images?page=1&per_page=999&type=distribution",
                       auth=self.BasicAuth)
        AvailableImages = Images.json()
        return AvailableImages

    def CreateDroplet(self, name="example", region="nyc3", size="512mb",
                      image="centos-7-0-x64", **kwargs):
        DropParms = {"name": name, "region": region, "size": size, "image": image}
        DropParms.update(kwargs)
        Create = r.post(self.APIURL + "/droplets", auth=self.BasicAuth,
                        params=DropParms)
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
    # TODO Handle Return Codes 204 is success, 404 droplet not found

    def ListDropletUpgrade(self):
        Upgrade = r.get(self.APIURL + "/droplet_upgrades", auth=self.BasicAuth)
        DropletUpgrades = Upgrade.json()
        return DropletUpgrades

    def RebootDroplet(self, id):
        command = {"type": "reboot"}
        Reboot = r.post(self.APIURL + "/droplets/" + id + "/actions", params=command,
                        auth=self.BasicAuth)
        DropletReboot = Reboot.json()
        return DropletReboot

    def DropletPowerControl(self, id, action):
        command = {"type": action}
        Dpower = r.post(self.APIURL + "/droplets/" + id + "/actions", params=command,
                        auth=self.BasicAuth)
        DropPower = Dpower.json()
        return DropPower
    # Valid values for action are "power_cycle" "shutdown" "power_off" "power_on"

