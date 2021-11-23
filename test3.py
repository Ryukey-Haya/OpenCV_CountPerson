import cv2
import requests,json
import threading,time

def save_picture():
    cap=cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('H', '2', '6', '4'));
    cap.set(cv2.CAP_PROP_FPS, 60)

    if not cap.isOpened():
        return
    ret,frame=cap.read()
    return frame
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

save_picture()

#opencvのカスケードパス
cascade_path = "C:/opencv/sources/data/haarcascades/haarcascade_frontalface_default.xml"
cascade=cv2.CascadeClassifier(cascade_path)

#変数初期化
facerect="0"
nowtime=0
waittime=10
waitcheck=1
checktime=0
poststate=False
checkstate=False
#0:待機中
#1:時刻経過待ち
fps=0
fpsc=0
fpstime=time.time()

while True:
    frame=cv2.imread('photo.png')
    fpsc=fpsc+1
    if(time.time()-fpstime>1):
        fps=fpsc
        fpsc=0
        fpstime=time.time()

    if not poststate:
        #POST用スレッド
        Post_thread=threading.Thread(target=POST,args=(len(facerect),))
        poststate=True
        posttime=time.time()

    if(time.time()-posttime>waittime):
        Post_thread.start()
        poststate=False

    if not checkstate:
        checkstate=True
        checktime=time.time()

    if(time.time()-checktime>waitcheck):
        frame=save_picture()

        # 顔検出
        facerect = cascade.detectMultiScale(frame, scaleFactor=1.1, minNeighbors=2, minSize=(10, 10))
        # 矩形線の色
        rectangle_color = (0, 255, 0) #緑色
            # 顔を検出した場合
        if len(facerect) > 0:
            for rect in facerect:
                cv2.rectangle(frame, tuple(rect[0:2]),tuple(rect[0:2] + rect[2:4]), rectangle_color, thickness=2)
        cv2.putText(frame,"Human:{0}".format(len(facerect)),(10,100), cv2.FONT_HERSHEY_PLAIN, 3, (0,0,255), 2, cv2.LINE_AA)

    # フレームの描画
    cv2.putText(frame,"FPS:{0}".format(fps),(10,200),cv2.FONT_HERSHEY_PLAIN,3,(255,0,0),2,cv2.LINE_AA)

    cv2.imshow('frame', frame)
    # qキーの押下で処理を中止
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'): break
