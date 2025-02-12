import espnow as ESPNow

cccounter_a = 0

class Display(object):
    """Display"""

    def __init__(self, display_mac_address, system_data):
        self._system_data = system_data
        self.message_id = 1 # motor board ESPNow message ID

        self._espnow = ESPNow.ESPNow()
        peer = ESPNow.Peer(mac=bytes(display_mac_address), channel=1)
        self._espnow.peers.append(peer)

    def process_data(self):
        try:
            data = self._espnow.read()
            if data is not None:
                data = [n for n in data.msg.split()]
                # only process packages for us
                if int(data[0]) == self.message_id:
                    self._system_data.motor_enable_state = True if int(data[1]) != 0 else False
        except:
            pass

    def update(self):
        try:
            brakes_are_active = 1 if self._system_data.brakes_are_active else 0
            self._espnow.send(f"{int(self._system_data.battery_voltage_x10)} {int(self._system_data.battery_current_x100)} {int(self._system_data.motor_current_x100)} {self._system_data.motor_speed_erpm} {brakes_are_active}")
        except:
            pass
