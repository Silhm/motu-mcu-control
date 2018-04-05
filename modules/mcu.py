import mido
import time 

from modules.midiHelper import *

fader_api_range = [0, 4]
fader_midi_range = [-8192, 8176]

class MCU:
    def __init__(self):
        inPort = mido.get_input_names()[0]
        outPort = mido.get_output_names()[0]
        self.midiIN = mido.open_input(inPort)
        self.midiOUT = mido.open_output(outPort)

        self.mode = "main"
        self.vPotMode = "pan"

    def setMode(self, mode):
        """
        Define the mcu mode
        default is main mode
        """
        self.mode = mode 
        modeNotes = {
                "main": "A#4",
                "mixing": "D#3",
                # "send": "A2",
                # "unknown": "A#2"
        }
        note = midiFullNoteToNumber(modeNotes[mode])
        
        # first, turn off all leds
        self.midiOUT.send(mido.Message("note_on", note=70, velocity=0))
        self.midiOUT.send(mido.Message("note_on", note=51, velocity=0))

        # then, light on the good one!
        self.midiOUT.send(mido.Message("note_on", note=note, velocity=127))

    def getMode(self):
        """
        Get the current set mode
        """
        return self.mode

    def fLed(self, fId, status):
        """
        from 1 to 8
        """
        functionMidiNotes = ["G#2", "G2", "F#2", "F2", "G6", "G#6", "A6", "A#6"]
        note = midiFullNoteToNumber(functionMidiNotes[fId-1])
        msg = mido.Message("note_on", note=note, velocity=127 if status else 0)
        self.midiOUT.send(msg)
        print("led {}: {}".format(fId, functionMidiNotes[fId-1]))
        print(msg)

    def l1Led(self, fId, status):
        """
        from 1 to 8
        """
        l1MidiNotes =["E0", "F0", "F#0", "G0", "G#0", "A0", "A#0", "B0"]
        note = midiFullNoteToNumber(l1MidiNotes[fId-1])
        msg = mido.Message("note_on", note=note, velocity=127 if status else 0)
        self.midiOUT.send(msg)

    def l2Led(self, fId,status):
        """
        from 1 to 8
        """
        l2MidiNotes = ["C1", "C#1", "D1", "D#1", "E1", "F1", "F#1", "G1"]
        note = midiFullNoteToNumber(l2MidiNotes[fId-1])
        msg = mido.Message("note_on", note=note, velocity=127 if status else 0)
        self.midiOUT.send(msg)

    def vPotRing(self, vPotId, value, mode):
        """
        mode could be :
            - "single-dot" (default)
            - "boost-cut"
            - "wrap"
            - "spread"
        needTo analyze LogicControl_EN.pdf

        B0, 3i, XX
            31 hex  = 49 dec
            XX:  0 p xx vv vv
                 p : center led on (1) / off (0) -> no use with BCF
                xx : vpot mode 00 -> 03
                vv : value 00 -> 7F
        """
        modeByte = {
                "single-dot": 0,
                "boost-cut": 1,
                "wrap": 2,
                "spread": 3
        }

        byteArray = [0, 1, 0, modeByte[mode]]
        valueAsBytes = (int(value)).to_bytes(1, byteorder='big')

        bytesVal = bytes(byteArray) + valueAsBytes 
        ccValue = 0
        for bit in bytesVal:
            ccValue = (ccValue << 1) | bit

        print("vPot {}:{}  bytes[{}]   valToSend: {}".format(vPotId,value, bytesVal, ccValue))

        cc = list(range(48, 56))[vPotId-1]
        
        msg = mido.Message('control_change',  control=cc, value=ccValue)
        self.midiOUT.send(msg)

    def faderPos(self, fId, pos):
        """
        :param fId:
        :param pos:
        :return:
        """
        msg = mido.Message('pitchwheel',  channel=fId, pitch=pos)
        self.midiOUT.send(msg)

    def resetController(self):
        """
        Reset controller to null state
        """
        for f in range(0, 8):
            self.faderPos(f, fader_midi_range[0])
            self.l1Led(f, False)
            self.l2Led(f, False)
            self.fLed(f, False)


if __name__ == "__main__":
    mcu = MCU()
    
    for i in range(1,9):
        mcu.fLed(i,True)
        time.sleep(0.1)
    for i in range(1,9):
        mcu.fLed(i,False)
        time.sleep(0.1)
    
    for i in range(1,9):
        mcu.l1Led(i,True)
        time.sleep(0.1)
    for i in range(1,9):
        mcu.l1Led(i,False)
        time.sleep(0.1)

    for i in range(1,9):
        mcu.l2Led(i,True)
        time.sleep(0.1)
    for i in range(1,9):
        mcu.l2Led(i,False)
        time.sleep(0.1)

    for i in range(1, 9):
        for j in range(0, 127):
            mcu.vPotRing(i, j, "single-dot")
            time.sleep(0.01)

        time.sleep(0.1)
