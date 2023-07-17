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
    v1.0 (7/17/2023): Revised by Nobel Zhou for Generation 2 displays (nxz157@case.edu)
"""

import serial
from typing import List

class PanelCom:
    def __init__(self, port, baudrate=19200):
        self.ser = serial.Serial(port=port, baudrate=baudrate, timeout=None)
    
    def __del__(self):
        self.ser.close()

    # 1 byte commands
    def start(self):
        self._send_serial(chr(0x01) + chr(0x20))

    def stop(self):
        self._send_serial(chr(0x01) + chr(0x30))

    def start_w_trig(self):
        self._send_serial(chr(0x01) + chr(0x25))
        
    def stop_w_trig(self):
        self._send_serial(chr(0x01) + chr(0x35))
    
    def clear(self):
        self._send_serial(chr(0x01) + chr(0xF0))

    def all_off(self):
        self._send_serial(chr(0x01) + chr(0x00))
        
    def all_on(self):
        self._send_serial(chr(0x01) + chr(0xFF))
    
    def g_level(self, level: int):
        if level < 0 or level > 7:
            raise ValueError('Level must be between 0 and 7')
        self._send_serial(chr(0x01) + chr(0x40 + level))
    
    def led_toggle(self):
        self._send_serial(chr(0x01) + chr(0x50))

    def reset_controller(self):
        self._send_serial(chr(0x01) + chr(0x60))

    def bench_pattern(self):
        self._send_serial(chr(0x01) + chr(0x70))

    def laser_on(self):
        self._send_serial(chr(0x01) + chr(0x10))

    def laser_off(self):
        self._send_serial(chr(0x01) + chr(0x11))

    def ident_compression_on(self):
        self._send_serial(chr(0x01) + chr(0x12))   

    def ident_compression_on(self):
        self._send_serial(chr(0x01) + chr(0x13))  

    # 2 byte commands
    def reset_panel(self, panel_addr: int):
        if panel_addr < 0 or panel_addr > 127:
            raise ValueError('Panel address must be between 1 and 127, or 0 for all panels')
        self._send_serial(chr(0x02) + chr(0x01) + chr(panel_addr))
    
    def display_panel_addr(self, panel_addr: int):
        if panel_addr < 0 or panel_addr > 127:
            raise ValueError('Panel address must be between 1 and 127, or 0 for all panels')
        self._send_serial(chr(0x02) + chr(0x02) + chr(panel_addr))
    
    def set_pattern_id(self, pattern_id: int):
        if pattern_id < 1 or pattern_id > 99:
            raise ValueError('Pattern ID must be between 1 and 99')
        self._send_serial(chr(0x02) + chr(0x03) + chr(pattern_id))

    def adc_test(self, channel: int):
        if channel < 0 or channel > 7:
            raise ValueError('ADC Channel must be between 0 and 7')
        self._send_serial(chr(0x02) + chr(0x04) + chr(channel))

    def dio_test(self, channel: int):
        if channel < 0 or channel > 7:
            raise ValueError('DIO Channel must be between 0 and 7')
        self._send_serial(chr(0x02) + chr(0x05) + chr(channel))
    
    def set_trigger_rate(self, rate: int):
        if rate < 0 or rate > 255:
            raise ValueError('Trigger rate must be between 0 and 255')
        self._send_serial(chr(0x02) + chr(0x06) + chr(rate))
    
    # 3 byte commands
    def set_mode(self, x_mode: int, y_mode: int):
        self._send_serial(chr(0x03) + chr(0x10) + chr(x_mode) + chr(y_mode))
    
    def change_address(self, old_addr: int, new_addr: int):
        if old_addr < 0 or old_addr > 127 or new_addr < 0 or new_addr > 127:
            raise ValueError('Panel address must be between 1 and 127, or 0 for all panels')
        self._send_serial(chr(0x03) + chr(0xFF) + chr(old_addr) + chr(new_addr))
    
    # 5 byte commands
    def set_position(self, x_pos: int, y_pos: int):
        if x_pos < 0 or y_pos < 0:
            raise ValueError('Position indices must be non-negative numbers')
        self._send_serial(chr(0x05) + chr(0x70) + PanelCom._dec_to_char(x_pos, 2) + PanelCom._dec_to_char(y_pos, 2))
    
    def set_gain_bias(self, x_gain: int, x_bias: int, y_gain: int, y_bias: int):
        self._send_serial(chr(0x05) + chr(0x71) + PanelCom._signed_bytes_to_chars([x_gain, x_bias, y_gain, y_bias]))

    # longer functions
    def send_function(self, is_x: bool, segment_num: int, function: List[int]):
        self._send_serial(chr(52) + chr(1 if is_x else 2) + chr(segment_num) +  PanelCom._signed_bytes_to_chars(function))

    # private methods
    def _send_serial(self, to_write: str):
        self.ser.write(list(map(ord, list(to_write))))
    
    # static methods
    @staticmethod
    def _dec_to_char(num: int, num_chars: int) -> str:
        if num > 2 ** (8 * num_chars):
            raise ValueError('Number is too large to fit in specified number of chars')
        elif num < 0:
            raise ValueError('Number must be positive')
        
        return ''.join([chr(num >> (8 * i)) for i in range(0, num_chars, 1)])
    
    @staticmethod
    def _signed_bytes_to_chars(bytes: List[int]) -> str:
        return ''.join([chr((b % 256 + 256) % 256) for b in bytes])
    