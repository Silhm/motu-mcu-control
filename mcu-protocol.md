Work in progress...

# Understanding Mackie Control Protocol

Mackie Control Protocol (MCP) is a protocol to exchange information between the DAW and the control surface.
If data transmitted or received is bigger than 3 bytes, the MCP will use SysEx, otherwise it uses standard MIDI messages.

All byte are transmitted in Hex format (something like 0xF0, 0x6C and so one). For readability, all this bytes will be 
written without the '0x' notation.

This is inspired by [Logic Control Manual](http://stash.reaper.fm/2063/LogicControl_EN.pdf).

### SysEx format

The first 5 bytes transmitted to the controller are something like F0 00 00 66 00 :
* F0 : Start of the SysEx Data
* 00 00 66 : manufacturer id (mackie)
* 00 : product id (I guess)

As describe in the marual, this header will be simplified as <hdr> in this document.



### Displaying Data on LCD

DAW -> controller

* Every LCD message start with the header <hdr> followed by the 0x12 byte.
* Then the next byte tells the position to display the text.
* We get the actual text (mostly 6 chars)
* Finally, the SysEx ends with a 0xF7 byte

Example:

    F0 00 00 66 00 12 38 ***4C 35 30 52 35 30 20*** FC
     <hdr>         |   \_position                     \_end of SysEx
              LCD message


## Position of the text on the LCD

On a Mackie Control, the LCD screen has 2x56 characters, divided by 8 (8 channels on a BCF2000) equals 7 chars by channel.

Each position on the screen is identified by an offset:

* From 00 to 37 (56 values) for the first line,
* From 38 to 6F (56 values) for the second line 

So the LCD screens could be represented like this:
![LCD](http://i.imgur.com/Dh8LDwu.png)

In my example SysEx, the 0x38 byte following the 0x12 one, means that the text will be displayed on the 2nd line, first character.


## Displaying text

To display the text, just convert the Hex values to Char according to the ASCII table.

In Arduino code, a simple _display.write()_ will convert Hex value to Char.

    So 4C 35 30 52 35 30 20
    is  L  5  0  R  5  0      

So we got a PAN message : **L50R50** to display on the second line!

![text on second line](http://i.imgur.com/oAMDVcw.png)



