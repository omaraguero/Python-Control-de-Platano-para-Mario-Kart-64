import cv2
import numpy as np
import vgamepad as vg

gamepad = vg.VX360Gamepad()
cap = cv2.VideoCapture(0)

lowerYellow = np.array([20, 100, 100])
upperYellow = np.array([30, 255, 255])

minSize = 2000
maxSize = 40000

while True:
    ret,frame = cap.read()
    frame = cv2.flip(frame, 1)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    mask = cv2.inRange(hsv, lowerYellow, upperYellow)
    
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    for contour in contours:
        area = cv2.contourArea(contour)
        
        if minSize < area < maxSize:
            
            rect = cv2.minAreaRect(contour)
            box = cv2.boxPoints(rect)
            box = np.int0(box)
            
            (x,y),(w,h),angle=rect
            if w>h:
                angle = angle + 90
            
            cv2.drawContours(frame,[box],0,(0,255,0,2))
            
            currentPos = (int(x),int(y))
            
            #cv2.putText(frame, str(angle), (50,50), cv2.FONT_HERSHEY_DUPLEX, 2, (0,255,0))
            #cv2.putText(frame, str(currentPos), (50,100), cv2.FONT_HERSHEY_DUPLEX, 2, (0,255,0))
            
            gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_A)
            gamepad.left_joystick(x_value= int((angle - 92.5)/0.0022),y_value=0)
            
            
            if y > 320:
                gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_B)
            else:
                gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_B)
            
            gamepad.update()    

    cv2.imshow("detector de platano", frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_A)        
gamepad.left_joystick(x_value=0,y_value=0)
gamepad.update()