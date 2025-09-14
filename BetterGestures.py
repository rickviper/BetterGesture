import cv2
import mediapipe as mp
import pyautogui
import time
import numpy as np
import sys
import math

cv2.destroyAllWindows()

# mediapipe stuff
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.8)

# for webcam
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

# mapping screen size
screen_w, screen_h = pyautogui.size()

alt_pressed = False
last_tab_time = 0
tab_interval = 1.0   # alt+tap press interval

# Gesture state
last_gesture = None
last_gesture_time = 0
gesture_cooldown = 1.0  # interval between play/pause

# pinch state
pinch_active = False
last_pinch_time = 0
pinch_click_cooldown = 1.0  

mouse_mode = False
last_mode_switch = 0
mode_switch_cooldown = 1.5  

def finger_status(landmarks):
    # from joint to tip
    fingers = []
    fingers.append(landmarks[4].x < landmarks[3].x)     # thumb
    fingers.append(landmarks[8].y < landmarks[6].y)     # index
    fingers.append(landmarks[12].y < landmarks[10].y)   # middle
    fingers.append(landmarks[16].y < landmarks[14].y)   # ring
    fingers.append(landmarks[20].y < landmarks[18].y)   # pinky ponky
    return fingers

def classify_gesture(fingers):
    if fingers[1] and not any(fingers[i] for i in [0,2,3,4]):
        return "alt_tab"       # index only
    elif all(fingers):
        return "play_pause"    # open palm
    else:
        return None
    

def is_pinch(lm, threshold=0.05):
    x1, y1 = lm[4].x, lm[4].y
    x2, y2 = lm[8].x, lm[8].y
    dist = math.hypot(x2-x1, y2-y1)
    return dist < threshold

def is_call_sign(lm):
    fingers = finger_status(lm)
    return fingers[0] and fingers[4] and not fingers[1] and not fingers[2] and not fingers[3]

def is_pinch_grab(lm, threshold=0.05):
    x1, y1 = lm[4].x, lm[4].y
    x2, y2 = lm[8].x, lm[8].y
    return math.hypot(x2-x1, y2-y1) < threshold

def is_left_click(lm, threshold=0.05):
    x1, y1 = lm[4].x, lm[4].y
    x2, y2 = lm[12].x, lm[12].y
    return math.hypot(x2-x1, y2-y1) < threshold

def is_right_click(lm, threshold=0.05):
    x1, y1 = lm[4].x, lm[4].y
    x2, y2 = lm[16].x, lm[16].y
    return math.hypot(x2-x1, y2-y1) < threshold

# cursor smoothing
smooth_x, smooth_y = pyautogui.position()  # current cursor position
smoothing_factor = 0.2   # smaller = smoother, larger = more responsive

# click smoothing
left_click_frames = 0
right_click_frames = 0
click_frame_threshold = 3  # frames required to register click



try:
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hands.process(rgb)

        if result.multi_hand_landmarks:
            for hand_landmarks in result.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                lm = hand_landmarks.landmark
                current_time = time.time()

                # mode switching
                if is_call_sign(lm) and current_time - last_mode_switch > mode_switch_cooldown:
                    mouse_mode = not mouse_mode
                    last_mode_switch = current_time

                if mouse_mode:
                    ix, iy = lm[8].x, lm[8].y
                    screen_x = np.interp(ix, [0, 1], [0, screen_w])
                    screen_y = np.interp(iy, [0, 1], [0, screen_h])

                    if is_pinch_grab(lm):
                        smooth_x = smooth_x * (1 - smoothing_factor) + screen_x * smoothing_factor
                        smooth_y = smooth_y * (1 - smoothing_factor) + screen_y * smoothing_factor
                        pyautogui.moveTo(smooth_x, smooth_y)

                    
                    # left click smoothing
                    if is_left_click(lm):
                        left_click_frames += 1
                    if left_click_frames >= click_frame_threshold and current_time - last_pinch_time > pinch_click_cooldown:
                        pyautogui.click(button="left")
                        print("Left click")
                        last_pinch_time = current_time
                        left_click_frames = 0  # reset counter after click
                    else:
                        left_click_frames = 0  # reset if fingers apart

                    # smoothing for right click
                    if is_right_click(lm):
                        right_click_frames += 1
                    if right_click_frames >= click_frame_threshold and current_time - last_pinch_time > pinch_click_cooldown:
                        pyautogui.click(button="right")
                        print("Right click")
                        last_pinch_time = current_time
                        right_click_frames = 0  # reset counter after click
                    else:
                        right_click_frames = 0  # reset if fingers apart


                else:
                    fingers = finger_status(lm)
                    gesture = classify_gesture(fingers)

                    # for switching windows
                    if gesture == "alt_tab":
                        if not alt_pressed:
                            pyautogui.keyDown('alt')
                            alt_pressed = True
                        if current_time - last_tab_time > tab_interval:
                            pyautogui.press('tab')
                            last_tab_time = current_time
                    else:
                        if alt_pressed:
                            pyautogui.keyUp('alt')
                            alt_pressed = False

                    # for play/pause
                    if gesture and (gesture != last_gesture or current_time - last_gesture_time > gesture_cooldown):
                        if gesture == "play_pause":
                            pyautogui.press('space')
                            print("Play/Pause triggered")
                        last_gesture = gesture
                        last_gesture_time = current_time

        # tacking screen display
        mode_text = "Mouse Mode" if mouse_mode else "Keyboard Mode"
        cv2.putText(frame, mode_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 
                    1, (0, 255, 0) if mouse_mode else (255, 0, 0), 2)

        cv2.imshow("Gesture Control", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

except KeyboardInterrupt:
    print("Execution interrupted by user")

finally:
    cap.release()
    cv2.destroyAllWindows()
    if alt_pressed:
        pyautogui.keyUp('alt')
    print("Resources released.")
    sys.exit(0)

