from ..Library.Module import L293D_Library as l293d
import time

in1 = 121
in2 = 117
channel = 2

if __name__ == "__main__":
    # regist device
    l293d.set_device(in1, in2, channel)
    # motor forward (5s)
    l293d.motor_control(in1, in2, "forward", channel)
    time.sleep(5)
    # stop (2s)
    l293d.motor_control(in1, in2, "stop", channel)
    time.sleep(2)
    # motor backward (5s)
    l293d.motor_control(in1, in2, "backward", channel)
    time.sleep(5)
    # motor stop (2s)
    l293d.motor_control(in1, in2, "stop", channel)
    time.sleep(2)
    # unregist device
    l293d.quit_device(in1, in2, channel)