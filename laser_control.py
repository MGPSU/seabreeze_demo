import usb
import os


class Laser:
    def __init__(self):
        self.name = None
        self.port = None
        self.pulseMode = None
        self.repRate = None
        self.burstCount = None
        self.diodeCurrent = None
        self.energyMode = None
        self.pulseWidth = None
        self.diodeTrigger = None
        self.autoArm = False

    def __send_command(self):
        pass

    def fire_laser(self):
        pass

    def get_status(self):
        pass

    def arm(self):
        pass

    def disarm(self):
        pass

    def update_settings(self):
        # cmd format, ignore brackets => ;[Address]:[Command String][Parameters]<CR>
        cmd_strings = list()

        cmd_strings.append(';LA:PM ' + str(self.pulseMode) + '<CR>')
        cmd_strings.append(';LA:RR ' + str(self.repRate) + '<CR>')
        cmd_strings.append(';LA:BC ' + str(self.pulseMode) + '<CR>')
        cmd_strings.append(';LA:DC ' + str(self.diodeCurrent) + '<CR>')
        cmd_strings.append(';LA:EM ' + str(self.energyMode) + '<CR>')
        cmd_strings.append(';LA:PM ' + str(self.pulseMode) + '<CR>')
        cmd_strings.append(';LA:DW ' + str(self.pulseWidth) + '<CR>')
        cmd_strings.append(';LA:DT ' + str(self.pulseMode) + '<CR>')

        return cmd_strings
