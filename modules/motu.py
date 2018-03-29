"""
This program will allow interaction with the motu
"""
import argparse
import json
import requests


class Motu:

    def __init__(self, ipAddr=None, port=80):
        self.ipAddr = ipAddr
        self.port = port 
        self.url = "http://{}:{}".format(ipAddr,port)
       
        self.uid = self._getUid()
        self.settings = self._getSettings()

        print("== Motu AVB: ==")
        print("Settings: {}".format(self.settings if self.settings else "No Motu soundcard found"))


    def _query(self, address, value):
        """
        Send the corresponding  message
        - address is a string
        - value is an array
        Return True if well received by the motu soundcard
        """
        value = json.dumps(value)
        url = "{}/datastore{}".format(self.url, address)
        r = requests.post(url, {"json":value})
        
        return True if r.status_code is 200 else False


    def _get(self, address):
        """
        Get the value at a given endPoint
        """
        url = "{}/datastore{}".format(self.url, address)
        r = requests.get(url)
        return r.json() if r.status_code is 200 else False

    
    def _getUid(self):
        """
        Get the uid of the motu soundCard
        """
        uidJson = self._get("/uid")
        return uidJson.value if uidJson else False


    def _getSettings(self):
        """
        Get the settings of the motu soundCard
        """
        return self._get("avb/{}/".format(self.uid))


    ###################################################
    def setSolo(self, ch, solo):
        """
        Solo a given channel
        """
        address = "/mix/chan/{}/matrix/solo".format(ch)
        values = { "value": 1 if solo else 0}
        return self._query(address, values)

    
    def getSolo(self, ch):
        """
        Get Solo status of a given channel
        """
        address = "/mix/chan/{}/matrix/solo".format(ch)
        return self._get(address)

 
    ###################################################
    def setMute(self, ch, mute):
        """
        Mute a given channel
        """
        address = "/mix/chan/{}/matrix/mute".format(ch)
        values = { "value": 1 if mute else 0}
        return self._query(address, values)


    def getMute(self, ch):
        """
        Get Mute status of a given channel
        """
        address = "/mix/chan/{}/matrix/mute".format(ch)
        return self._get(address)


    ###################################################
    def setGain(self, ch, gain):
        """
        Set gain of a given channel
        """
        address = "/mix/chan/{}/matrix/???".format(ch)
        values = { "value": gain}
        print("TODO: set Gain")
        #return self._query(address, values)
 
 
    def getGain(self, ch):
        """
        Get gain of a given channel
        """
        address = "/mix/chan/{}/matrix/???".format(ch)
        print("TODO: get Gain")
        #return self._query(address, values)
 

    ###################################################
    def setPan(self, ch, pan):
        """
        Set Pan of a given channel 
        > from -1 to 1
        """
        if -1 <= pan <= 1:
            address = "/mix/chan/{}/matrix/pan".format(ch)
            values = { "value": pan}
            return self._query(address, values)
        else:
            return False
    

    def getPan(self, ch):
        """
        Get Pan of a given channel 
        > from -1 to 1
        """
        address = "/mix/chan/{}/matrix/pan".format(ch)
        return self._get(address)
    

    ###################################################
    def setEq(self, ch, eq):
        """
        Big stuff to do here
        """
        print("TODO set EQ")

        eq = {
            "hpf":{
                "enabled": True,
                "freq": 40
            },
            "lowShelf":{
                "enabled": True,
                "freq": 80,
                "gain": 0,
                "bw": 1,
                "mode": 0
            },
            "mid1":{
                "enabled": True,
                "freq": 800,
                "gain": 0,
                "bw": 1,
            },
            "mid2":{
                "enabled": True,
                "freq": 10000,
                "gain": 0,
                "bw": 1,
            },
            "highShelf":{
                "enabled": True,
                "freq": 18000,
                "gain": 0,
                "bw": 1,
                "mode": 0
            }
        }

    def getEq(self, ch):
        """
        Get eq Object of the given chan
        """
        address = "/mix/chan/{}/eq".format(ch)
        return self._get(address)


    ###################################################
    def setComp(self, ch):
        print("TODO set Comp")


    def getComp(self, ch):
        print("TODO set Comp")


    ###################################################
    def muteMain(self, mute):
        """
        Mute main outputs
        """
        address = "/mix/main/{}/matrix/mute".format(1)
        values = { "value": 1 if mute else 0}
        return self._query(address, values)


    def muteMonitor(self, mute):
        """
        Mute monitor outputs
        """
        address = "/mix/monitor/{}/matrix/mute".format(1)
        values = { "value": 1 if mute else 0}
        return self._query(address, values)






