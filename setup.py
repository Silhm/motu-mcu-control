import sys
import argparse
import mido
from modules.midiHelper import *


allStrips = []


class Setup:
    def __init__(self, ipAddr=None, port=80):
        print("new setup")
        self.ipAddr = ipAddr
        self.port = port
        
        midiPort = mido.get_input_names()[0]
        self.midiIN = mido.open_input(midiPort)

    def setupInterface(self):
        print("Setup the MOTU: use 4 first vPot to set IP, validate with F1, cancel with F2")
        # listen to midi event
        
        vPotCC = [16, 17, 18, 19]
        ip = [0, 0, 0, 0]

        msg = self.midiIN.receive()
        while msg:
            if msg.type == "control_change" :
                direction = 1 if msg.value == 1 else -1
                potId = vPotCC.index(msg.control)

                ip[potId] = ip[potId] + direction

                sys.stdout.write("\r\x1b[K"+ip.__str__())
                sys.stdout.flush()
            
            if msg.type == "note_on":
                print("")
                midiFullNote = midiNumberToFullNote(msg.note)
                if midiFullNote == "G2":
                    print("Validated MOTU IP: {}.{}.{}.{}".format(ip[0], ip[1], ip[2], ip[3]))
                    self.ipAddr = "{}.{}.{}.{}".format(ip[0], ip[1], ip[2], ip[3])
                    break
                if midiFullNote == "G2":
                    print("Cancel ")
                    break

            msg = self.midiIN.receive()


def setupController(debug):

    print("=== This will drop all configuration an make a factory reset ===")
    print("=== It will use the MIDI learn system                        ===")

    print("")
    print("** Strips **")
    if debug:
        faderCount = 8
        print("=== It will use BCF settings to debug ===")
    else:
        faderCount = input('Enter the number of strips your controller can handle (8) : ')
        faderCount = faderCount if faderCount else 8

    for stripId in range(1, faderCount+1):
        stripAddrDef = {
                "id": stripId,
                "fader" : False,
                "vPot": False,
                "mute": False,
                "solo": False,
        }

        print(">> Strip ", stripId)
        print("     Move the Fader     ", end='')
        stripAddrDef['fader'] = ""
        if debug:
            stripAddrDef['fader'] = mido.Message('pitchwheel', pitch=0, channel=stripId) 
        print(" OK")
        
        print("     Click solo button  ", end='')
        stripAddrDef['solo'] = ""
        if debug:
            note = ["E0", "F0", "F#0", "G0", "G#0", "A0", "A#0", "B0"][stripId-1]
            stripAddrDef['solo'] = mido.Message('note_on',  note=midiFullNoteToNumber(note), velocity=127)
        print(" OK")

        print("     Click mute button  ", end='')
        stripAddrDef['mute'] = ""
        if debug:
            note = ["C1", "C#1", "D1", "D#1", "E1", "F1", "F#1", "G1"][stripId-1]
            stripAddrDef['mute'] = mido.Message('note_on',  note=midiFullNoteToNumber(note), velocity=127)
        print(" OK")

        print("     Move the vPot      ", end='')
        stripAddrDef['vPot'] = ""
        if debug:
            cc = [16, 17, 18, 19, 20, 21, 22, 23][stripId-1]
            stripAddrDef['mute'] = mido.Message('control_change',  control=cc, value=1)
        print(" OK")

        print("     Click the vPot      ", end='')
        stripAddrDef['vPotClick'] = ""
        if debug:
            note = ["G#1", "A1", "A#1", "B1", "C2", "C#2", "D2", "D#2"][stripId-1]
            stripAddrDef['vPotClick'] = mido.Message('note_on',  note=midiFullNoteToNumber(note), velocity=127)
        print(" OK")

        allStrips.append(stripAddrDef)

    print("** Function Keys **")
    print(" Click F1", end='')
    f1 = ""
    if debug:
        f1 = mido.Message('note_on',  note=midiFullNoteToNumber("G2"), velocity=127)

    print(" OK")
    print(" Click F2", end='')
    f2 = ""
    if debug:
        f2 = mido.Message('note_on',  note=midiFullNoteToNumber("G#2"), velocity=127)
    print(" OK")

    print(" Click F3", end='')
    f3 = ""
    if debug:
        f3 = mido.Message('note_on',  note=midiFullNoteToNumber("F2"), velocity=127)
    print(" OK")

    print(" Click F4", end='')
    f4 = ""
    if debug:
        f4 = mido.Message('note_on',  note=midiFullNoteToNumber("F#2"), velocity=127)
    print(" OK")

    print(" Click F5", end='')
    f5 = ""
    if debug:
        f5 = mido.Message('note_on',  note=midiFullNoteToNumber("G6"), velocity=127)
    print(" OK")

    print(" Click F6", end='')
    f6 = ""
    if debug:
        f6 = mido.Message('note_on',  note=midiFullNoteToNumber("A6"), velocity=127)
    print(" OK")
    
    print(" Click F7", end='')
    f7 = ""
    if debug:
        f7 = mido.Message('note_on',  note=midiFullNoteToNumber("G#6"), velocity=127)
    print(" OK")
    
    print(" Click F8", end='')
    f8 = ""
    if debug:
        f8 = mido.Message('note_on',  note=midiFullNoteToNumber("A#6"), velocity=127)
    print(" OK")

    print("** Misc **")
    print(" Click Bank +", end='')
    bankUp = ""
    if debug:
       bankUp = mido.Message('note_on',  note=midiFullNoteToNumber("A#2"), velocity=127)
    print(" OK")

    print(" Click Bank -", end='')
    bankDown = ""
    if debug:
        bankDown = mido.Message('note_on',  note=midiFullNoteToNumber("B2"), velocity=127)
    print(" OK")

    return {
            "global": {
                "f1": f1,
                "f2": f2,
                "f3": f3,
                "f4": f4,
                "f5": f5,
                "f6": f6,
                "f7": f7,
                "f8": f8
            },
            "strips": allStrips
        }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--debug", default=False, help="Put some default data")
    args = parser.parse_args()

    setupController(args.debug)
    print(allStrips)

