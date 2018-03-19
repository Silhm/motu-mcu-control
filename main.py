"""
This program is the main one
"""
import argparse
from midiWait import MidiWait



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", default="127.0.0.1",
            help="The ip of the DAW OSC server")
    parser.add_argument("--port", type=int, default="80",
            help="The port the DAW OSC is listening to")
    args = parser.parse_args()

    midiWait = MidiWait(args.ip, args.port)
    
    
    
    
    
    
    while midiWait.read():
        pass
