import threading
import time
import inputCore
import globalPluginHandler
import queueHandler
import addonHandler
from logHandler import log
from .xinput import XInput
from .joystick import Joystick

addonHandler.initTranslation()

# Gamepad backends, the first one that finds a gamepad is used
BACKENDS = (XInput, Joystick)

class GamepadGesture(inputCore.InputGesture):
    shouldPreventSystemIdle = True
    def __init__(self, button_name):
        self.button_name = button_name
        super().__init__()
    def _get_identifiers(self): return [f"gp:{self.button_name.lower()}"]
    @classmethod
    def getDisplayTextForIdentifier(cls,identifier): return _("Gamepad Controller"), identifier.split(':')[1]
    def _get_displayName(self): return _("Gamepad") + f" {self.button_name}"

inputCore.registerGestureSource("gp", GamepadGesture)

class GlobalPlugin(globalPluginHandler.GlobalPlugin):
    def __init__(self):
        super().__init__()
        self._terminate = False
        self._backends = []
        self.hasGamepad = False
        for backend in BACKENDS:
            try:
                self._backends.append(backend())
            except Exception:
                log.error(f"{backend.__name__} backend not available.", exc_info=True)
        self._thread = threading.Thread(target=self._run_poll, name="gamepad_poll")
        self._thread.daemon = True
        self._thread.start()

    def _read(self):
        for backend in self._backends:
            pressed = backend.read()
            if pressed is not None:
                return pressed

    def _run_poll(self):
        last = set()

        while not self._terminate:
            try:
                pressed = self._read()
                if pressed is not None:
                    if not self.hasGamepad:
                        self.hasGamepad = True
                        log.info("Gamepad connected")
                    for name in pressed - last:
                        self._trigger_gesture(name)
                    last = pressed
                    time.sleep(0.01) # 100Hz
                else:
                    if self.hasGamepad:
                        self.hasGamepad = False
                        log.info("Gamepad disconnected")
                    last = set()
                    # We did not find gamepad, have a good rest
                    time.sleep(5)
            except Exception:
                log.debugWarning("Gamepad poll cycle failed", exc_info=True)
                time.sleep(2)

    def _trigger_gesture(self, button_name):
        try:
            gesture = GamepadGesture(button_name)
            queueHandler.queueFunction(
                queueHandler.eventQueue, 
                inputCore.manager.executeGesture, 
                gesture
            )
        except Exception as e:
            log.error(f"Gamepad gesture execution failed: {e}")

    def terminate(self):
        self._terminate = True
        super().terminate()