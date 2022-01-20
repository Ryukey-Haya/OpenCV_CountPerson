import numpy as np
import cv2
from insightface.app import FaceAnalysis

image_file = "input.jpg"
img = cv2.imread(image_file)

app = FaceAnalysis()
app.prepare(ctx_id=0, det_size=(640, 640))

faces = app.get(np.asarray(img))
print("faces:" + str(len(faces)))

rimg = app.draw_on(img, faces)
cv2.imwrite("./output.jpg", rimg)

"""
import numpy as np
import cv2
from insightface.app import FaceAnalysis

cap=cv2.VideoCapture(0,cv2.CAP_DSHOW)
cap.set(cv2.CAP_PROP_FRAME_WIDTH,1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT,720)

app = FaceAnalysis()
app.prepare(ctx_id=0, det_size=(640, 640))

while True:
    ret, frame = cap.read()
    cv2.imshow("camera", frame)

    k = cv2.waitKey(1)&0xff # キー入力を待つ
    if k == ord('p'):
        img=frame
        faces = app.get(np.asarray(img))
        print("faces:" + str(len(faces)))
    elif k == ord('q'):
        # 「q」キーが押されたら終了する
        break

# キャプチャをリリースして、ウィンドウをすべて閉じる
cap.release()
cv2.destroyAllWindows()
"""
