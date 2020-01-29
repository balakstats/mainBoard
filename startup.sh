#!/bin/sh
sleep 10

sudo python3 /home/pi/Zeitnehmung/mainBoard.py --led-brightness=8 --led-rows=32 --led-cols=64 --led-multiplexing=1 --led-chain=6 --led-slowdown-gpio=2
