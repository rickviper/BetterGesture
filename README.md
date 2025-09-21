# BetterGesture

BetterGestures is a hand-gesture based control system that uses your webcam and [MediaPipe](https://developers.google.com/mediapipe) to recognize hand movements and perform system actions like **alt+tab switching, play/pause control, mouse movement, and clicking**. All without touching your keyboard or mouse.  

<br>

## ✨ Features  

### Keyboard mode  
- Switch applications with **Alt+Tab** (index finger only).  
- Play/Pause media with an open palm.  
- Easily remap gestures to other keys or key combinations (e.g., volume control, screenshots, shortcuts).  

### Mouse mode  
- Move cursor using pinch gesture: thumb + index finger (continuously).  
- Perform **left click**: thumb + middle finger pinch (once).  
- Perform **right click**: thumb + ring finger pinch (once).  
- Smooth cursor motion and click detection for stability.  

### General  
- Toggle between **Mouse Mode** and **Keyboard Mode** with the “call sign” hand gesture (thumb + pinky extended). The current mode is displayed on the tracking window. 
- Real-time display: See gesture tracking and current mode on-screen.

  <br>

## 📦 Requirements  

- Tested on **Windows**  
- Make sure you have **Python 3.12 or lower** (Mediapipe doesn’t support higher python versions).  

Install dependencies:  
```bash
pip install opencv-python mediapipe pyautogui numpy
```
⚠️ On some systems (especially Windows), you may need to install `opencv-contrib-python` instead of `opencv-python`.  

<br>

## 🚀 Installation & Usage  

1. Clone this repository:  
   ```bash
   git clone https://github.com/rickviper/BetterGesture
   cd BetterGesture
   ```
2. Run the script:
   ```bash
   python BetterGesture.py
   ```
3. Grant access to your webcam when promted.

4. Use gestures to control your system

   - Index finger only → Alt+Tab to switch windows.

   - Open palm → Play/Pause.

   - Call sign (🤙) → Switch between Mouse Mode / Keyboard Mode.

   - Pinch with index finger + thumb → Move cursor.

   - Pinch with middle finger + thumb → Left click.
 
   - Pinch with ring finger + thumb → Right click.

   - Select the tracking window and press `q` to quit.
  
     <br>

## ❔ How it works
 - Uses MediaPipe Hands to detect 21 landmarks on the hand.

 - Classifies finger positions into gestures.

 - Maps gestures to system events using PyAutoGUI.

 - Provides smoothed cursor movement & debounced clicks to reduce noise.

   <br>

## 🤝 Contributing  

Contributions are always welcome!  

BetterGestures is designed to be **easily extendable** — you can map **any key, key combination, or shortcut** to new gestures.  

- Check out the gesture detection functions in `BetterGestures.py` (like `is_pinch`, `is_call_sign`, `is_left_click`).  
- Create your own function that defines a gesture using hand landmarks.  
- Map it to a system action using **PyAutoGUI**.  

### Examples  
- Control volume → `volumeup`, `volumedown`  
- Take screenshots → `ctrl+shift+s`  
- Open apps → `win+r` → type command  

### Adding a Custom Gesture  

Here’s how you can define a new gesture and assign it to an action:  

```python
def is_thumbs_up(lm):
    #detects a thumbs up gesture.
    return lm[4].y < lm[3].y and lm[8].y > lm[6].y

#in main loop 
if is_thumbs_up(lm):
    pyautogui.press("volumeup")   # increase system volume
```
Replace `volumeup` with any key or use `pyautogui.hotkey()` for combinations, e.g.:
```python
pyautogui.hotkey("ctrl", "shift", "s")   # screenshot shortcut
```
