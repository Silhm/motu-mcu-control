import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 


import mido
import time 
from modules.midiHelper import *


midiPort = mido.get_input_names()[0]
midiIN = mido.open_input(midiPort)
midiOUT = mido.open_output(midiPort)


fader     = True 
vPotCW    = False
vPotCCW   = False 
vPotClick = False
solo = False
mute = False 
fClick = False
bank = True

if fader:
    print("~~~~~ Moving faders ~~~~~~")
    ch = 0
    for i in range(-8000,8000):
        if i % 100 == 0:
            ch = ch +1
            ch = ch % 8
            msg = mido.Message('pitchwheel', pitch=i, channel=ch)
            #print("MIDI: {}  : Fader move".format(msg))
            midiOUT.send(msg)
            time.sleep(0.05)

    print("")



if solo:
    print("~~~~~ Click solo buttons ~~~~~~")
    for i in range(0,8):
        note = ["E0", "F0", "F#0", "G0", "G#0", "A0", "A#0", "B0"][i]
        msg = mido.Message('note_on', note=midiFullNoteToNumber(note), velocity=127) 
        midiOUT.send(msg)
        print("{} ".format(i+1), end='')
        time.sleep(0.5)
    # click again
    for i in range(0,8):
        note = ["E0", "F0", "F#0", "G0", "G#0", "A0", "A#0", "B0"][i]
        msg = mido.Message('note_on', note=midiFullNoteToNumber(note), velocity=127) 
        midiOUT.send(msg)
        print("{} ".format(i+1), end='')
        time.sleep(0.5)

    print("")

if mute:
    print("~~~~~ Click mute buttons ~~~~~~")
    for i in range(0,8):
        note = ["C1", "C#1", "D1", "D#1", "E1", "F1", "F#1", "G1"][i]
        msg = mido.Message('note_on', note=midiFullNoteToNumber(note), velocity=127) 
        midiOUT.send(msg)
        print("{} ".format(i+1), end='')
        time.sleep(0.5)
    # click again
    for i in range(0,8):
        note = ["C1", "C#1", "D1", "D#1", "E1", "F1", "F#1", "G1"][i]
        msg = mido.Message('note_on', note=midiFullNoteToNumber(note), velocity=127) 
        midiOUT.send(msg)
        print("{} ".format(i+1), end='')
        time.sleep(0.5)

    print("")


if vPotCW:
    print("~~~~~ Moving vPot up ~~~~~~")
    for ch in range(0,8):
        cc = [16, 17, 18, 19, 20, 21, 22, 23][ch]
        for i in range(0,30):
            msg = mido.Message('control_change',  control=cc, value=1)
            midiOUT.send(msg)
            time.sleep(0.01)
        print("{} ".format(ch+1), end='')
        time.sleep(0.2)

    print("")

if vPotCCW:
    print("~~~~~ Moving vPot down ~~~~~~")
    for ch in range(0,8):
        cc = [16, 17, 18, 19, 20, 21, 22, 23][ch]
        for i in range(0,50):
            msg = mido.Message('control_change',  control=cc, value=65)
            midiOUT.send(msg)
            time.sleep(0.01)
        print("{} ".format(ch+1), end='')
        time.sleep(0.2)

    print("")


if vPotClick:
    print("~~~~~ Clickin vPot ~~~~~~")
    for ch in range(0,8):
        note = ["G#1", "A1", "A#1", "B1", "C2", "C#2", "D2", "D#2"][ch]
        msg = mido.Message('note_on',  note=midiFullNoteToNumber(note), velocity=127)
        midiOUT.send(msg)
        time.sleep(0.5)
        print("{} ".format(ch+1), end='')
    print("")



if fClick:
    print("~~~~~ Clickin Function keys ~~~~~~")
    for f in range(0,8):
        note = ["G2","G#2","F2","F#2","G6","A6","G#6","A#6"][f]
        msg = mido.Message('note_on',  note=midiFullNoteToNumber(note), velocity=127)
        midiOUT.send(msg)
        time.sleep(0.5)
        print("F{} ".format(f+1), end='')
    print("")


if bank:
    print("~~~~~ Clickin Bank keys ~~~~~~")
    msg = mido.Message('note_on',  note=midiFullNoteToNumber("A#2"), velocity=127)
    midiOUT.send(msg)
    print("Bank UP ", end='')
    time.sleep(0.5)
    msg = mido.Message('note_on',  note=midiFullNoteToNumber("B2"), velocity=127)
    midiOUT.send(msg)
    print("| Bank DOWN", end='')
    time.sleep(0.5)

    print("")
