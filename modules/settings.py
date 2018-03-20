
class Settings:

    def __init__(self):
        self.faderPos = [0]*8
        self.vPotPos = [0]*8
        self.solo = [False]*8
        self.mute = [False]*8
        self.bank = 0

    #fader
    def setFaderPos(self, ch, val):
        self.faderPos[ch] = val
    
    def getFaderPos(self, ch):
        return self.faderPos[ch]

    #vPot
    def setVpotPos(self, ch, val):
        self.vPotPos[ch] = val
    
    def getVpotPos(self, ch):
        return self.vPotPos[ch] if self.vPotPos[ch] else 0

    #solo
    def setSolo(self, ch, status):
        self.solo[ch] = status
    
    def getSolo(self, ch):
        return self.solo[ch]

    #mute
    def setMute(self, ch, status):
        self.mute[ch] = status
    
    def getMute(self, ch):
        return self.mute[ch]

    #bank
    def getCurrentBank(self):
        return self.bank

    def setCurrentBank(self,bank):
        self.bank = bank
        
    

