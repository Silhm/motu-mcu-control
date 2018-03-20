import re

def midiNoteToNumber(note, octave):
    _notes = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

    index = _notes.index(note)

    return ((octave+1) * 12) + index

def midiNumberToNote(number):
    _notes = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    index = number % 12
    note = _notes[index]
    octave = int((number-12)/12)
    #print("MIDI Note number "+str(number)+" : "+str(note)+str(octave))
    return (note,octave)


def midiNumberToFullNote(number):
    _notes = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    index = number % 12
    note = _notes[index]
    octave = int((number-12)/12)
    #print("MIDI Note number "+str(number)+" : "+str(note)+str(octave))
    return "{}{}".format(note,octave)


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

    percent = (oscValue - minOSC ) / (maxOSC-minOSC) * 100.0
    midiVal = (maxMidi - minMidi) * percent  / 100 + minMidi

    return int(midiVal)


def convertValueToOSCRange(midiValue, oscRange, midiRange):
    """
    value : OSC value
    OscRange: 
    midiRange
    """
    minOSC = oscRange[0]
    maxOSC = oscRange[1]

    minMidi = midiRange[0]
    maxMidi = midiRange[1]

    percent = (midiValue - minMidi ) / (maxMidi-minMidi) * 100.0
    oscVal = (maxOSC - minOSC) * percent  / 100 + minOSC

    return oscVal
