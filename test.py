import cv2
import requests,json
import threading,time
import queue


class ThreadingVideoCapture:
    def __init__(self,src,max_queue_size=256):
        print("クラス初期化...")
        self.video = cv2.VideoCapture(src)
        self.video.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('H', '2', '6', '4'));
        self.video.set(cv2.CAP_PROP_FPS, 30)
        #self.video.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        #self.video.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        self.q = queue.Queue(maxsize=max_queue_size)
        self.stopped=False
        facerect="0"
        #print("クラス初期化完了")


    def start(self):
        print("スレッド開始...")
        thread=threading.Thread(target=self.update,daemon=True)
        thread.start()
        return self

    def update(self):
        print("アップデート...")
        while True:
            if self.stopped:
                return
            ret, frame = video.read()

            self.q.put((ret,frame))

            if not ret:
                self.stop()
                return
            self.check()

    def check(self):
        print("顔検出...")
        # 顔検出
        facerect = cascade.detectMultiScale(frame, scaleFactor=1.1, minNeighbors=2, minSize=(10, 10))
        # 矩形線の色
        rectangle_color = (0, 255, 0) #緑色
        # 顔を検出した場合
        if len(facerect) > 0:
            for rect in facerect:
                cv2.rectangle(frame, tuple(rect[0:2]),tuple(rect[0:2] + rect[2:4]), rectangle_color, thickness=2)
        #顔認識した人数
        #cv2.putText(frame,"Human:{0}".format(len(facerect)),(10,100), cv2.FONT_HERSHEY_PLAIN, 3, (0,0,255), 2, cv2.LINE_AA)
        cv2.putText(frame,"FPS:{0}".format(fps),(10,200),cv2.FONT_HERSHEY_PLAIN,3,(255,0,0),2,cv2.LINE_AA)
    def read(self):
        return self.q.get()

    def stop(self):
        self.stopped=True

    def release(self):
        self.stopped=True
        self.video.release()

    def isOpened(self):
        return self.video.isOpened()

    def get(self,i):
        return self.video.read(i)



#opencvのカスケードパス
#cascade_path = "C:/opencv/sources/data/haarcascades/haarcascade_frontalface_default.xml"
cascade_path = "C:/opencv/sources/data/haarcascades/haarcascade_upperbody.xml"
cascade = cv2.CascadeClassifier(cascade_path)

#変数初期化
nowtime=0
waittime=10
timestate=False
#0:待機中
#1:時刻経過待ち
fps=0
fpsc=0
fpstime=time.time()


def POST(Data):
    #POST先
    #テスト環境
    url ="https://httpbin.org/post"
    #本番環境
    #url="http://172.20.10.2:3000/api/posts"
    response=requests.post(url,json={"numPeople":Data})
    if(response.status_code==200):
        print("POST成功")
    else:
        print("POST失敗 :%d" %response.status_code)
    print(response.text)


video=ThreadingVideoCapture(0)

if not video.isOpened():
    raise RuntimeError

video.start()
print("ビデオ開始...")
while True:
    fpsc=fpsc+1
    if(time.time()-fpstime>1):
        fps=fpsc
        fpsc=0
        fpstime=time.time()
    ret,frame=video.read()

    if not ret:
        break
    video.check()

    if not timestate:
        #POST用スレッド
        Post_thread=threading.Thread(target=POST,args=(len(facerect),))
        timestate=True
        nowtime=time.time()

    if(time.time()-nowtime>waittime):
        Post_thread.start()
        timestate=False

    cv2.imshow('frame',frame)

    # qキーの押下で処理を中止
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'): break
video.release()
cv2.destroyAllWindows()

"""
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
    # 顔検出
    facerect = cascade.detectMultiScale(frame, scaleFactor=1.1, minNeighbors=2, minSize=(10, 10))
    # 矩形線の色
    rectangle_color = (0, 255, 0) #緑色

    # 顔を検出した場合
    if len(facerect) > 0:
        for rect in facerect:
            cv2.rectangle(frame, tuple(rect[0:2]),tuple(rect[0:2] + rect[2:4]), rectangle_color, thickness=2)
    #顔認識した人数
    #cv2.putText(frame,"Human:{0}".format(len(facerect)),(10,100), cv2.FONT_HERSHEY_PLAIN, 3, (0,0,255), 2, cv2.LINE_AA)
    cv2.putText(frame,"FPS:{0}".format(fps),(10,200),cv2.FONT_HERSHEY_PLAIN,3,(255,0,0),2,cv2.LINE_AA)

    if not timestate:
        #POST用スレッド
        Post_thread=threading.Thread(target=POST,args=(len(facerect),))
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
"""
