# Example using panel_com

from panel_com import PanelCom
import time

# Create a PanelCom object
controller = PanelCom('COM5')
controller.set_pattern_id(1)
controller.ident_compression_off()
controller.set_mode(4, 4)
controller.set_gain_bias(0, 0, 0, 0)

# Make dummy sequence of 1 to 1000
sequence = [i for i in range(1, 1001)]

# Send function of all ones
for i in range(20):
    j = 1 + i * 50;
    k = j + 49;

    controller.send_function(True, i, sequence[j : k])
    controller.send_function(False, i, sequence[j : k])
    
    time.sleep(0.1)
