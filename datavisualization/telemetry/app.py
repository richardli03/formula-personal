"""
Entrypoint app file

Objective: initialize and run telemetry software pipeline
"""

from library import (
    RadioSerialIn,
    LogFile,
    RedisDataSender,
)


def run():
    """
    Run the data pipeline
    """
    stream = LogFile("decoded_can.txt", ["brake_analog_voltage_msb", "brake_analog_voltage_lsb", "cf", "bspdsense", "tsmssense", "left_e_stop_sense", "glvmssense"])
    # stream = RadioSerialIn("___")
    print('testing...')
    parser = RedisDataSender(stream)
    parser.grab_serial_data()


if __name__ == "__main__":
    run()