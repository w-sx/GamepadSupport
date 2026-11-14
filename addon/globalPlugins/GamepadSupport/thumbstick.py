import time

THRESHOLD_PRESS = 16000
THRESHOLD_RELEASE = 8000
INITIAL_DELAY = 0.5
REPEAT_INTERVAL = 0.15

class Thumbstick:
    """Report a thumbstick (x to the right, y up, both -32768..32767) as one Up/Down/Left/Right button.

    The button is reported when the stick is pushed, then again every REPEAT_INTERVAL once INITIAL_DELAY
    has passed. It is left out of the reports in between, so every report counts as a new press.
    """
    def __init__(self, name):
        self._name = name
        self._held = None
        self._next_repeat = 0

    def read(self, x, y):
        values = {"Up": y, "Down": -y, "Left": -x, "Right": x}
        previous = self._held
        # pressed above THRESHOLD_PRESS, kept until below THRESHOLD_RELEASE, only the dominant direction counts
        if previous is None or values[previous] < THRESHOLD_RELEASE:
            direction = max(values, key=values.get)
            self._held = direction if values[direction] > THRESHOLD_PRESS else None
        now = time.monotonic()
        if self._held is None:
            return set()
        if self._held != previous:
            self._next_repeat = now + INITIAL_DELAY
        elif now >= self._next_repeat:
            self._next_repeat = now + REPEAT_INTERVAL
        else:
            return set()
        return {f"{self._name}_{self._held}"}