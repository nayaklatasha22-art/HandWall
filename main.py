
import cv2
import mediapipe as mp
import numpy as np
import math

# ==========================================
# 1. CAMERA SETUP
# ==========================================

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Camera could not open!")
    exit()

# ==========================================
# 2. MEDIAPIPE HAND DETECTION
# ==========================================

mp_hands = mp.solutions.hands

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    model_complexity=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

# ==========================================
# 3. CANVAS SETUP
# ==========================================

pink_canvas = None
white_canvas = None

previous_x = None
previous_y = None

smooth_x = None
smooth_y = None

is_drawing = False

# Pink neon color (BGR)
PINK = (255, 50, 220)
WHITE = (255, 255, 255)

# Thin handwriting
PINK_THICKNESS = 7
WHITE_THICKNESS = 2

# Smoothing strength
SMOOTHING = 0.35

# Pinch sensitivity
PINCH_START = 0.32
PINCH_STOP = 0.48

# ==========================================
# 4. MAIN LOOP
# ==========================================

while True:

    success, frame = cap.read()

    if not success:
        print("Camera frame not received!")
        break

    # Mirror camera
    frame = cv2.flip(frame, 1)

    height, width, _ = frame.shape

    # Create canvases
    if pink_canvas is None:

        pink_canvas = np.zeros(
            (height, width, 3),
            dtype=np.uint8
        )

        white_canvas = np.zeros(
            (height, width, 3),
            dtype=np.uint8
        )

    # Convert image
    rgb_frame = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2RGB
    )

    results = hands.process(rgb_frame)

    # ======================================
    # 5. HAND TRACKING
    # ======================================

    if results.multi_hand_landmarks:

        hand = results.multi_hand_landmarks[0]
        landmarks = hand.landmark

        # Index finger tip
        index_tip = landmarks[8]

        # Thumb tip
        thumb_tip = landmarks[4]

        # Palm landmarks
        index_base = landmarks[5]
        pinky_base = landmarks[17]

        # Finger coordinates
        x = int(index_tip.x * width)
        y = int(index_tip.y * height)

        thumb_x = int(thumb_tip.x * width)
        thumb_y = int(thumb_tip.y * height)

        # ==================================
        # 6. NORMALIZED PINCH DETECTION
        # ==================================

        pinch_distance = math.hypot(
            x - thumb_x,
            y - thumb_y
        )

        palm_size = math.hypot(
            (index_base.x - pinky_base.x) * width,
            (index_base.y - pinky_base.y) * height
        )

        if palm_size > 0:

            pinch_ratio = pinch_distance / palm_size

            # Start drawing
            if not is_drawing:

                if pinch_ratio < PINCH_START:
                    is_drawing = True

            # Stop drawing
            else:

                if pinch_ratio > PINCH_STOP:
                    is_drawing = False

        # ==================================
        # 7. SMOOTH FINGER MOVEMENT
        # ==================================

        if smooth_x is None:

            smooth_x = x
            smooth_y = y

        else:

            smooth_x = (
                SMOOTHING * x
                + (1 - SMOOTHING) * smooth_x
            )

            smooth_y = (
                SMOOTHING * y
                + (1 - SMOOTHING) * smooth_y
            )

        current_x = int(smooth_x)
        current_y = int(smooth_y)

        # ==================================
        # 8. DRAWING
        # ==================================

        if is_drawing:

            if previous_x is not None:

                # Pink neon stroke
                cv2.line(
                    pink_canvas,
                    (previous_x, previous_y),
                    (current_x, current_y),
                    PINK,
                    PINK_THICKNESS,
                    cv2.LINE_AA
                )

                # Bright inner stroke
                cv2.line(
                    white_canvas,
                    (previous_x, previous_y),
                    (current_x, current_y),
                    WHITE,
                    WHITE_THICKNESS,
                    cv2.LINE_AA
                )

            previous_x = current_x
            previous_y = current_y

        else:

            # Release = stop drawing
            previous_x = None
            previous_y = None

        # ==================================
        # 9. FINGER CURSOR
        # ==================================

        cv2.circle(
            frame,
            (current_x, current_y),
            6,
            (0, 255, 0),
            -1
        )

    else:

        # Reset when hand leaves camera
        is_drawing = False

        previous_x = None
        previous_y = None

        smooth_x = None
        smooth_y = None

    # ======================================
    # 10. NEON GLOW EFFECT
    # ======================================

    glow = cv2.GaussianBlur(
        pink_canvas,
        (0, 0),
        sigmaX=10,
        sigmaY=10
    )

    # Combine pink glow and pink stroke
    neon = cv2.addWeighted(
        glow,
        0.9,
        pink_canvas,
        1.0,
        0
    )

    # Add white center
    neon = cv2.addWeighted(
        neon,
        1.0,
        white_canvas,
        0.8,
        0
    )

    # Blend with camera
    frame = cv2.addWeighted(
        frame,
        0.75,
        neon,
        1.0,
        0
    )

    # ======================================
    # 11. DISPLAY INSTRUCTIONS
    # ======================================

    cv2.putText(
        frame,
        "PINCH THUMB + INDEX: WRITE",
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (0, 255, 255),
        2
    )

    cv2.putText(
        frame,
        "RELEASE: MOVE TO NEXT WORD",
        (20, 80),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.65,
        (0, 255, 0),
        2
    )

    cv2.putText(
        frame,
        "C: CLEAR | Q: QUIT",
        (20, 120),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        WHITE,
        2
    )

    # ======================================
    # 12. SHOW WINDOW
    # ======================================

    cv2.imshow(
        "Smooth Neon Handwriting",
        frame
    )

    key = cv2.waitKey(1) & 0xFF

    # Clear all writing
    if key == ord('c'):

        pink_canvas[:] = 0
        white_canvas[:] = 0

        previous_x = None
        previous_y = None

    # Quit
    if key == ord('q'):
        break

# ==========================================
# 13. CLEANUP
# ==========================================

cap.release()
hands.close()

cv2.destroyAllWindows()
