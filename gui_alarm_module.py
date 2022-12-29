
class Alarm:
    def __init__(self, alarm_name, inverted=False, trigger_mode="state"):
        self.alarm_name = alarm_name
        self.alarm_value = 0

        self._trigger_mode = trigger_mode
        self._inverted = inverted
        self._input_current_value = 0

    def monitor_alarm(self, input_val):

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
        self.alarm_value = alarm_out

        return alarm_out

