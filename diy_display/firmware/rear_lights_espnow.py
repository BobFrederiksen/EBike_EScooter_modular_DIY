import espnow as ESPNow

class RearLights(object):

    def __init__(self, _espnow, mac_address, system_data):
        self._system_data = system_data
        self.message_id = 8 # rear lights ESPNow messages ID

        self._espnow = _espnow
        self._peer = ESPNow.Peer(mac=bytes(mac_address), channel=1)
        
    def update(self):
        try:
            # add peer before sending the message
            self._espnow.peers.append(self._peer)

            self._espnow.send(f"{self.message_id} {int(self._system_data.rear_lights_board_pins_state)}")

            # now remove the peer
            self._espnow.peers.remove(self._peer)
        except:
            pass
