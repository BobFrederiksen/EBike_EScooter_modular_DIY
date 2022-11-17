import board
import digitalio
from digitalio import Pull
import analogio
import busio
import asyncio
import simpleio

import vesc

# configure NRF52840 board green LED
led = digitalio.DigitalInOut(board.LED1)
led.direction = digitalio.Direction.OUTPUT

# init VESC object
vesc = vesc.VESC(board.P0_20, board.P0_22)

# configure UART for communications with display
uart_display = busio.UART(board.P0_09, board.P0_10, baudrate = 19200)

# configure ADC input for throttle signal
adc_throttle = analogio.AnalogIn(board.P0_29)

# configure IO input for brake sensor signal
io_brake_sensor = digitalio.DigitalInOut(board.P0_02)
io_brake_sensor.pull = Pull.UP
io_brake_sensor.direction = digitalio.Direction.INPUT

# configure IO input for wheel speed sensor signal
io_wheelspeed_sensor = digitalio.DigitalInOut(board.P1_15)
io_wheelspeed_sensor.pull = Pull.UP
io_wheelspeed_sensor.direction = digitalio.Direction.INPUT

async def vesc_heartbeat():
    while True:
        vesc.send_heart_beat()
        await asyncio.sleep(0.75)

async def read_sensors_control_motor():
    while True:

        # read throttle and map the value to motor speed value
        min_throttle_adc = 18000 # checked on my current hardware
        max_throttle_adc = 65535 # max value of analogio.AnalogIn
        min_motor_speed_erpm = 0
        max_motor_speed_erpm = 8500 # max value of the motor speed ERPM
        motor_speed_erpm = simpleio.map_range(adc_throttle.value, min_throttle_adc, max_throttle_adc, min_motor_speed_erpm, max_motor_speed_erpm)

        print(motor_speed_erpm)

        await asyncio.sleep(0.5)

        # set motor current

        # set motor speed

        # await asyncio.sleep(0.002)

async def main():
    vesc_heartbeat_task = asyncio.create_task(vesc_heartbeat())
    read_sensors_control_motor_task = asyncio.create_task(read_sensors_control_motor())
    await asyncio.gather(vesc_heartbeat_task, read_sensors_control_motor_task)
    print("done main()")

asyncio.run(main())
