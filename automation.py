
import uinput
import time
import evdev
device = evdev.InputDevice('/dev/input/event1')
print(device)
#
# device = uinput.Device([
#         uinput.BTN_LEFT,
#         uinput.BTN_RIGHT,
#         uinput.REL_X,
#         uinput.REL_Y,
#         ])
# time.sleep(1)
#
# for i in range(20):
#     time.sleep(0.01)
#     device.emit(uinput.REL_Y, 5)