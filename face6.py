import cv2
import requests,json
import threading,time
import numpy as np
from insightface.app import FaceAnalysis

video = cv2.VideoCapture(0)
#video.set(cv2.CAP_PROP_FPS,30)
#video.set(cv2.CAP_PROP_FRAME_WIDTH,1280)
#video.set(cv2.CAP_PROP_FRAME_HEIGHT,720)
print("check!")
app=FaceAnalysis()
app.prepare(ctx_id=0,det_size=(640,640))
print("check!")
faces="0"
nowtime=0
#10秒
waittime=10
timestate=False
#0:wait 1:active
fps=0
fpsc=0
fpstime=time.time()
print("check!")
def POST(Data):
    #Post先
    #テスト
    url ="https://httpbin.org/post"
    #本番
    #url="http://133.167.122.196:8080/api/posts"
    response=requests.post(url,json={"numPeople":Data})
    if(response.status_code==200):
        print("POST Success")
    else:
        print("Post Failed :%d"%response.status_code)
    print(response.text)

def Shot():
    # フレームを読込み
    ret, frame = video.read()
    # フレームが読み込めなかった場合は終了（動画が終わると読み込めなくなる）
    height = frame.shape[0]
    width = frame.shape[1]
    cv2.imwrite("check.jpg",frame)

Shot()
print("check!")
while True:
    if not timestate:
        #POST用スレッド
        Shot()
        faces = app.get(np.asarray(cv2.imread("check.jpg")))
        rimg = app.draw_on(cv2.imread("check.jpg"), faces)
        cv2.imshow('frame', rimg)
        #Post_thread=threading.Thread(target=POST,args=(len(faces),))
        Post_thread=threading.Thread(target=POST,args=(str(len(faces)),))
        timestate=True
        nowtime=time.time()
    if(time.time()-nowtime>waittime):
        Post_thread.start()
        timestate=False

    # qキーの押下で処理を中止
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'): break

#メモリの解放
video.release()
cv2.destroyAllWindows()
