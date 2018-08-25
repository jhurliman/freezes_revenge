from __future__ import print_function
from os.path import dirname, join

import random
import signal
import snowboydecoder
import sys


SOUNDS = [
    join(dirname(__file__), '..', 'sounds', 'freeze-is-coming.wav'),
    join(dirname(__file__), '..', 'sounds', 'the-ice-age.wav'),
    join(dirname(__file__), '..', 'sounds', 'winter-has-come-at-last.wav'),
]

interrupted = False


def signal_handler(signal, frame):
    global interrupted
    interrupted = True


def interrupt_callback():
    global interrupted
    return interrupted


def on_detected():
    print('Turning on')
    snowboydecoder.play_audio_file(random.choice(SOUNDS))
    # TODO


def off_detected():
    print('Turning off')
    # TODO


def main():
    if len(sys.argv) != 3:
        print("Error: need to specify 2 model names")
        print("Usage: python demo.py 1st.model 2nd.model")
        sys.exit(-1)

    models = sys.argv[1:]

    # capture SIGINT signal, e.g., Ctrl+C
    signal.signal(signal.SIGINT, signal_handler)

    sensitivity = [0.5]*len(models)
    detector = snowboydecoder.HotwordDetector(models, sensitivity=sensitivity)
    print('Listening... Press Ctrl+C to exit')

    detector.start(detected_callback=[on_detected, off_detected],
                   interrupt_check=interrupt_callback,
                   sleep_time=0.03)

    detector.terminate()


main()
