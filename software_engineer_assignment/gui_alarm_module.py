"""
    File name: gui_alarm_module.py
    Date: 02.01.2023
    Desc: gui_alarm_module.py
"""

import datetime


class Alarm:
    """
    Alarm class used for controlling and filtering the input alarm variable.

    Args:
        alarm_name(str): Name of the alarm
        inverted(bool): Alarm polarity; default False
        trigger_mode(str): rising - rising edge trigger, falling - falling edge trigger,
        state - trigger when state high

    Attributes:
        alarm_name(str): Name of the alarm
        alarm_out(int): output of the alarm
        _inverted(bool): Alarm polarity; default False
        _trigger_mode(str): rising - rising edge trigger, falling - falling edge trigger,
        state - trigger when state high
        _input_current_value(int): Current input of the alarm
    """
    def __init__(self, alarm_name, inverted=False, trigger_mode="state"):
        self.alarm_name = alarm_name
        self.alarm_out = 0

        self._trigger_mode = trigger_mode
        self._inverted = inverted
        self._input_current_value = 0

    def monitor_alarm(self, input_val: int):
        """
        Monitor input of the alarm and return alarm output value
        according the configuration (rising edge, inverted...)
        args: input_val(int) - input alarm
        return: output "filtered" alarm value according the configuration
        """
        alarm_out = 0

        # Invert input
        if self._inverted:
            if input_val == 1:
                value = 0
            else:
                value = 1
        else:
            value = input_val

        # Alarm triggers
        if self._trigger_mode == "rising":   # Rising edge alarm
            if value == 1 and self._input_current_value == 0:
                alarm_out = 1
        elif self._trigger_mode == "falling":  # Falling edge alarm
            if value == 0 and self._input_current_value == 1:
                alarm_out = 1
        else:
            if value == 1:
                alarm_out = 1

        self._input_current_value = value
        self.alarm_out = alarm_out

        return alarm_out


class AlarmLogger:
    """
    Alarm Logger class for logging the input alarms

    Args:
        log_path(str): Path to the alarm log file

    Attributes:
        log_file_path(str): Path to the alarm log file
    """
    def __init__(self, log_path: str):
        self.log_file_path = log_path

    def log_alarm(self, alarm: Alarm):
        """
        Logs input alarm into the file
        args: Alarm(Alarm) - input alarm
        return: /
        """
        if alarm.alarm_out == 1:
            try:
                with open(self.log_file_path, 'a') as file:
                    alm_str = f"{alarm.alarm_name} @ {datetime.datetime.now()}\n"
                    file.write(alm_str)
            except FileNotFoundError:
                print("Log file not found")
