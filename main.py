import network
import socket
from time import sleep
import machine
from machine import Timer
from umqtt.simple import MQTTClient

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

def connect_to_mqtt():
    """
    Function that connects u to MQTT Broker
    """
    client = MQTTClient(
        client_id=b"pavel_pico_w",
        server="pavel-vacha.cz",
        port=0,
        user="",
        password="",
        keepalive=7200
    )
    client.connect()
    return client

def msg_callback(topic, response):
    """
    Sem chodí ty zprávy z MQTT Brokera
    """
    print("Received message on topic:", topic)
    print("Response:", response)

def interruption_handler(timer):
    client.check_msg()
    
ip = connect_to_wifi("Vila Harcov", "harcov27235788")
print(f'Connected on {ip}')


client = connect_to_mqtt()
client.set_callback(msg_callback)
client.subscribe("gnss")

# Každých 100 milisekund se vygeneruje přerušení
# Efektivnější než while True loop
soft_timer = Timer(mode=Timer.PERIODIC, period=100, callback=interruption_handler)

#import mip
#mip.install("umqtt.simple")
