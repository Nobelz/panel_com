"""
panel_com.py

Python class rewrite of the serial interface with Micahel Reiser's panel controller.

Author: Various authors (see below)
Version: 1.0

Revision History:
    2004?: Original Matlab code by Michael Reiser
    2006?: Translated to Python by SAB
    4/8/2007: Made into a class by JAB
    2008?: Made into a stand alone python package by Will Dickson
    v1.0 (7/17/2023): Revised and added additional functionality by Nobel Zhou (nxz157@case.edu)
"""

# Constants
GAIN_MAX = 10.0
GAIN_MIN = -10.0
OFFSET_MAX = 5.0
OFFSET_MIN = -5.0

import serial
import types

class PanelCom:
    def __init__(self, port, baudrate):
        self.ser = serial.Serial(port=port, baudrate=baudrate, timeout=None)
        
    def SetPatternID(self, patternid):
        if type(patternid) != types.IntType: raise TypeError
        if patternid < 0: raise ValueError
        self.send(chr(0x02) + chr(0x03) + chr(patternid))

    def BlinkLED( self ): self.send(chr(0x01) + chr(0x50))

    def AllOn( self ): self.send(chr(0x01) + chr(0xFF))

    def AllOff( self ): self.send(chr(0x01) + chr(0x00))

    def Greenscale( self, level ):
        if type(level) != types.IntType: raise TypeError
        if level < 0 or level > 7: raise ValueError
        self.send(chr(0x01) + chr(0x40 + level))

    def Start( self ): self.send(chr(0x01) + chr(0x20))

    def Stop( self ): self.send(chr(0x01) + chr(0x30))

    def Reset( self ): self.send(chr(0x02) + chr(0x01) + chr(0x00))

    def SetMode( self, modex, modey ):
        if type(modex) != types.IntType or type(modey) != types.IntType:
            raise TypeError
        if modex < 0 or modey < 0 or modex > 4 or modey > 4:
            raise ValueError
        self.send(chr(0x03) + chr(0x10) + chr(modex) + chr(modey))

    def SetGainOffset(self,gainx,offsetx,gainy,offsety):
        gainx_num = get_char_num(round(100.0*gainx/GAIN_MAX))
        gainy_num = get_char_num(round(100.0*gainy/GAIN_MAX))
        offsetx_num = get_char_num(round(100.0*offsetx/OFFSET_MAX))
        offsety_num = get_char_num(round(100.0*offsety/OFFSET_MAX))
        msg = chr(0x05) + chr(0x71) + chr(gainx_num) + chr(offsetx_num) + chr(gainy_num) + chr(offsety_num)
        self.send(msg)

    def SetPositions(self,xpos,ypos):
        if type(xpos) != types.IntType or type(ypos) != types.IntType:
            raise TypeError
        if xpos < 0 or xpos > 255 or ypos < 0 or ypos > 255:
            raise ValueError
        self.send(chr(0x05) + chr(0x70) + chr(xpos) + chr(0x00) + chr(ypos) + chr(0x00))

    def SetAO(self, chan, val):
        if type(chan) != types.IntType or type(val) != types.IntType:
            raise TypeError
        if chan < 1 or chan > 4 or abs(val) > 255:
            raise ValueError
        if val > 0:
            self.send(chr(0x04) + chr(0x10) + chr(chan) + chr(0x00) + chr(val))
        else:
            self.send(chr(0x04) + chr(0x11) + chr(chan) + chr(0x00) + chr(abs(val)))

    def Address( self, oldaddr, newaddr ):
        if type(oldaddr) != types.IntType or type(newaddr) != types.IntType:
            raise TypeError
        if oldaddr < 0 or newaddr < 0: raise ValueError
        self.send(chr(0x03) + chr(0xFF) + chr(oldaddr) + chr(newaddr))

    #################################################################################
    def send(self,buf):
        #print "sending:", repr(buf)
        self.ser.write( buf )

def get_char_num(x):
    """
    Convert signed integer to number in range 0 - 256
    """
    return int((256+x)%256)


    
