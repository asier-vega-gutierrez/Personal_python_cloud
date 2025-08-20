import sys

class Signalhandler:
    def __init__(self, sig, frame):
        self.signal_handler(sig, frame)

    def signal_handler(sig, frame):
        sys.exit(0)