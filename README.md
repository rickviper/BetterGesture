
# BetterGesture

BetterGestures is a hand-gesture based control system that uses your webcam and MediaPipe
 to recognize hand movements and perform system actions like alt+tab switching, play/pause control, mouse movement, and clicking — all without touching your keyboard or mouse.


## Features
<ul>
 <li>#### Keyboard mode:</li>

- Switch applications with Alt+Tab (index finger only).

- Play/Pause media with an open palm.
- Easily remap gestures to other keys or key combinations (e.g., volume control, screenshots, shortcuts).

<li>#### Mouse mode:</li>

- Move cursor using hand position.

- Perform left click (thumb + middle finger pinch).

- Perform right click (thumb + ring finger pinch).

- Smooth cursor motion and click detection for stability.

<li>Toggle between Mouse Mode and Keyboard Mode with the “call-sign” hand gesture (thumb + pinky extended).</li>

<li>Real-time display: See gesture tracking and current mode on-screen.</li>
</ul>

## Requirements

Tested on Windows

Make sure you have python 3.12 or lower (Mediapipe doesn't support higher python versions)

Install dependencies:

```python
pip install opencv-python mediapipe pyautogui numpy

```
⚠️ On some systems (especially Windows), you may need to install ```opencv-contrib-python``` instead of ```opencv-python```.


## Installation & Usage

1) Clone this repository

```bash
git clone https://github.com/rickviper/BetterGesture
cd BetterGesture

```
2) Run the script

```bash
python BetterGesture.py

```

3) Grant access to your webcam when prompted.

#### Use gestures to control your system:

- Index finger only → Alt+Tab to switch windows.

- Open palm → Play/Pause.

- Call sign (🤙) → Switch between Mouse Mode / Keyboard Mode.

- Pinch with index finger + thumb → Move cursor.

- Pinch with middle finger + thumb → Left click.

- Pinch with ring finger + thumb → Right click.

- Press q to quit.
## How it works

- Uses MediaPipe Hands to detect 21 landmarks on the hand.

- Classifies finger positions into gestures.

- Maps gestures to system events using PyAutoGUI.

- Provides smoothed cursor movement & debounced clicks to reduce noise.


## Contributing

Contributions are always welcome!

- One of the best parts of BetterGestures is that you can easily extend it with your own gestures (keys, shortcuts everything can be mapped to gestures)!

- Look at the finger_status and gesture detection functions inside BetterGestures.py (like ```is_pinch```, ```is_call_sign```, ```is_left_click```).

- Map your gesture to any keyboard key, key combination, or mouse action using PyAutoGUI.

- Examples:
<ul>
 <li></li>Control volume (```volumeup```, ```volumedown```).</li>

 <li>Take screenshots (```ctrl+shift+s```).</li>

 <li>Open apps (```win+r``` → type command).</li>
 </ul>


- Submit a pull request to share your gesture with the community

- Submit a pull request to share your gesture with the community

