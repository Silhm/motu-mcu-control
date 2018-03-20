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


print("~~~~~ Moving vPot up ~~~~~~")
ch = 0    
cc = [16, 17, 18, 19, 20, 21, 22, 23][ch]
# first IP block
for i in range(0,127):
    msg = mido.Message('control_change',  control=16, value=1)
    midiOUT.send(msg)
    time.sleep(0.01)
time.sleep(0.2)
# 2nd IP block
for i in range(0,27):
    msg = mido.Message('control_change',  control=17, value=1)
    midiOUT.send(msg)
    time.sleep(0.01)
for i in range(0,27):
    msg = mido.Message('control_change',  control=17, value=65)
    midiOUT.send(msg)
    time.sleep(0.01)

time.sleep(0.5)
# 3rd IP block    
for i in range(0,28):
    msg = mido.Message('control_change',  control=18, value=1)
    midiOUT.send(msg)
    time.sleep(0.01)
for i in range(0,28):
    msg = mido.Message('control_change',  control=18, value=65)
    midiOUT.send(msg)
    time.sleep(0.01)

time.sleep(0.5)
# 4th
msg = mido.Message('control_change',  control=19, value=1)
midiOUT.send(msg)
time.sleep(0.01)


msg = mido.Message('note_on',  note=midiFullNoteToNumber("G2"))
midiOUT.send(msg)

