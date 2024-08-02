import sys
import os

export_path = "/sys/class/pwm/pwmchip0/export" # regist pwm pin path
unexport_path = "/sys/class/pwm/pwmchip0/unexport" # unregist pwm pin path

channel_path = "/sys/class/pwm/pwmchip0/pwm{}" # pwm channel path
enable_path = "/sys/class/pwm/pwmchip0/pwm{}/enable" # pwm signal enable path
period_path = "/sys/class/pwm/pwmchip0/pwm{}/period" # set period of pulse cycle time path
cycle_path = "/sys/class/pwm/pwmchip0/pwm{}/duty_cycle" # set high signal time in pulse cycle path
polarity_path = "/sys/class/pwm/pwmchip0/pwm{}/polarity" # set polarity of pwm signal path

# check path existence to confirm channel is regist
def is_exported(channel):
    return os.path.exists(channel_path.format(channel))

# regist channel
def export(channel):
    if(not is_exported(channel)):
        try:
            with open(export_path, 'w') as export_file:
                export_file.write(str(channel))
        except IOError as e:
            print(f"Error : PWm {channel} Exporting : {e}")
            sys.exit(1)

# unregist channel
def unexport(channel):
    if (is_exported(channel)):
        try:
            with open(unexport_path, 'w') as unexport_file:
                unexport_file.write(str(channel))
        except IOError as e:
            print(f"Error : PWM {channel} Unexporting : {e}")
            sys.exit(1)

# enable : 1, 0
# make pwm signal on or off
def set_enable(channel, enable):
    if(is_exported(channel)):
        try:
            with open(enable_path.format(channel), 'w') as enable_file:
                enable_file.write(str(enable))
        except IOError as e:
            print(f"Error : PWM {channel} Enable Setting : {e}")
            sys.exit(1)            

# unit : ns
# set period of pwm signal's pulse. period is on + off signal's time.
def set_period_ns(channel, period):
    if(is_exported(channel)):
        try:
            with open(period_path.format(channel), 'w') as period_file:
                period_file.write(str(period))
        except IOError as e:
            print(f"Error : PWM {channel} Period Setting : {e}")
            sys.exit(1)

# set duty cycle of pwm signal's pulse. duty cycle is time which need to be high in one cycle of pulse.
# when duty cycle over than period of pulse, it makes error
def set_cycle_ns(channel, cycle):
    if(is_exported(channel)):
        try:
            with open(cycle_path.format(channel), 'w') as cycle_file:
                cycle_file.write(str(cycle))
        except IOError as e:
            print(f"Error : PWM {channel} Duty Cycle Setting : {e}")
            sys.exit(1)


# unit : sec
# set period of pwm signal's pulse. period is on + off signal's time.
def set_period_sec(channel, period):
    if(is_exported(channel)):
        try:
            with open(period_path.format(channel), 'w') as period_file:
                period_file.write(str(int(period)*1000000000))
        except IOError as e:
            print(f"Error : PWM {channel} Period Setting : {e}")
            sys.exit(1)

# set duty cycle of pwm signal's pulse. duty cycle is time which need to be high in one cycle of pulse.
# when duty cycle over than period of pulse, it makes error
def set_cycle_sec(channel, cycle):
    if(is_exported(channel)):
        try:
            with open(cycle_path.format(channel), 'w') as cycle_file:
                cycle_file.write(str(int(cycle) *1000000000))
        except IOError as e:
            print(f"Error : PWM {channel} Duty Cycle Setting : {e}")
            sys.exit(1)

# polarity 'normal' or 'inversed'
# set polarity of pwm signal. Inversed make signal reverse.
def set_polarity(channel, polarity):
    if(is_exported(channel)):
        try:
            with open(polarity_path.format(channel), 'w') as polarity_file:
                polarity_file.write(str(polarity))
        except IOError as e:
            print(f"Error : PWM {channel} Polarity Setting : {e}")
            sys.exit(1)