# Motu-MCU-control
Control your MOTU AVB soundcard with your MCU enabled controller

Based on documentation from MOTU:  http://cdn-data.motu.com/downloads/audio/AVB/avb_osc_api.pdf

Work in progress...

This program convert data from your Midi controller and send it to your MOTU sound interface.
It can be placed on your computer or on a RaspberryPi like computer board.

For now, it's one way, from MCU to MOTU and it still need to be tested in conditions

# Quick start 
- Connect your MCU (in my case a BCF2000) to the RaspberryPi with USB and connect the RaspberryPi to the network where the MOTU soundcard is.
- Run the main.py program (you can use *--ip* arguments to set the MOTU interface IP address)
- That's it!

## TODO
* Handle data from the Motu interface
* Handle MCU controls to fit the MOTU settings

* Handle banks to use multiple layers of fader
* Handle the send mode
* Handle flip mode (invert fader and rotary vPot)
* Add a mute all / unmute all
* Add a clear solo button
* Handle MCU extension for larger setups

* Create a virtual strip to control EQ, Comp, and Limiter
* Display track names and values on scribbles 
* Improve setup routine (via a remote web interface or directly ) to setup the MOTU IP address and other relevant settings

