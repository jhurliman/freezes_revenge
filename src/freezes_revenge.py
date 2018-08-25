#!/usr/bin/env python2

from __future__ import print_function
from os.path import dirname, join

import random
import signal
import snowboydecoder
import sys


MODELS = [
    join(dirname(__file__), '..', 'resources', 'mr_freeze.pmdl'),
    join(dirname(__file__), '..', 'resources', 'turn_off.pmdl'),
]

SOUNDS = [
    join(dirname(__file__), '..', 'sounds', 'freeze-is-coming.wav'),
    join(dirname(__file__), '..', 'sounds', 'the-ice-age.wav'),
    join(dirname(__file__), '..', 'sounds', 'winter-has-come-at-last.wav'),
]

GPIO_PIN = 23

interrupted = False
relay = None

try:
    from gpiozero import LED
    relay = LED(GPIO_PIN)
    print('Using GPIO relay on pin {}'.format(GPIO_PIN))
except:  # noqa
    print('Skipping GPIO relay')


def signal_handler(signal, frame):
    global interrupted
    interrupted = True


def interrupt_callback():
    global interrupted
    return interrupted


def on_detected():
    print('Turning on')
    snowboydecoder.play_audio_file(random.choice(SOUNDS))
    if relay:
        relay.on()


def off_detected():
    print('Turning off')
    if relay:
        relay.off()


def main():
    # capture SIGINT signal, e.g., Ctrl+C
    signal.signal(signal.SIGINT, signal_handler)

    sensitivity = [0.5]*len(MODELS)
    detector = snowboydecoder.HotwordDetector(MODELS, sensitivity=sensitivity)
    print('Mr. Freeze is listening...')

    detector.start(detected_callback=[on_detected, off_detected],
                   interrupt_check=interrupt_callback,
                   sleep_time=0.03)

    detector.terminate()


main()
