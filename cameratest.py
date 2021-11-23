import cv2

cap = cv2.VideoCapture(2, cv2.CAP_DSHOW)

while True:
    ret, frame = cap.read()
    cv2.imshow('demo', frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break
cap.release()
cv2.destroyAllWindows()
