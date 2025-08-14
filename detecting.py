import cv2
from ultralytics import YOLO
import time
from Actions import Actions


def Real_Time_Video_Process():
    weaponDetected = False
    writeVideo = True

    yolo_model = YOLO('./runs/detect/Normal_Compressed/weights/best.pt')
    
    video_capture = cv2.VideoCapture(0)
    
    width = int(video_capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')

    out = None
    action = Actions()
    
    while True:
        ret, frame = video_capture.read()
        if not ret:
            break
        
        if weaponDetected:
            out.write(frame)
        
        results = yolo_model(frame)

        if cv2.waitKey(1) == ord('q'):
            break

        for result in results:
            classes = result.names
            cls = result.boxes.cls
            conf = result.boxes.conf
            detections = result.boxes.xyxy

            for pos, detection in enumerate(detections):
                if conf[pos] >= 0.6:
                    weaponDetected = True

                    if writeVideo:
                        out = cv2.VideoWriter('currentFeed.mp4', fourcc, 20.0, (width, height))
                        writeVideo = False

                    xmin, ymin, xmax, ymax = detection
                    label = f"{classes[int(cls[pos])]} {conf[pos]:.2f}" 
                    color = (0, int(cls[pos]), 255)
                    cv2.rectangle(frame, (int(xmin), int(ymin)), (int(xmax), int(ymax)), color, 2)
                    cv2.putText(frame, label, (int(xmin), int(ymin) - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2, cv2.LINE_AA)
                    cv2.imwrite('static/currentDetection.jpg',frame)

                    # action.NotifyOwner(label)

        cv2.imshow('Live Feed', frame)
    video_capture.release()
    out.release()


Real_Time_Video_Process()