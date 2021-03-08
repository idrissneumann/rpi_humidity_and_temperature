import Adafruit_DHT


def read_humidity_and_temperature(input_pin):
    return Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, input_pin)


def read_humidity(input_pin):
    return read_humidity_and_temperature(input_pin)[0]


def read_temperature(input_pin):
    return read_humidity_and_temperature(input_pin)[1]
