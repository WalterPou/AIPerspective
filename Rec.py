import cv2
import mediapipe as mp
import numpy as np
#import pyfirmata as pyf

#board = pyf.Arduino('COM4')
#Index = board.get_pin('d:9:i')
#Index.mode = pyf.SERVO
mpdraw = mp.solutions.drawing_utils
mpdraw_styles = mp.solutions.drawing_styles
mphands = mp.solutions.hands
hands = mphands.Hands()
cap = cv2.VideoCapture(0)
background = np.zeros([512,512,3],np.uint8)
#x1 = y1 = x2 = y2 = 0

def Main():
    while True:
        data, frame = cap.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(frame)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mpdraw.draw_landmarks(
                    background,
                    hand_landmarks,
                    mphands.HAND_CONNECTIONS
                )

                for idx, lm in enumerate(hand_landmarks.landmark):
                    h,w,_ = frame.shape
                    x,y = int(lm.x * w), int(lm.y * h)
                    if idx == 8:
                        x2 = x
                        y2 = y
                        cv2.putText(background, "IDX8", (x,y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (160,32,240), 1)
                    if idx == 0:
                        x1 = x
                        y1 = y
                        cv2.putText(background, "IDX0", (x,y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (160,32,240), 1)
                    try:
#                        degree_index = (y1 - y2) / 2    
#                        Index.write(int(degree_index))
#                        print(f'IDX8 >> {degree_index}')
                        cv2.rectangle(background, (x2,y2), (x1,y1), (0,0,255), 1)
                    except:
                        pass
        cv2.imshow('frame', background)
        background.fill(1)
        if cv2.waitKey(1) == ord('q'):
            break
    cv2.destroyAllWindows()

if __name__ == '__main__':
    Main()