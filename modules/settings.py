import shelve
from modules.midiHelper import *


class Settings:
    """
    Class to handle settings to keep in memory
    """

    def __init__(self):
        self.faderPos = [0]*8
        self.vPotPos = [0]*8
        self.solo = [False]*8
        self.mute = [False]*8
        self.function = [False]*8
        self.bank = 0

        self._db = shelve.open("config.db")

    def _store(self, key, val):
        self._db[key] = val

    def _recall(self, key):
        return self._db[key]

    def restoreDefault(self):
        self.setMcuMode("main")
        self.setStripCount(8)
        self.setFlipMode(False)
        self.setDimValue(-20)


    # fader
    def setFaderPos(self, ch, val):
        self.faderPos[ch] = val

    def getFaderPos(self, ch):
        return self.faderPos[ch]

    # vPot
    def setVpotPos(self, ch, val):
        self.vPotPos[ch] = val
    
    def getVpotPos(self, ch):
        return self.vPotPos[ch] if self.vPotPos[ch] else 0

    # solo
    def setSolo(self, ch, status):
        self.solo[ch] = status
    
    def getSolo(self, ch):
        return self.solo[ch]

    # mute
    def setMute(self, ch, status):
        self.mute[ch] = status
    
    def getMute(self, ch):
        return self.mute[ch]

    # bank
    def getCurrentBank(self):
        return self.bank

    def setCurrentBank(self, bank):
        self.bank = bank
        
    # F buttons
    def setFunction(self, fId, status):
        self.function[fId] = status
        return status

    def getFunction(self, fId):
        return self.function[fId]

    def setMcuMode(self, mode):
        """
        Set the mcu mode
        :return:
        """
        self._store("mcumode", mode)

    def getMcuMode(self):
        return self._recall("mcumode")

    def setStripCount(self, count):
        """
        Get the number of strip available
        :return:
        """
        self._store("stripCount", count)

    def getStripCount(self):
        """
        Get the number of strip available
        :return:
        """
        return self._recall("stripCount")

    # flipMode
    def setFlipMode(self, flip):
        """
        Flip mode to reverse vPot and faders
        :param flip:
        :return:
        """
        self._store("flipMode", flip)


    def getFlipMode(self):
        """
        Know if flipmode is activated
        :return:
        """
        return self._recall("flipMode")


    # dim values
    def setDimValue(self, gain):
        """
        How much gain should be applied when pressing dim button
        :param gain: in db
        :return:
        """
        self._store("dimValue", gain)

    def getDimValue(self, datatype="db"):
        """
        How much gain should be applied when pressing dim button
        :return gain: in dB
        """
        gain = self._recall("dimValue")
        if datatype is "api":
            gain = convertDecibelToAPI(gain)

        return gain

