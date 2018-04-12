"""
This program will allow interaction with the motu
"""
import json
import requests
import time
import sys

from modules.midiHelper import *
from modules.settings import Settings

fader_api_range = [0, 4]
fader_midi_range = [-8192, 8192]

class Motu:

    def __init__(self, ipAddr=None, port=80):
        self.ipAddr = ipAddr
        self.port = port 
        self.url = "http://{}:{}".format(ipAddr, port)
       
        self.uid = self._getUid()
        self.waitOnline()

        self.motuSettings = self._getSettings()
        self.settings = Settings()


        if self.motuSettings:
            print("========== Motu AVB: ===========")
            print("* Name        : {}".format(self.motuSettings["hostname"]))
            print("* uid         : {}".format(self.uid))
            print("* Sample rate : {}".format(self.motuSettings["cfg/0/current_sampling_rate"]))
            print("================================")

    def _query(self, address, value):
        """
        Send the corresponding  message
        - address is a string
        - value is an array
        Return True if well received by the motu soundcard
        """
        value = json.dumps(value)
        url = "{}/datastore{}".format(self.url, address)
        r = requests.post(url, {"json": value})
        print("{} : {}".format(url, value))

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
        return uidJson["value"] if uidJson else False

    def _getSettings(self):
        """
        Get the settings of the motu soundCard
        """
        settings = self._get("/avb/{}/".format(self.uid))
        return settings

    def isOnline(self):
        return self._getUid()

    def waitOnline(self, timeout=10):
        cpt = 0
        while not self.isOnline():
            cpt = cpt + 1
            message = "Motu not online or unreachable, trying again ({})".format(cpt)
            sys.stdout.write("\r\x1b[K" + message.__str__())
            sys.stdout.flush()
            time.sleep(1)
            if cpt == timeout:
                print("\n Please verify that the soundCard is reachable on the network at {}".format(self.url))
                quit(404)

    ###################################################
    def setSolo(self, ch, solo):
        """
        Solo a given channel
        """
        address = "/mix/chan/{}/matrix/solo".format(ch)
        values = {"value": 1 if solo else 0}
        return self._query(address, values)

    def getSolo(self, ch):
        """
        Get Solo status of a given channel
        """
        address = "/mix/chan/{}/matrix/solo".format(ch)
        solo = self._get(address)
        return bool(solo["value"])

    def clearSolo(self):
        """
        Remove all solo status of the strips
        :return:
       """
        for ch in range(0, self.settings.getStripCount()):
            self.setSolo(ch, False)

    ###################################################
    def setMute(self, ch, mute):
        """
        Mute a given channel
        """
        address = "/mix/chan/{}/matrix/mute".format(ch)
        values = {"value": 1 if mute else 0}
        return self._query(address, values)

    def getMute(self, ch):
        """
        Get Mute status of a given channel
        """
        address = "/mix/chan/{}/matrix/mute".format(ch)
        mute = self._get(address)
        return bool(mute["value"])

    def muteAll(self, mute):
        """
        Mute / Unmute all strips
        :param mute: true to mute all, false otherwise
        :return:
        """
        for ch in range(0, self.settings.getStripCount()):
            self.setMute(ch, mute)

    ###################################################
    def setGain(self, ch, gain):
        """
        Set gain of a given channel
        """
        address = "/mix/chan/{}/matrix/???".format(ch)
        values = {"value": gain}
        print("TODO: set Gain")
        # return self._query(address, values)

    def getGain(self, ch):
        """
        Get gain of a given channel
        """
        address = "/mix/chan/{}/matrix/???".format(ch)
        print("TODO: get Gain")
        # return self._query(address, values)

    ###################################################
    def setFader(self, ch, fader):
        """
        Set fader of a given channel
        """
        address = "/mix/chan/{}/matrix/fader".format(ch)
        values = { "value": fader}
        return self._query(address, values)

    def getFader(self, ch, datatype="api"):
        """
        Get fader of a given channel
        """
        address = "/mix/chan/{}/matrix/fader".format(ch)
        fader = self._get(address)
        if datatype is "midi":
            return convertValueToMidiRange(fader["value"], fader_api_range, fader_midi_range, "log")
        else:
            return fader["value"]


    ###################################################
    def setMainFader(self, fader):
        """
        Set fader of a main 
        """
        address = "/mix/main/{}/matrix/fader".format(0)
        values = {"value": fader}
        return self._query(address, values)
 
    def getMainFader(self, datatype="api"):
        """
        Get fader of a main 
        """
        address = "/mix/main/{}/matrix/fader".format(0)
        fader = self._get(address)

        if fader:
            if datatype is "midi":
                return convertValueToMidiRange(fader["value"], fader_api_range, fader_midi_range, "log")
            else:
                return fader["value"]
        else:
            return False

    def setMonitorFader(self, fader):
        """
        Set fader of a monitor output
        """
        address = "/mix/monitor/{}/matrix/fader".format(0)
        values = {"value": fader}
        return self._query(address, values)

    def getMonitorFader(self, datatype="api"):
        """
        Get fader of a monitor
        """
        address = "/mix/monitor/{}/matrix/fader".format(0)
        fader = self._get(address)
        if fader:
            if datatype is "midi":
                return convertValueToMidiRange(fader["value"], fader_api_range, fader_midi_range, "log")
            else:
                return fader["value"]
        else:
            return False

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

    def getPan(self, ch, datatype="api"):
        """
        Get Pan of a given channel 
        > from -1 to 1
        """
        address = "/mix/chan/{}/matrix/pan".format(ch)
        pan = self._get(address)
        if datatype is "midi":
            return convertValueToMidiRange(pan["value"], [-1, 1], [0, 127])
        else:
            return pan["value"]

    ###################################################
    def setEq(self, ch, eq):
        """
        Big stuff to do here
        """
        print("TODO set EQ")

        eq = {
            "hpf": {
                "enabled": True,
                "freq": 40
            },
            "lowShelf": {
                "enabled": True,
                "freq": 80,
                "gain": 0,
                "bw": 1,
                "mode": 0
            },
            "mid1": {
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
            "highShelf": {
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
        """
        Enable compressor on given channel
        """
        print("TODO set Comp")

    def getComp(self, ch):
        """
        Knoww if compressor is enabled on given channel
        """
        print("TODO set Comp")

    ###################################################
    def muteMain(self, mute):
        """
        Mute main outputs
        """
        address = "/mix/main/{}/matrix/mute".format(0)
        values = {"value": 1 if mute else 0}
        self._query(address, values)
        return mute

    def getMainMute(self):
        """
        Is Main muted?
        """
        address = "/mix/main/{}/matrix/mute".format(0)
        mute = self._get(address)
        return bool(mute["value"] if mute else False)

    def muteMonitor(self, mute):
        """
        Mute monitor outputs
        """
        address = "/mix/monitor/{}/matrix/mute".format(0)
        values = {"value": 1 if mute else 0}
        self._query(address, values)
        return mute

    def getMonitorMute(self):
        """
        Is monitor muted?
        """
        address = "/mix/monitor/{}/matrix/mute".format(0)
        mute = self._get(address)
        return bool(mute["value"] if mute else False)

    def dim(self, status):
        """
        Apply -20dB on current master value
        """
        gain = self.settings.getDimValue("api")

        if status:
            self.setMainFader(gain)
        else:
            # revert to 0dB
            self.setMainFader(1)

    def getTrackName(self, ch):
        """
        Get the track name of a given channel
        :param ch:
        :return:
        """
        # TODO
        return "Track {}".format(ch)