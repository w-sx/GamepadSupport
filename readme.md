# Gamepad Support Add-on

This add-on provides NVDA with support for **XInput-compatible gamepads** (such as Xbox controllers, mainstream PC gamepads, etc.). With this add-on, users can map gamepad buttons to NVDA commands or keyboard shortcuts, enabling one-handed computer operation via a controller.

## General Information

* **Add-on Name**: Gamepad Support
* **Author**: Shunxian Wu <PurrHare@outlook.com>
* **Tested Version**: NVDA 2026.1
* **License**: GPL v3
* **Official Website**: [NVDA Chinese Community](https://www.nvdacn.com/)
* **Repository**: [GitHub Repository](https://github.com/w-sx/GamepadSupport)

---

## Features

* **XInput Integration**: Based on the XInput 1.4 standard, offering high compatibility and ultra-low latency.
* **Full Button Recognition**:
    * **D-Pad**: Up, Down, Left, Right.
    * **Action Buttons**: A, B, X, Y.
    * **Shoulder Buttons**: LB, RB.
    * **Thumbstick Clicks**: L_Thumb (Left stick click), R_Thumb (Right stick click).
    * **Menu Buttons**: Start, Back.
    * **Thumbstick Direction**: Left and right analog sticks — push Up/Down/Left/Right to trigger independent gestures, with auto-repeat while held.
* **Smart Trigger Detection**: Simulates LT and RT linear triggers as standard binary buttons. Includes pressure threshold logic to prevent accidental triggers.
* **Native Gesture Support**: All gamepad inputs are registered as standard NVDA "gestures," allowing flexible configuration just like keyboard shortcuts.
* **Performance Optimization**:
    * **Active Mode**: Polls at 100Hz when a gamepad is connected for responsive input.
    * **Idle Mode**: Automatically switches to a 5-second low-frequency scan when disconnected to save CPU resources.

---

## User Guide

After installing the add-on and connecting your gamepad:

1.  Press `NVDA + 1` to turn on **Input Help** and test if gamepad button presses are announced correctly.
2.  Open the **NVDA Menu** (`NVDA + N`).
3.  Go to **Preferences (P)** -> **Input Gestures (N)...**.
4.  Select an NVDA command, click the **Add (A)** button, and then press the gamepad button you wish to bind.

---

## FAQ

**Q: Why is my gamepad not responding?**
A: Please ensure your gamepad supports XInput mode (standard on most modern PC controllers). You can check the NVDA log; if it shows "Gamepad connected," the device is recognized.

**Q: Why use XInput 1.4 only?**
A: This ensures compatibility with the native drivers in Windows 8 and above. If you are using an older version of Windows, you may need to update your DirectX runtime libraries.

---

## Contribution & Feedback

If you encounter bugs or have functional suggestions, please contact us via:
* Submit an issue on [GitHub Issues](https://github.com/w-sx/GamepadSupport/issues).
* Join the discussion at the Chinese community [NVDA Chinese community](https://www.nvdacn.com/).