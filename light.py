#!/usr/bin/env python3
from time import sleep
from random import randrange as rand
from threading import Thread
import sys

# todo: create a device finder
devpath = '/dev/hidraw0'

colors = {
    'red': 0x01,
    'green': 0x02,
    'blue': 0x03,
    'cyan': 0x06,
    'magenta': 0x05,
    'yellow': 0x04,
    'black': 0x08,
    'white': 0x07
}

chsum = lambda b0, b1, b3: (21 * b0 ** 2 + 19 * b1 - 3 * b3) % 255

def bg(f, *args):
    t = Thread(target=f, args=args)
    t.start()

def turn_on(color='white', delay=0.0):
    sleep(delay)
    cmd = bytearray.fromhex('ff' * 64)
    cmd[0] = 0x11
    cmd[1] = colors[color]
    cmd[3] = rand(255)
    cmd[2] = chsum(cmd[0], cmd[1], cmd[3])
    with open(devpath, 'wb') as device:
        device.write(bytes(cmd))  # ensure we're writing bytes, not a string

def turn_off(delay=0.0):
    turn_on('black', delay)

def blink(color, count=1, delay=0.2):
    for i in range(count):
        turn_on(color, delay)
        turn_off(delay)
    turn_off()

def gay():
    while True:  # Нескінченний цикл
        for c in ['red', 'green', 'blue', 'cyan', 'magenta', 'yellow']:
            turn_on(c, 0.1)
            sleep(0.1)  # Можна регулювати час між кольорами
        turn_off(0.2)
        sleep(0.5)  # Можна додавати час затримки між циклами

def static_color(color):
    turn_on(color)  # Включаємо статичний колір на постійно

if __name__ == '__main__':
    try:
        # Перевіряємо, чи є достатньо аргументів
        if len(sys.argv) >= 3:
            col, cnt = sys.argv[1], int(sys.argv[2])
            bg(blink, col, cnt)
        elif len(sys.argv) == 2 and sys.argv[1] == 'gay':  # Якщо передано 'gay' як аргумент
            bg(gay)  # Запускаємо функцію gay() у окремому потоці
        elif len(sys.argv) == 2 and sys.argv[1] in colors:  # Якщо передано колір як аргумент
            color = sys.argv[1]
            static_color(color)  # Включаємо статичний колір
        else:
            col, cnt = 'white', 1  # Значення за замовчуванням
            bg(blink, col, cnt)
    except Exception as e:
        print(f"Error: {e}")
        bg(blink, "white", 1)  # За замовчуванням використовуємо білий колір та один блимання

