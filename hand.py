import cv2
import mediapipe as mp
import pyautogui
import numpy as np
import math
import time

prev_time = 0
pyautogui.PAUSE = 0

# Disable PyAutoGUI fail-safe to prevent exits when reaching screen corners
pyautogui.FAILSAFE = False

# Initialize MediaPipe and webcam
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    max_num_hands=2,
    model_complexity=0,
    min_detection_confidence=0.6, 
    min_tracking_confidence=0.6
    )
cap = cv2.VideoCapture(0)
# cap.set(3, 640)
# cap.set(4, 480)

# Get full screen size
screen_width, screen_height = pyautogui.size()

# Cursor state
cursor_x, cursor_y = pyautogui.position()
frozen = False

# Smaller input range (center 40% of webcam view)
input_range_x = [0.3, 0.7]
input_range_y = [0.3, 0.7]

# Gesture state
prev_left_pos = None
swipe_threshold = 80  # pixels

# Finger states
def fingers_up(hand_landmarks):
    tips_ids = [4, 8, 12, 16, 20]
    fingers = []

    # Thumb
    if hand_landmarks.landmark[tips_ids[0]].x < hand_landmarks.landmark[tips_ids[0] - 1].x:
        fingers.append(1)
    else:
        fingers.append(0)

    # Other fingers
    for id in range(1, 5):
        if hand_landmarks.landmark[tips_ids[id]].y < hand_landmarks.landmark[tips_ids[id] - 2].y:
            fingers.append(1)
        else:
            fingers.append(0)

    return fingers

smoothening = 5
prev_x, prev_y = 0, 0

# frame_skip = 2
# frame_count = 0
while True:
    success, frame = cap.read()
    if not success:
        break

    # frame_count += 1
    # if frame_count % frame_skip != 0:
    #     continue

    fps = 1/(time.time()-prev_time)
    prev_time = time.time()

    # Draw control zone
    h, w, _ = frame.shape
    cv2.rectangle(frame,
                (int(w*0.3), int(h*0.3)),
                (int(w*0.7), int(h*0.7)),
                (255,255,0),2)

    # Flip frame
    frame = cv2.flip(frame, 1)

    # Convert to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process hands
    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks and results.multi_handedness:
        for hand_landmarks, handType in zip(results.multi_hand_landmarks, results.multi_handedness):
            label = handType.classification[0].label  # 'Left' or 'Right'
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            fingers = fingers_up(hand_landmarks)

            index_tip = hand_landmarks.landmark[8]
            x, y = index_tip.x, index_tip.y

            # Clamp hand coordinates to the control zone
            x = np.clip(x, input_range_x[0], input_range_x[1])
            y = np.clip(y, input_range_y[0], input_range_y[1])

            mapped_x = int(np.interp(x, input_range_x, [0, screen_width]))
            mapped_y = int(np.interp(y, input_range_y, [0, screen_height]))

            # Handle right hand: cursor control
            if label == 'Right':
                if sum(fingers) == 0:
                    frozen = True
                    cv2.putText(frame, "Cursor Paused (Fist)", (30, 100),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                elif fingers[1] == 1 and sum(fingers) == 1:
                    frozen = False

                if not frozen:
                    # alpha = 0.2
                    # cursor_x = alpha * mapped_x + (1-alpha) * prev_x
                    # cursor_y = alpha * mapped_y + (1-alpha) * prev_y

                    cursor_x = prev_x + (mapped_x - prev_x) / smoothening
                    cursor_y = prev_y + (mapped_y - prev_y) / smoothening
                    prev_x, prev_y = cursor_x, cursor_y

                # Move the cursor to last known position, within bounds
                safe_x = max(1, min(cursor_x, screen_width - 2))
                safe_y = max(1, min(cursor_y, screen_height - 2))
                pyautogui.moveTo(safe_x, safe_y)

            # Handle left hand: pinch click and swipe
            if label == 'Left':
                thumb_tip = hand_landmarks.landmark[4]
                index_x, index_y = int(index_tip.x * frame.shape[1]), int(index_tip.y * frame.shape[0])
                thumb_x, thumb_y = int(thumb_tip.x * frame.shape[1]), int(thumb_tip.y * frame.shape[0])

                # Pinch = click
                distance = math.hypot(index_x - thumb_x, index_y - thumb_y)
                if distance < 40:
                    pyautogui.click()
                    cv2.putText(frame, "CLICK", (index_x + 30, index_y),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

                # Swipe detection (index + middle fingers up)
                if fingers[1] == 1 and fingers[2] == 1:
                    current_pos = index_x
                    if prev_left_pos is not None:
                        delta = current_pos - prev_left_pos
                        if delta > swipe_threshold:
                            pyautogui.press('right')
                            cv2.putText(frame, "SWIPE RIGHT", (50, 400),
                                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
                        elif delta < -swipe_threshold:
                            pyautogui.press('left')
                            cv2.putText(frame, "SWIPE LEFT", (50, 400),
                                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
                    prev_left_pos = current_pos

    current_time = time.time()
    fps = 1 / (current_time - prev_time)
    prev_time = current_time

    cv2.putText(frame, f'FPS: {int(fps)}', (20,40),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

    cv2.imshow("Gesture Control", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()