import network
import socket
from time import sleep
import machine
from machine import Timer, Pin
from umqtt.simple import MQTTClient
import ujson
from random import random

interrupt_flag=0
IS_PUBLISHER=True

components = {
    "LED01":15,
}

pins = {}

def init_components():
    for key in components:
        pins[key] = machine.Pin(components.get(key), Pin.OUT)


def connect_to_wifi(ssid, password):
    """
    Function that connects u to WiFI
    """
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while wlan.isconnected() == False:
        print('Waiting for connection...')
        sleep(1)
    ip = wlan.ifconfig()[0]

    return ip

def connect_to_mqtt(username, password):
    """
    Function that connects u to MQTT Broker
    """
    client = MQTTClient(
        client_id=b"pico_w" + str(random()),
        server="pavel-vacha.cz",
        port=0,
        user=username,
        password=password,
        keepalive=7200
    )
    client.connect()
    return client

def msg_callback(topic, response):
    """
    Sem chodí ty zprávy z MQTT Brokera
    """
    parse_response = ujson.loads(response)
    print("Response:", parse_response)
    process_message(parse_response)

def message_button_clicked(pin):
    global interrupt_flag
    interrupt_flag=1
    
    push_message({"id":"LED01"})
    
def push_message(message):
    print("Publishuju message")
    #  ujson.dumps(message)
    client.publish("kuba",ujson.dumps(message))
    
def interruption_handler(timer):
    client.check_msg()
    
def process_message(data):
    pins.get(data.get("id")).toggle()
    
init_components()

#ip = connect_to_wifi("Vila Harcov", "harcov27235788")
ip = connect_to_wifi("Pavel - iPhone", "debil123")

print(f'Connected on {ip}')


client = connect_to_mqtt("pavel", "pavel123")
client.set_callback(msg_callback)
client.subscribe("pavel")

# Každých 100 milisekund se vygeneruje přerušení
# Efektivnější než while True loop
soft_timer = Timer(mode=Timer.PERIODIC, period=100, callback=interruption_handler)

pin = Pin(16,Pin.IN,Pin.PULL_UP)
pin.irq(trigger=Pin.IRQ_FALLING, handler=message_button_clicked)

while True:
    if interrupt_flag is 1:
        print("Interrupt has occured")
        interrupt_flag=0

#import mip
#mip.install("umqtt.simple")


