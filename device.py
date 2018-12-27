import win32com.client


class Device(object):
    def __init__(self,ip):
        self.using_oscilloscope = True
        self.read_string_value = '4.4'
        self._dso = None
        self.ip = ip

    def is_debug_mode(self):
        return False if self.using_oscilloscope else True

    def connect(self):
        if self.using_oscilloscope:
            self._dso = win32com.client.Dispatch('LeCroy.ActiveDSOCtrl.1')
            self._dso.MakeConnection('IP:%s'% self.ip)


    def disconnect(self):
        if self._dso:
            self._dso.Disconnect()

    def write_string(self, command, eoi):
        if self.using_oscilloscope:
            self._dso.WriteString(command, eoi)
        else:
            print '    WriteString("%s", %d)' % (command, eoi)

    def read_string(self):
        if self.using_oscilloscope:
            result = self._dso.ReadString(256)
            return result
        else:
            print '    ReadString() return %s' % self.read_string_value
            return self.read_string_value

    def get_name(self):
        if self.using_oscilloscope:
            result = self._dso.ReadString(256)
            return result
        else:
            return 'debug_name'

    def get_sn(self):
        if self.using_oscilloscope:
            result = self._dso.ReadString(256)
            return result
        else:
            return 'debug_sn'

    def test_set_read_string_value(self, value):
        self.read_string_value = value
