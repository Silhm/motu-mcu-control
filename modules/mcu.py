import mido
import time 

from midiHelper import *


class MCU:
    def __init__(self):
        inPort = mido.get_input_names()[0]
        outPort = mido.get_output_names()[0]
        self.midiIN = mido.open_input(inPort)
        self.midiOUT = mido.open_output(outPort)

    
    def fLed(self, fId,status):
        """
        from 1 to 8
        """
        functionMidiNotes = ["G#2","G2","F#2","F2","G6","G#6","A6","A#6"]
        note = midiFullNoteToNumber(functionMidiNotes[fId-1])
        msg = mido.Message("note_on", note=note, velocity=127 if status else 0)
        self.midiOUT.send(msg)
        print("led {}: {}".format(fId, functionMidiNotes[fId-1]))
        print(msg)



    def l1Led(self, fId,status):
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


    def vPotRing(self, vPotId, value, mode="single-dot"):
        """
        mode could be :
            - "single-dot" (default)
            - "boost-cut"
            - "wrap"
            - "spread"
        needTo analyze LogicControl_EN.pdf
        """
        modeByte = {
                "single-dot":0,
                "boost-cut":1,
                "wrap":2,
                "spread":3
        }
        
        ccValue = bytes([0,1, 0,modeByte[mode], 7,2, 7,16])


        print("vPot {}:{}".format(vPotId,value))
        cc = [30, 31, 32, 33, 34, 35, 36, 37][vPotId-1]
        msg = mido.Message('control_change',  control=cc, value=65)
        self.midiOUT.send(msg)


    def faderPos(self, fId, pos):
        print("TODO: fader pos")
    



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
