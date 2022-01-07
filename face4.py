import cv2

capture = cv2.VideoCapture(0)
before = None

# エリアの最大値と最小値は任意の値に変更して
MAX_AREA_LIMIT = 50000
MIN_AREA_LIMIT = 1000

while capture.isOpened():
    #  OpenCVでWebカメラの画像を取り込む
    ret, frame = capture.read()
    # frameのサイズを変更
    # スクリーンショットを撮りたい関係で1/4サイズに縮小
    frame = cv2.resize(frame, (int(frame.shape[1]/2), int(frame.shape[0]/2)))

    # 加工なし画像を表示する
    cv2.imshow('frame', frame)

    # 取り込んだフレームに対して差分をとって動いているところが明るい画像を作る
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.bitwise_not(gray, gray)
    if before is None:
        before = gray.copy().astype('float')
        continue

    # 現フレームと前フレームの加重平均を使うと良いらしい
    cv2.accumulateWeighted(gray, before, 0.2)
    mdframe = cv2.absdiff(gray, cv2.convertScaleAbs(before))
    # 動いているところが明るい画像を表示する
    cv2.imshow('MotionDetected Frame', mdframe)

    # 動いているエリアの面積を計算してちょうどいい検出結果を抽出する

    # 閾値を指定して2値化する
    _, thresh = cv2.threshold(mdframe, 3, 255, cv2.THRESH_BINARY)

    # 輪郭データに変換しくれるfindContours
    contours, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    max_area = 0
    target = contours[0]

    for cnt in contours:
         #輪郭の面積を求めてくれるcontourArea
        area = cv2.contourArea(cnt)

        if max_area < area and area < MAX_AREA_LIMIT and area > MIN_AREA_LIMIT:
            max_area = area;
            target = cnt

    # 動いているエリアのうちそこそこの大きさのものがあればそれを矩形で表示する
    if max_area <= MIN_AREA_LIMIT:
        areaframe = frame
        # 動体検知できていないことを表示しているだけ
        cv2.putText(areaframe, 'Not Detected', (0,50), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255,0), 3, cv2.LINE_AA)
    else:
        # 矩形検出
        x, y, width, height = cv2.boundingRect(target)
        areaframe = cv2.rectangle(frame, (x, y),(x + width, y + height), (0,255,0), 2)

    cv2.imshow('MotionDetected Area Frame', areaframe)

    # q が押されたら終了させる、ラズパイだと何で終了させたらいいのかは自分で調べて
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break;

# キャプチャをリリースして、ウィンドウをすべて閉じる
capture.release()
cv2.destroyAllWindows()
