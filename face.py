import cv2,time
import requests,json
import threading

#動画を読込み
#カメラ等でストリーム再生の場合は引数に0等のデバイスIDを記述する
video = cv2.VideoCapture(0)

#opencvのカスケードパス
#cascade_path = "C:/opencv/sources/data/haarcascades/haarcascade_frontalface_default.xml"
cascade_path = "C:/opencv/sources/data/haarcascades/haarcascade_upperbody.xml"
cascade = cv2.CascadeClassifier(cascade_path)

#変数初期化
facerect="0"
nowtime=0
waittime=10
timestate=False
#0:待機中
#1:時刻経過待ち

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

while video.isOpened():
    # フレームを読込み
    ret, frame = video.read()

    # フレームが読み込めなかった場合は終了（動画が終わると読み込めなくなる）
    if not ret: break
    # 顔検出
    facerect = cascade.detectMultiScale(frame, scaleFactor=1.1, minNeighbors=2, minSize=(30, 30))
    # 矩形線の色
    rectangle_color = (0, 255, 0) #緑色

    # 顔を検出した場合
    if len(facerect) > 0:
        for rect in facerect:
            cv2.rectangle(frame, tuple(rect[0:2]),tuple(rect[0:2] + rect[2:4]), rectangle_color, thickness=2)
    #顔認識した人数
    cv2.putText(frame,"Human:{0}".format(len(facerect)),(10,100), cv2.FONT_HERSHEY_PLAIN, 3, (0,0,255), 2, cv2.LINE_AA)

    if not timestate:
        #POST用スレッド
        Post_thread=threading.Thread(target=POST,args=(len(facerect),))
        timestate=True
        nowtime=time.time()

    if(time.time()-nowtime>waittime):
        #POST(len(facerect))
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
