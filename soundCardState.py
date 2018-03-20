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
        self._chanData = False
    
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
        #TODO: handle all the data once I got to know the datastore format


        
    def _dispatchFader(self, address, stripId, faderValue):
        """
        Convert fader OSC value to MIDI value
        """
        faderMidiRange = self.ctrlConfig.getFaderMidiRange()
        faderOSCRange = self.dawConfig.getFaderOSCRange()
        faderMove = self.ctrlConfig.getFaderMove("type")
        readyVal = convertValueToMidiRange(faderValue, self.dawConfig.getFaderOSCRange(), self.ctrlConfig.getFaderMidiRange())
        
        # TODO: handle bank (should be available in database or memory)
        # stripId with bank handle
        bank = self.db.getCurrentBank()
        bankSize = self.db.getBankSize()
        
        sId = stripId

        # need to stay in 1 -> bankSize range
        if(sId > bankSize):
            sId = (sId % bankSize) +1


        midiMessage = "{} ch: {} value:{}".format(faderMove, sId, readyVal)
        print("Dispatching OSC: {} {} {} to MIDI: {}  ".format(address,stripId,faderValue, midiMessage))
        
        msg = mido.Message('pitchwheel', pitch=readyVal, channel=sId)
        self.midiOUT.send(msg)


    def _dispatchButtonsLine1(self, address, stripId, buttonValue):
        """
        Convert Solo / Rec OSC value to MIDI value
        """
        # Do nothing if not good mode
        buttonMode = self.db.getButtonMode()
        bank = self.db.getCurrentBank()
        bankSize = self.db.getBankSize()

        if buttonMode == "solomute" and "rec" in address:
            return
    
        line = 1
        buttonsMidiNotes  = self.ctrlConfig.getButtonNotes(line)
        buttonsMidiType = self.ctrlConfig.getButtonType(line)

        sId = stripId -1
        # need to stay in 1 -> bankSize range
        if(sId >= bankSize):
            sId = (sId % bankSize) 

        midiNote = midiFullNoteToNumber(buttonsMidiNotes[sId])
        midiVelocity = 127 #buttonsMidiValueOn if buttonValue else buttonsMidiValueOff
        msg = mido.Message(buttonsMidiType, note=midiNote, velocity=midiVelocity)
        print("Dispatching OSC: {} {} {} to MIDI: {}  ".format(address,stripId,buttonValue, msg))
        self.midiOUT.send(msg)


    def _dispatchButtonsLine2(self, address, stripId, buttonValue):
        """
        Convert Mute / Select OSC value to MIDI value
        """
        buttonMode = self.db.getButtonMode()
        bank = self.db.getCurrentBank()
        bankSize = self.db.getBankSize()

        # Do nothing if not good mode
        if buttonMode == "solomute" and "select" in address:
            return
        
        line = 2
        buttonsMidiNotes  = self.ctrlConfig.getButtonNotes(line)
        buttonsMidiType = self.ctrlConfig.getButtonType(line)
 
        sId = stripId - 1
        # need to stay in 1 -> bankSize range
        if(sId >= bankSize):
            sId = (sId % bankSize) 

        midiNote = midiFullNoteToNumber(buttonsMidiNotes[sId])

        midiVelocity = 127 #buttonsMidiValueOn if buttonValue else buttonsMidiValueOff
        msg = mido.Message(buttonsMidiType, note=midiNote, velocity=midiVelocity)
        print("Dispatching OSC: {} {} {} to MIDI: {}  ".format(address,stripId,buttonValue, msg))
        self.midiOUT.send(msg)


    def _dispatchFunctionButtons(self, address, bname):
        """
        Convert Mute / Select OSC value to MIDI value
        """
        bname = bname[0]
        
        fNote  = midiFullNoteToNumber(self.ctrlConfig.getfButtonNote(bname,"note"))
        fVelocity = self.ctrlConfig.getfButtonNote(bname,"valueOn")
        fChannel = self.ctrlConfig.getfButtonNote(bname,"ch")
        fType = self.ctrlConfig.getfButtonNote(bname,"type")

        msg = mido.Message(fType, note=fNote, velocity=fVelocity, channel=fChannel)
        print("Dispatching OSC: {} (mapped to {}) to MIDI: {}  ".format(address,bname, msg))
        self.midiOUT.send(msg)






if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", default="127.0.0.1",
        help="The ip of the OSC server")
    parser.add_argument("--port", type=int, default=8000,
        help="The port the OSC server is listening on")
    args = parser.parse_args()

    state = State(args.ip, args.port)
    
    state.getAll()
    state.refreshController()
