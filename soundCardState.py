"""
This program will get the soundcard state by querying it and sending the right midi message to the controller
"""
import argparse
import random
import time
import json

import requests

import sqlite3

import mido

from modules.midiHelper import *

class State:

    def __init__(self, ipAddr=None, port=None ):
        self.ipAddr = ipAddr
        
        midiPort = mido.get_output_names()[0]
        self.midiOUT = mido.open_output(midiPort)

        self._chanData = False       
        self.stripCount = 8

    
    def getAll(self):
        """
        Get DataStore for all channels
        """
        print("Get All channels data")
        chanUrl = '/datastore/mix/chan/'

        url = "http://" + self.ipAddr + chanUrl
        r = requests.get(url)
        if r.status_code is 200:
            self._chanData = r.json()


    def refreshController(self):
        """
        Set the controller in the same state as the interface
        """
        print("refreshing controller state")

        if self._chanData:
            self.recalFader()
            self.recalSolo()
            self.recalMute()

        else:
            print(">> No data <<")


    def recalFader(self, fId=False):
        """
        Recal position of one fader or all if no id provided
        """
        if fId:
            chanFader = "mix/chan/{}/matrix/fader".format(fId)
            faderVal = self._chanData[chanFader]
            self._dispatchFader(faderVal, fId)
        else:
            for i in range(0,self.stripCount):
                chanFader = "mix/chan/{}/matrix/fader".format(i)
                faderVal = self._chanData[chanFader]
                self._dispatchFader(faderVal, i)
 

    def recalSolo(self, sId=False):
        """
        Recal state of button line 1 or all if no id provided
        """
        if sId:
            buttonId = "mix/chan/{}/matrix/solo".format(sId)
            buttonState = self._chanData[buttonId]
            self._dispatchButtonsLine1(buttonState, sId)
        else :
            for i in range(0,self.stripCount):
                buttonId = "mix/chan/{}/matrix/solo".format(i)
                buttonState = self._chanData[buttonId]
                self._dispatchButtonsLine1(buttonState, i)


    def recalMute(self, sId=False):
        """
        Recal state of button line 2 or all if no id provided
        """
        if sId:
            buttonId = "mix/chan/{}/matrix/mute".format(sId)
            buttonState = self._chanData[buttonId]
            self._dispatchButtonsLine2(buttonState, sId)
        else :
            for i in range(0,self.stripCount):
                buttonId = "mix/chan/{}/matrix/mute".format(i)
                buttonState = self._chanData[buttonId]
                self._dispatchButtonsLine2(buttonState, i)






        
    def _dispatchFader(self, faderValue, stripId):
        """
        Convert fader OSC value to MIDI value
        """
        apiRange = [0,4]
        midiRange = [-8192,8176]
        readyVal = convertValueToMidiRange(faderValue, apiRange, midiRange)
        
        # TODO: handle bank (should be available in database or memory)

        midiMessage = "{} ch: {} value:{}".format("pitchwheel", stripId, readyVal)
        msg = mido.Message('pitchwheel', pitch=readyVal, channel=stripId)
        self.midiOUT.send(msg)
        print("[{}][fader:{}] [midi OUT] : {} ".format(stripId, faderValue, msg))


    def _dispatchButtonsLine1(self,  buttonValue, stripId):
        """
        Convert Solo / Rec OSC value to MIDI value
        """
        soloMidiNotes = ["E0", "F0", "F#0", "G0", "G#0", "A0", "A#0", "B0"]
        
        midiNote = midiFullNoteToNumber(soloMidiNotes[stripId])
        midiVelocity = 127 if buttonValue else 0
        msg = mido.Message("note_on", note=midiNote, velocity=midiVelocity)
        self.midiOUT.send(msg)
        print("[{}][solo:{}] [midi OUT] : {} ".format(stripId, bool(buttonValue), msg))


    def _dispatchButtonsLine2(self,  buttonValue, stripId):
        """
        Convert Mute / Select OSC value to MIDI value
        """
        muteMidiNotes = ["C1", "C#1", "D1", "D#1", "E1", "F1", "F#1", "G1"]
        
        midiNote = midiFullNoteToNumber(muteMidiNotes[stripId])
        midiVelocity = 127 if buttonValue else 0
        msg = mido.Message("note_on", note=midiNote, velocity=midiVelocity)
        self.midiOUT.send(msg)
        print("[{}][mute:{}] [midi OUT] : {} ".format(stripId, bool(buttonValue), msg))

 
    def _dispatchButtonsLine2(self,  buttonValue, stripId):
        """
        Convert Mute / Select OSC value to MIDI value
        """
        muteMidiNotes = ["C1", "C#1", "D1", "D#1", "E1", "F1", "F#1", "G1"]
        
        midiNote = midiFullNoteToNumber(muteMidiNotes[stripId])
        midiVelocity = 127 if buttonValue else 0
        msg = mido.Message("note_on", note=midiNote, velocity=midiVelocity)
        self.midiOUT.send(msg)
        print("[{}][mute:{}] [midi OUT] : {} ".format(stripId, bool(buttonValue), msg))




if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", default="127.0.0.1",
        help="The ip of the OSC server")
    parser.add_argument("--port", type=int, default=8000,
        help="The port the OSC server is listening on")
    parser.add_argument("--debug", action="store_true", help="Use example datastore")
    args = parser.parse_args()

    state = State(args.ip, args.port)
    
    if args.debug:
        state._chanData = json.load(open('tests/datastore.json'))
    else:
        state.getAll()

    state.refreshController()
