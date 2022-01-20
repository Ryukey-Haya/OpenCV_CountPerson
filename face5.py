import cv2
import requests,json
import threading,time
import numpy as np
from insightface.app import FaceAnalysis

video = cv2.VideoCapture(0,cv2.CAP_DSHOW)
video.set(cv2.CAP_PROP_FPS,30)
video.set(cv2.CAP_PROP_FRAME_WIDTH,1280)
video.set(cv2.CAP_PROP_FRAME_HEIGHT,720)

app=FaceAnalysis()
app.prepare(ctx_id=0,det_size=(640,640))

faces="0"
nowtime=0
#10秒
waittime=10
timestate=False
#0:wait 1:active
fps=0
fpsc=0
fpstime=time.time()

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

while video.isOpened():
    fpsc=fpsc+1
    if(time.time()-fpstime>1):
        fps=fpsc
        fpsc=0
        fpstime=time.time()

    # フレームを読込み
    ret, frame = video.read()
    # フレームが読み込めなかった場合は終了（動画が終わると読み込めなくなる）
    if not ret: break
    height = frame.shape[0]
    width = frame.shape[1]

    #顔認識した人数
    cv2.putText(frame,"Human:{0}".format(len(faces)),(10,100), cv2.FONT_HERSHEY_PLAIN, 3, (0,0,255), 2, cv2.LINE_AA)
    cv2.putText(frame,"FPS:{0}".format(fps),(10,200),cv2.FONT_HERSHEY_PLAIN,3,(255,0,0),2,cv2.LINE_AA)

    if not timestate:
        #POST用スレッド
        faces = app.get(np.asarray(frame))
        Post_thread=threading.Thread(target=POST,args=(len(faces),))
        timestate=True
        nowtime=time.time()

    if(time.time()-nowtime>waittime):
        Post_thread.start()
        timestate=False

    # フレームの描画
    cv2.imshow('frame', frame)

    # qキーの押下で処理を中止
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'): break

#メモリの解放
video.release()
cv2.destroyAllWindows()
