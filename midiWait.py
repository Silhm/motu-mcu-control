"""
This program handle MIDI from an MCU midi controller and create event to send to the mixer
"""
import argparse
import json

import requests 

import mido

from modules.midiHelper import *
from modules.settings import Settings 
from modules.mcu import MCU 
from modules.motu import Motu
from setup import Setup


class MidiWait:

    def __init__(self, ipAddr=None, port=80):
        # Init Midi client and display available devices
        midiINPort = mido.get_input_names()[0]
        midiOUTPort = mido.get_output_names()[0]
        self.midiIN = mido.open_input(midiINPort)
        self.midiOUT = mido.open_output(midiOUTPort)
        self.mcu = MCU()
        self.motu = Motu(ipAddr, port)
        self.settings = Settings()
        self.hwSetup = Setup()
    
        self.mixerUrl = "http://{}:{}".format(ipAddr, port)
        print("Will send events to mixer at {}".format(self.mixerUrl))

        self.recall()

    def setup(self):
        """
        Set up the bridge
        """
        self.hwSetup.setupInterface()

    def sendQueryMessage(self, address, value):
        """
        Send the corresponding  message
            - address is a string
            - value is an array
        """
        value = json.dumps(value)
        url = "{}/datastore{}".format(self.mixerUrl, address)
        print("{} {}".format(url, value))

        r = requests.post(url, {"json":value})
        # print(">Query [{}] {}  {} with data {}".format(r.status_code,self.mixerUrl, address,value))
        print("{}".format(r))

    def routeMessage(self, midiMessage):
        print("midiIN {}:".format(midiMessage))
        # Faders
        if midiMessage.type == "pitchwheel":
            self._handlePitchWheel(midiMessage.channel, midiMessage.pitch)

        # vPots
        if midiMessage.type == "control_change" :
            self._handleVpotRot(midiMessage.control,midiMessage.value)
            
        if midiMessage.type == "note_on" and midiMessage.velocity == 127 :
            soloMidiNotes = ["E0", "F0", "F#0", "G0", "G#0", "A0", "A#0", "B0"]
            muteMidiNotes = ["C1", "C#1", "D1", "D#1", "E1", "F1", "F#1", "G1"]
            vPotMidiNotes = ["G#1", "A1", "A#1", "B1", "C2", "C#2", "D2", "D#2"]
            bankMidiNotes = ["A#2","B2"]
            functionMidiNotes = ["G2","G#2","F2","F#2","G6","A6","G#6","A#6"]
            midiFullNote = midiNumberToFullNote(midiMessage.note)
            
            # Solo
            if midiFullNote in soloMidiNotes:
                ch  = soloMidiNotes.index(midiFullNote) + 1
                self._handleSoloButton(ch)

            # Mute
            if midiFullNote in muteMidiNotes:
                ch  = muteMidiNotes.index(midiFullNote) + 1
                self._handleMuteButton(ch)

            # vPots click
            if midiFullNote in vPotMidiNotes:
                ch  = vPotMidiNotes.index(midiFullNote) + 1
                self._handleVpotClick(ch)

            # Bank buttons 
            if midiFullNote in bankMidiNotes:
                bankUp = bankMidiNotes.index(midiFullNote) == 0
                self._handleBankButton(bankUp)

            # Function buttons 
            if midiFullNote in functionMidiNotes:
                f = functionMidiNotes.index(midiFullNote)
                self._handleFunctionButton(f)

    def read(self):
        """ Read Midi message """
        msg = self.midiIN.receive()
        self.routeMessage(msg)
        return msg

    # TODO
    def _handleEncoderGrpButtons(self, name, clicked):
        """
        Handle the Encoder groups button (only top and bottom right)
        """
        """
        if clicked and name == "TopRight" :
            self.db.setButtonMode("solomute")
        elif clicked and name == "BottomRight":
            self.db.setButtonMode("selectrec")
        """
        print("button mode: {}".format(name))

    def _handleFunctionButton(self, fNum):
        """
        Handle the function Buttons F1 -> F8    
        """
        print("Button F{} clicked".format(fNum+1))
        # get previous know state and toggle it
        fState = self.settings.getFunction(fNum)

        if fNum == 7:
            self.motu.dim(fState)
            fState = self.settings.setFunction(fNum,not fState)
            # update led on button
            self.mcu.fLed(8,fState)

    def _handleBankButton(self, up):
        """
        Handle bank buttons
        """
        bank = self.settings.getCurrentBank()

        if up: 
            bank = bank + 1
        else :
            bank = bank - 1

        if bank < 0:
            bank = 0
        print("BANK is {}".format(bank))

        self.settings.setCurrentBank(bank)

    def _handlePitchWheel(self, ch, value):
        """
        Handle fader moves
        """
        self.settings.setFaderPos(ch,value) 
        
        apiRange = [0,4]
        midiRange = [-8192,8176]
        
        faderValue = convertValueToOSCRange(value, apiRange, midiRange)
        # todo : log scale?    

        if ch is 7: # and mode is monito!
            self.motu.setMainFader(faderValue)
        elif ch is 6: # and mode is monito!
            self.motu.setMonitorFader(faderValue)
        else:
            self.motu.setFader(ch, faderValue)

        self.mcu.faderPos(ch, value)        

    def _handleVpotClick(self, ch):
        """
        Handle vPot click: restore default pan or gain
        """
 
        newPos = 0
        address = "/mix/chan/{}/matrix/pan".format(ch)
        values = { "value":newPos}
        self.sendQueryMessage(address, values)
        self.settings.setVpotPos(ch,newPos)

    def _handleVpotRot(self, cc, value):
        """
        Handle vPot rotation 
        TODO: speed
        """
        vPotCC = [16, 17, 18, 19, 20, 21, 22, 23]
        
        if cc in vPotCC:
            ch = vPotCC.index(cc) 
        
        currentPos = self.motu.getPan(ch)
        apiRange = [-1, 1]
        midiRange = [0, 127]

        address = "/mix/chan/{}/matrix/pan".format(ch)
        direction = 1 if 1 <= value <= 15 else -1
        # speed= rotation[1] if rotation[1]>1 else 1
        # _speeds = [10, 3, 2, 2, 1, 1, 1, 1, 1 , 1]
        # newVal = currentVal + (direction * 5 * (pow(10, -1 * _speeds[speed]  )))

        newPos = round(currentPos + (direction * 0.05), 3)

        if newPos > apiRange[1]:
            newPos = apiRange[1]
        if newPos < apiRange[0]:
            newPos = apiRange[0]
        
        self.settings.setVpotPos(ch, newPos)
        values = {"value": newPos}
        self.sendQueryMessage(address, values)
        
        # update led ring
        midiVal = convertValueToMidiRange(newPos, apiRange, midiRange)
        self.mcu.vPotRing(ch, midiVal, "single-dot")

    def _handleSoloButton(self, ch):
        """
        Handle soloButton click 
        """
        # get motu state and toggle it
        mcuMode = self.mcu.getMode()
        print("mcuMode : {}", format(mcuMode))
        if mcuMode is "main":
            if ch == 7: 
                # monitoring toggle
                mute = self.motu.getMonitorMute()
                m = self.motu.muteMonitor(not mute)
                self.mcu.l1Led(7, not m)
            if ch == 8: 
                # main toggle
                mute = self.motu.getMainMute()
                m=self.motu.muteMain(not mute)
                self.mcu.l1Led(8, not m)

        else:
            solo = self.settings.getSolo(ch)
            address = "/mix/chan/{}/matrix/solo".format(ch)

            newStatus = not solo

            values = {"value": newStatus}
            self.sendQueryMessage(address, values)
            
            self.settings.setSolo(ch, newStatus)

    def _handleMuteButton(self, ch):
        """
        Handle muteButton click 
        """
        # get previous know state and toggle it
        mute = self.settings.getMute(ch)
        address = "/mix/chan/{}/matrix/mute".format(ch)

        newStatus = not mute 

        values = {"value": newStatus}
        self.sendQueryMessage(address, values)
        
        self.settings.setMute(ch, newStatus)

    def recall(self):
        """
        Set back everything
        """
        # todo check mode first
        apiRange = [0,4]
        midiRange = [-8192,8176]
        mainFader = self.motu.getMainFader()
        monitorFader = self.motu.getMonitorFader()
        mainFaderValue = convertValueToMidiRange(mainFader, apiRange, midiRange)
        monitorFaderValue = convertValueToMidiRange(monitorFader, apiRange, midiRange)
        self.mcu.faderPos(6, monitorFaderValue )
        self.mcu.faderPos(7, mainFaderValue )

        self.mcu.l1Led(7, not self.motu.getMonitorMute())
        self.mcu.l1Led(8, not self.motu.getMainMute())


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", default="127.0.0.1", help="The ip of the DAW OSC server")
    parser.add_argument("--port", type=int, default="80", help="The port the DAW OSC is listening to")
    args = parser.parse_args()

    midiWait = MidiWait(args.ip, args.port)

    # Read Midi
    print("Read midi input...")

    while midiWait.read():
        pass


