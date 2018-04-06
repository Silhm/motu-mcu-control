import re
import math



def midiNoteToNumber(note, octave):
    _notes = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

    index = _notes.index(note)

    return ((octave+1) * 12) + index


def midiNumberToNote(number):
    _notes = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    index = number % 12
    note = _notes[index]
    octave = int((number-12)/12)
    # print("MIDI Note number "+str(number)+" : "+str(note)+str(octave))
    return (note,octave)


def midiNumberToFullNote(number):
    _notes = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    index = number % 12
    note = _notes[index]
    octave = int((number-12)/12)
    # print("MIDI Note number "+str(number)+" : "+str(note)+str(octave))
    return "{}{}".format(note, octave)


def midiFullNoteToNumber(fullNote):
    """
    Convert a note like A1, G#4 or F#-1 to a number
    """
    midiPattern = re.compile('([A-G]#?)(-?[0-9])')
    m = midiPattern.match(fullNote)

    if m:
        return int(midiNoteToNumber(str(m.group(1)), float(m.group(2))))


def convertValueToMidiRange(oscValue, oscRange, midiRange):
    """
    value : OSC value
    OscRange: 
    midiRange
    """
    minOSC = oscRange[0]
    maxOSC = oscRange[1]

    minMidi = midiRange[0]
    maxMidi = midiRange[1]

    percent = (oscValue - minOSC) / (maxOSC-minOSC) * 100.0
    midiVal = (maxMidi - minMidi) * percent / 100 + minMidi

    return int(midiVal)


def convertValueToOSCRange(midiValue, oscRange, midiRange, scale="linear"):
    """
    value : OSC value
    OscRange: 
    midiRange
    """
    print("scale {}".format(scale))
    #  midi    API   decibels
    #  8000 ->  4     +12dB      20log(4)
    #  4000 ->  1       0db      20log(1)
    # -8000 ->  0     -12dB      20log(0.001)  #log(0) is -inf

    minOSC = oscRange[0]
    maxOSC = oscRange[1]

    minMidi = midiRange[0]
    maxMidi = midiRange[1]
    percent = (midiValue - minMidi) / (maxMidi - minMidi) * 100.0
    oscVal = (maxOSC - minOSC) * percent / 100 + minOSC

    if scale is "log":
        # analyze https://stackoverflow.com/questions/846221/logarithmic-slider#846249
        # and : https: // www.image - line.com / support / FLHelp / html / mixer_dB.htm
        """
        minOSC = math.log(minOSC)
        maxOSC = math.log(maxOSC)
        # calculate adjustment factor
        sc = (maxOSC - minOSC) / (maxMidi - minMidi)
        oscVal = math.exp(minOSC + sc*(midiValue-minMidi))
        """
        oscVal = 20 * math.log(oscVal)


    print(" PITCH = {}  >>  VAL = {}".format(midiValue, oscVal))
    return oscVal
