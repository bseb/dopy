#!/usr/bin/env python3

import json
try:
    import requests as r
    from requests.auth import HTTPBasicAuth
except ImportError:
    print('Requests module missing,please install Requests')


class Dopy():
    """ Takes 1 argument, Digital Ocean API Key. This creates a dopy object
    that allows you to interact with your digital ocean account.All output is
    returned in json. Full API documentation can be found at
    https://developers.digitalocean.com/documentation/v2/ """

    APIURL = "https://api.digitalocean.com/v2"
    jsonheaders = {'content-type': 'application/json'}

    def __init__(self, APIToken):
        self.APIToken = APIToken
        self.BasicAuth = HTTPBasicAuth(APIToken, ' ')

    def GetAccountDetails(self):
        """returns account info"""
        ActInfo = r.get(self.APIURL + "/account", auth=self.BasicAuth)
        AccountDetail = ActInfo.json()
        return AccountDetail

    def GetDropletList(self):
        """returns all droplets associated with account"""
        List = r.get(self.APIURL + "/droplets", auth=self.BasicAuth)
        DropletList = List.json()
        return DropletList

    def GetAccountActions(self):
        """returns recent actions performed"""
        Actions = r.get(self.APIURL + "/actions", auth=self.BasicAuth)
        ActionList = Actions.json()
        return ActionList

    def ListAvailableImages(self):
        """returns available droplet images"""
        Images = r.get(self.APIURL + "/images?page=1&per_page=999&" +
                       "type=distribution", auth=self.BasicAuth)
        AvailableImages = Images.json()
        return AvailableImages

    def ListAvailableSizes(self):
        """returns available droplet sizes"""
        Sizes = r.get(self.APIURL + "/sizes", auth=self.BasicAuth)
        AvailableSizes = Sizes.json()
        return AvailableSizes

    def ListAvailableRegions(self):
        """returns regions (datacenters) available for droplet creation"""
        Regions = r.get(self.APIURL + "/regions", auth=self.BasicAuth)
        AvailableRegions = Regions.json()
        return AvailableRegions

    def CreateDroplet(self, name="example", region="nyc3", size="512mb",
                      image="centos-7-0-x64", **kwargs):
        """Creates a new droplet. Required parameters are required arguments for
        droplet creation. There are more options available,a full listing can
        be found at
        https://developers.digitalocean.com/documentation/v2/#droplets"""
        DropParms = {"name": name, "region": region, "size": size,
                     "image": image}
        DropParms.update(kwargs)
        Create = r.post(self.APIURL + "/droplets", auth=self.BasicAuth,
                        headers=self.jsonheaders,
                        data=json.dumps(DropParms))
        CreatedDroplet = Create.json()
        return CreatedDroplet

    def GetDropletInfo(self, id):
        """returns info on a single droplet, requires droplet ID number"""
        Info = r.get(self.APIURL + "/droplets/" + id, auth=self.BasicAuth)
        DropletInfo = Info.json()
        return DropletInfo

    def GetDropletActions(self, id):
        """returns recent actions on a droplet, requrires droplet ID number"""
        Actions = r.get(self.APIURL + "/droplets/" + id + "/actions",
                        auth=self.BasicAuth)
        DropletActions = Actions.json()
        return DropletActions

    def ListDropletSnapshots(self, id):
        """returns  snapshots available for a droplet, requrires droplet ID"""
        Snapshots = r.get(self.APIURL + "/droplets/" + id + "/snapshots",
                          auth=self.BasicAuth)
        DropletSnapshots = Snapshots.json()
        return DropletSnapshots

    def ListDropletBackups(self, id):
        """returns backups stored for droplet, requires droplet ID"""
        Backups = r.get(self.APIURL + "/droplets/" + id + "/Backups",
                        auth=self.BasicAuth)
        DropletBackups = Backups.json()
        return DropletBackups

    def DestroyDroplet(self, id):
        """destroys droplet, requires droplet ID. USE WITH CAUTION"""
        Delete = r.delete(self.APIURL + "/droplets/" + id, auth=self.BasicAuth)
        return Delete

    def ListDropletUpgrade(self):
        """ lists available upgrades for a droplet, requires droplet ID """
        Upgrade = r.get(self.APIURL + "/droplet_upgrades", auth=self.BasicAuth)
        DropletUpgrades = Upgrade.json()
        return DropletUpgrades

    def DropletPowerControl(self, id, action):
        """Controls the virtual power to a droplet, requires a droplet id and
        action.Valid actions are power_cycle shutdown power_off power_on"""
        ValidActions = ["power_cycle", "shutdown", "power_off", "power_on",
                        "reboot"]
        if action not in ValidActions:
            raise DopyError("%s is not a valid action" % action)
        command = {"type": action}
        Dpower = r.post(self.APIURL + "/droplets/" + id + "/actions",
                        params=command, auth=self.BasicAuth)
        DropPower = Dpower.json()
        return DropPower

    def ListKeys(self):
        """returns SSH keys associated with account"""
        Keys = r.get(self.APIURL + "/account/keys", auth=self.BasicAuth)
        KeyList = Keys.json()
        return KeyList

    def AddKeys(self, name, key):
        """This function adds an SSH key, arguments are a user chosen name for
        the key and the public key string"""
        KeyInfo = {"name": name, "public_key": key}
        AddKey = r.post(self.APIURL + "account/keys", auth=self.BasicAuth,
                        headers=self.jsonheaders,
                        data=json.dumps(KeyInfo))
        AddedKey = AddKey.json()
        return AddedKey

    def GetKeyInfo(self, keyid):
        """returns info on an SSH key associated with account, requires key ID
        number"""
        Key = r.get(self.APIURL + "/account/keys/" + keyid, auth=self.BasicAuth)
        KeyInfo = Key.json()
        return KeyInfo

    def RenameKey(self, keyid, name):
        """changes the name of an SSH key on the account. requires key ID number
        and a new name for the key"""
        NewName = {"name": name}
        Rename = r.put(self.APIURL + "/account/keys/" + keyid,
                       auth=self.BasicAuth,
                       headers=self.jsonheaders,
                       data=json.dumps(NewName))
        RenamedKey = Rename.json()
        return RenamedKey

    def DeleteKey(self, keyid):
        """deletes an SSH key from the account, requires a key ID number"""
        Delete = r.delete(self.APIURL + "/account/keys/" + keyid,
                          auth=self.BasicAuth)
        DeletedKey = Delete.json()
        return DeletedKey


class DopyError(Exception):
    """Custom exception class"""
    pass
