"""
Entrypoint app file

Objective: initialize and run telemetry software pipeline
"""

from library import (
    RadioSerialIn,
    RedisDataSender,
)


def run():
    """
    Run the data pipeline
    """
    # stream = ArduinoSerialIn()
    
    stream = RadioSerialIn()
    print('testing...')
    parser = RedisDataSender(stream)
    parser.grab_serial_data()


if __name__ == "__main__":
    run()