import espnow as ESPNow

class Display(object):
    """Display"""

    def __init__(self, display_mac_address, system_data):
        self._system_data = system_data

        self._espnow = ESPNow.ESPNow()
        peer = ESPNow.Peer(mac=bytes(display_mac_address), channel=0)
        self._espnow.peers.append(peer)

    def update(self):
        try:
            brakes_are_active = 1 if self._system_data.brakes_are_active else 0
            self._espnow.send(f"{int(self._system_data.battery_voltage_x10)} {int(self._system_data.battery_current_x100)} {int(self._system_data.motor_current_x100)} {self._system_data.motor_speed_erpm} {brakes_are_active}")
            print("ok tx display")
        except:
            pass
