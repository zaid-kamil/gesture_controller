import cv2
import mediapipe as mp
import pyautogui
import time

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

colors= {
  'white': (255, 255, 255),
  'black': (0, 0, 0),
  'red': (0, 0, 255),
  'green': (0, 255, 0),
  'blue': (255, 0, 0),
  'yellow': (0, 255, 255),
}

# For webcam input:
cap = cv2.VideoCapture(0)
distance = -1
mid_x, mid_y = -1, -1
min_dis = 50


  


with mp_hands.Hands(
    model_complexity=0,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as hands:
  while cap.isOpened():
    success, image = cap.read()
    image = cv2.flip(image, 1)
    h, w, _ = image.shape
    if not success:
      print("Ignoring empty camera frame.")
      continue

    image.flags.writeable = False
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(image)
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    if results.multi_hand_landmarks:
      for hand_landmarks in results.multi_hand_landmarks:

        # get index finger tip
        index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
        middle_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]

        # get finger tip coordinates
        ix = int(index_finger_tip.x * w)
        iy = int(index_finger_tip.y * h)
        mx = int(middle_finger_tip.x * w)
        my = int(middle_finger_tip.y * h)
        mid_x, mid_y = int((ix + mx)/2), int((iy + my)/2)
        
        # calculate distance between index and middle finger
        distance = ((ix - mx)**2 + (iy - my)**2)**0.5
        if distance > 50:
          # draw circle on finger tip
          cv2.circle(image, (ix, iy), 10, colors['red'], 1)
          cv2.circle(image, (mx, my), 10, colors['blue'], 1)
          # draw line between index and middle finger
          cv2.line(image, (ix, iy), (mx, my), colors['white'], 2)
        else:
          # draw circle on finger tip
          cv2.circle(image, (ix, iy), 5, colors['green'], -1)
          cv2.circle(image, (mx, my), 5, colors['green'], -1)
          # draw line between index and middle finger
          cv2.line(image, (ix, iy), (mx, my), colors['green'], 2)

        # display distance
        cv2.putText(image, f'{distance:.2f}', (int((ix + mx)/2), int((iy + my)/2)),
                     cv2.FONT_HERSHEY_SIMPLEX, .5, colors['black'], 1)
        
    # 3x3 grid
    if distance > 0 and distance < min_dis:    
      # black grid
      cv2.line(image, (w//3, 0), (w//3, h), colors['black'], 1)
      cv2.line(image, (2*w//3, 0), (2*w//3, h), colors['black'], 1)
      cv2.line(image, (0, h//3), (w, h//3), colors['black'], 1)
      cv2.line(image, (0, 2*h//3), (w, 2*h//3), colors['black'], 1)      
    else:
      # white grid
      cv2.line(image, (w//3, 0), (w//3, h), colors['white'], 1)
      cv2.line(image, (2*w//3, 0), (2*w//3, h), colors['white'], 1)
      cv2.line(image, (0, h//3), (w, h//3), colors['white'], 1)
      cv2.line(image, (0, 2*h//3), (w, 2*h//3), colors['white'], 1)

    # text at the bottom of the middle grid square
    min_height = 60
    cv2.putText(image, 'control', (w//2 - 50, h//3*2 - min_height),
                cv2.FONT_HERSHEY_SIMPLEX, 1, colors['yellow'], 2)
    # text in the left middle grid square
    cv2.putText(image, 'left', (50, h//3*2 - min_height),
                cv2.FONT_HERSHEY_SIMPLEX, 1, colors['yellow'], 2)
    # text in the right middle grid square
    cv2.putText(image, 'right', (w//3*2 + 50, h//3*2 - min_height),
                cv2.FONT_HERSHEY_SIMPLEX, 1, colors['yellow'], 2)
    # text in the top middle grid square
    cv2.putText(image, 'up', (w//2 - 20, h//3 - min_height),
                cv2.FONT_HERSHEY_SIMPLEX, 1, colors['yellow'], 2)
    # text in the bottom middle grid square
    cv2.putText(image, 'down', (w//2 - 30, h//3*2 + min_height),
                cv2.FONT_HERSHEY_SIMPLEX, 1, colors['yellow'], 2)
    # text in the top left grid square
    cv2.putText(image, 'esc', (50, h//3 - min_height),
                cv2.FONT_HERSHEY_SIMPLEX, 1, colors['green'], 1)
    # text in the top right grid square
    cv2.putText(image, 'space', (w//3*2 + 50, h//3 - min_height),
                cv2.FONT_HERSHEY_SIMPLEX, 1, colors['green'], 1)
    # text in the bottom left grid square
    cv2.putText(image, 'enter', (50, h//3*2 + min_height),
                cv2.FONT_HERSHEY_SIMPLEX, 1, colors['green'], 1)

    # create a rectangle when the mid_x and mid_y are in a certain area of grid
    # middle left
    if mid_x > 0 and mid_x < w//3 and mid_y > h//3 and mid_y < h//3*2:
      cv2.rectangle(image, (0, h//3), (w//3, h//3*2), colors['yellow'], 2)
      # press left
      pass

    # middle right
    if mid_x > w//3*2 and mid_x < w and mid_y > h//3 and mid_y < h//3*2:
      cv2.rectangle(image, (w//3*2, h//3), (w, h//3*2), colors['yellow'], 2)
      # press right
      pass
        

    # middle top
    if mid_x > w//3 and mid_x < w//3*2 and mid_y > 0 and mid_y < h//3:
      cv2.rectangle(image, (w//3, 0), (w//3*2, h//3), colors['yellow'], 2)
      # press up
      pass
      
    
    # middle bottom
    if mid_x > w//3 and mid_x < w//3*2 and mid_y > h//3*2 and mid_y < h:
      cv2.rectangle(image, (w//3, h//3*2), (w//3*2, h), colors['yellow'], 2)
      # press down
      pass
      
    # top lelf
    if mid_x > 0 and mid_x < w//3 and mid_y > 0 and mid_y < h//3:
      cv2.rectangle(image, (0, 0), (w//3, h//3), colors['yellow'], 2)
      # press esc
      if distance<min_dis and tap == False:
        pyautogui.press('esc')
        tap = True
    
    # top right
    if mid_x > w//3*2 and mid_x < w and mid_y > 0 and mid_y < h//3:
      cv2.rectangle(image, (w//3*2, 0), (w, h//3), colors['yellow'], 2)
      # press space
      pass

    # bottom left
    if mid_x > 0 and mid_x < w//3 and mid_y > h//3*2 and mid_y < h:
      cv2.rectangle(image, (0, h//3*2), (w//3, h), colors['yellow'], 2)
      # press enter
      pass
    
    # middle
    if mid_x > w//3 and mid_x < w//3*2 and mid_y > h//3 and mid_y < h//3*2:
      cv2.rectangle(image, (w//3, h//3), (w//3*2, h//3*2), colors['red'], 2)

    cv2.imshow('MediaPipe Hands', image)
 
    if cv2.waitKey(5) & 0xFF == 27:
      break
cap.release()
cv2.destroyAllWindows()