import os, cv2, json, sys, shutil
import numpy as np
import logging
from django.http import StreamingHttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.conf import settings
from django.urls import reverse
from .forms import VideoForm
from ultralytics import YOLO
from datetime import datetime, timedelta
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
from collections import Counter, deque
from moviepy.editor import *
logging.getLogger().propagate = False


def modelSelection(case):
    """
    load model
    Returns :
        model : YOLO(model) : a DL model trained with YOLOv8
    """
    model_name = f'{case}.pt'
    base_dir = os.path.dirname(os.path.abspath(__file__))  # 현재 base 위치 지정
    model_path = os.path.join(base_dir, 'model', model_name)  # load model -> upload/model/model.pt
    model = YOLO(model_path)
    return model


def checkError(request, case):
    """
    checking request error and return err_msg or ai_model
    Args : case : str : a case of video file
    Returns :
        err_str : dict or False : error msg to print
        model : False or YOLO(model) : a DL model trained with YOLOv8
    """
    # default set
    err_str = 0
    model = 0

    if request.method == 'POST':
        try:
            video = request.FILES['files[]']  # load uploaded file
            if not video.name.endswith('.mp4'):
                err_str = {'title':'Invalid Video Format', 'content':'mp4 확장자 영상 파일을 업로드해주세요'}
            else:
                model = modelSelection(case)

        except KeyError:
            err_str = {'title':'No File Upload Error', 'content':'업로드 할 파일을 선택해주세요.'}

        except ValueError:
            err_str = {'title':'Invalid Video Upload Error', 'content':'유효하지 않은 영상입니다.'}

    return err_str, model


def namingFile(case):
    """
    Setting file path
    Args :
        case : str : uploading videofile's case
    Returns :
        save_path : str : path for saving files
        data_name : str : name of videoLog file
    """
    number = 0
    save_path = f"{settings.STATICFILES_DIRS[0]}/videoLog/{case}/{datetime.now().strftime('%Y-%m-%d')}/"
    data_name = f"{case}-{datetime.now().strftime('%Y-%m-%d')}-{number}"
    mvpy_path = f"{settings.STATICFILES_DIRS[0]}\\videoLog\\{case}\\{datetime.now().strftime('%Y-%m-%d')}\\"
    while os.path.exists(f"{save_path}/{data_name}.mp4"):
        number += 1
        data_name = f"{case}-{datetime.now().strftime('%Y-%m-%d')}-{number}"
    return save_path, data_name, mvpy_path


def setLogDirectory():
    """
    Setting log file path
    Returns :
        log_directory : str : to save log directory by this project
    """
    log_directory = 'log/'
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)
    return log_directory


def setVideo(video):
    """
    Setting function values by the video file
    Args :
        video : file : uploaded video file
    Returns :
        video_capture : cv2.VideoCapture
        frame_height : int : video_capture frame height
        frame_width : int : video_capture frame width
        codec : cv2.VideoWriter_fourcc
        fps : int : video fps
        frame_size : int : video frame size
    """

    video_capture = cv2.VideoCapture(video.temporary_file_path())
    frame_height = int(video_capture.get(4))
    frame_width = int(video_capture.get(3))
    videoMetaData = VideoFileClip(video.temporary_file_path())
    codec = cv2.VideoWriter_fourcc(*'mp4v')
    fps = int(video_capture.get(cv2.CAP_PROP_FPS))
    frame_size = videoMetaData.size

    return video_capture, frame_height, frame_width, codec, fps, frame_size


def classLogging(class_counts, class1_name, class2_name, class3_name, frame_in_class1, frame_in_class2, frame_in_class3, class1, class2, class3, normalize_check_size):
    """
    Setting the logging
    Args :
        class_counts :  :
        class_names(1,2,3) :  :
        frame_in_class(1,2,3) :  :
        class(1,2,3) :  :
    Returns :
        class(1,2,3) :  :
        frame_in_class(1,2,3) :  :
    """

    if class1_name in class_counts:
        frame_in_class1 = class1_name
    if class2_name in class_counts:
        frame_in_class2 = class2_name
    if class3_name in class_counts:
        frame_in_class3 = class3_name

    class1.append(frame_in_class1)
    class2.append(frame_in_class2)
    class2.append(frame_in_class3)

    if class1_name and class1.count(class1_name) == normalize_check_size:
        frame_in_class1 = class1_name
    if class2_name and class2.count(class2_name) == normalize_check_size:
        frame_in_class2 = class2_name
    if class3_name and class3.count(class3_name) == normalize_check_size:
        frame_in_class3 = class3_name

    return class1, class2, class3, frame_in_class1, frame_in_class2, frame_in_class3


def excuteLogging(class_counts, case, text_log_path, now_time, frame_current):
    """
    Logging
    Args :
        class_counts : list or dict : if case is the human, this value's type must be dictionary
        case : string
        text_log_path : str : saving path
    """

    if case == 'human':
        for label, count in class_counts.items():
            times_check = now_time.strftime('%Y-%m-%d %H:%M:%S')
            with open(text_log_path, "a") as file:
                file.write(f"{times_check} {frame_current} {label} {count}people(s)\n")
    else:
        for label in class_counts:
            times_check = now_time.strftime('%Y-%m-%d %H:%M:%S')
            with open(text_log_path, "a") as file:
                file.write(f"{times_check} {frame_current} {label}\n")


def classNameSet(case):
    """
    setting class names by case
    Args : case : string : video file's case
    Returns :
        class 1,2,3 : deque : the value for checking video accuracy
        class1,2,3_name : str : class's name
        normalize_check_size : int :
    """

    # default set
    normalize_check_size = 3
    class1_name = 0
    class2_name = 0
    class3_name = 0

    if case == 'fire':
        class1_name = 'Fire_detected'
        class2_name = 'Smoke_detected'
    elif case == 'ppe':
        normalize_check_size = 5
        class1_name = 'Worker'
        class2_name = 'Helmet'
        class3_name = 'Vest'
    elif case == 'fall':
        class1_name = 'Fallen_detected'
    elif case == 'human':
        class1_name = 'Invading_detected'

    # class1~3 is the value for checking video accuracy
    class1 = deque(maxlen=normalize_check_size)
    class2 = deque(maxlen=normalize_check_size)
    class3 = deque(maxlen=normalize_check_size)

    return class1, class2, class3, class1_name, class2_name, class3_name, normalize_check_size


def point_in_polygon(point, polygon):
    point = Point(point)
    polygon = Polygon(polygon)
    if polygon.contains(point):
        return 'invade'
    else:
        return 'person'


def predictSelectedArea(frame, model, frame_size, frame_width, frame_height, points = [(281, 426), (648, 210), (977, 226), (978, 477), (470, 713)]):
    """
    if the case is 'human' this function active instead of predictOrdinary
    set the polygon in the video frame by vertex points
    And find only objects inside the polygon
    Args :
        frame : video_capture.read() : video frames
        model : YOLO(model) : a DL model trained with YOLOv8
        frame_size,frame_width,frame_heights : int : info of video file
        points : list of vertex tuples :
            * This project is prototype. So we used default parameter.
            but it must be a non-default parameter.
    Returns :
        results : model.predict() : model prediction results
        frame_predicted : video_capture.read() : video frames with drawn polygon and found objects
        class_counts : dict : {found class:counts}
    """

    frame_predicted = frame.copy()

    # draw polygon with setting from vertex points
    resized_points = []
    for point in points:
        x = int(point[0] * frame_size[0] / frame_width)
        y = int(point[1] * frame_size[1] / frame_height)
        resized_points.append((x, y))
    points = resized_points
    points_arr = np.array(points)
    cv2.polylines(frame_predicted, [points_arr.astype(np.int32)], isClosed=True, color=(0, 0, 255), thickness=2)

    results = model.predict(frame_predicted, verbose=False, conf=0.7, classes=[0, 1])[
        0]  # prediction conf 70%
    boxes = results.boxes.cpu().numpy()

    if len(points) > 3:
        class_check = []
        for box in boxes:
            r = box.xyxy[0].astype(int)
            ct = box.xywh[0].astype(int)
            text_position = (r[0], r[1] - 10)
            class_name = point_in_polygon(ct[:2], points)
            cv2.rectangle(frame_predicted, r[:2], r[2:], (255, 255, 255), 2)
            cv2.putText(frame_predicted, class_name, text_position, cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2,
                        cv2.LINE_AA)
            class_check.append(class_name)
        class_counts = Counter(class_check)
    return results, frame_predicted, class_counts


def predictOrdinary(frame, model):
    """
    predict the classes by video
    Args :
        frame : video_capture.read() : video frames
        model : YOLO(model) : a DL model trained with YOLOv8
    Returns :
        results : model.predict() : model prediction results
        frame_predicted : video_capture.read() : video frame with found objects
        class_counts : list : found class list
    """

    class_counts = [0]
    results = model.predict(frame, verbose=False, conf=0.7)[0]  # prediction conf 70%
    frame_predicted = results.plot(prob=False, conf=False)
    arr = results.boxes.cls.cpu().numpy()
    if len(arr) > 0:
        class_counts = np.vectorize(results.names.get)(arr)
    return results, frame_predicted, class_counts


def genFrames(video, model, case):
    """
    main function uploading.py
    Generate frames that display objects and logging objects detection to save
    Args :
        video : video file : uploaded video file
        model : YOLO(model) : a DL model trained with YOLOv8
        case : str : a case of uploaded video file
    """
    # preprocessing
    log_directory = setLogDirectory()
    save_path, data_name, mvpy_path = namingFile(case)
    video_capture, frame_height, frame_width, codec, fps, frame_size = setVideo(video)
    flag = 0
    frame_current = 0

    # log_path(LogFileName) : class-date-number_fps_(file's fps).log
    text_log_path = log_directory + f"{data_name}.log"

    # temp video write
    # 실시간처리영상(tempfile) dum dir에 작성
    dummy_path = f"{save_path}/dum/"
    os.makedirs(f"{dummy_path}", exist_ok=True)
    ######===== 오류발생으로 임시수정
    output_all_file = f"{mvpy_path}{data_name}.mp4"
    # mvpy_dum = mvpy_path + 'dum\\'
    # output_all_file = f"{mvpy_dum}{data_name}.mp4"
    ######===== 오류발생으로 임시수정
    all_video_writer = cv2.VideoWriter(output_all_file, codec, fps, frame_size)

    # class name set
    class1, class2, class3, class1_name, class2_name, class3_name, normalize_check_size = classNameSet(case)

    count = 0
    while video_capture.isOpened():
        count += 1
        frame_in_class1 = 0 # counting class1 from frame
        frame_in_class2 = 0
        frame_in_class3 = 0
        now_time = datetime.now()
        ret, frame = video_capture.read()  # 영상 프레임 읽기
        if not ret:  # 영상 재생이 안될 경우 break
            break
        frame = cv2.resize(frame, frame_size)

        # predict & frame processing
        if case == 'human':
            results, frame_predicted, class_counts = predictSelectedArea(frame, model, frame_size, frame_width, frame_height)
        else:
            results, frame_predicted, class_counts = predictOrdinary(frame, model)

        ################## logging #########################
        class1, class2, class3, frame_in_class1, frame_in_class2, frame_in_class3 = classLogging(class_counts, class1_name, class2_name, class3_name, frame_in_class1, frame_in_class2, frame_in_class3, class1, class2, class3, normalize_check_size)

        # logging
        if (frame_in_class1 == class1_name) or (frame_in_class2 == class2_name) or (frame_in_class3 == class3_name) and (flag == 0):
            flag = 1
            excuteLogging(class_counts, case, text_log_path, now_time, frame_current)

        all_video_writer.write(frame_predicted)

        _, jpeg_frame = cv2.imencode('.jpg', frame_predicted)  # cv2.imshow가 안되기 때문에 대체하였음
        frame_bytes = jpeg_frame.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n'
               + frame_bytes + b'\r\n\r\n')

        frame_current += 1

    all_video_writer.release()
    video_capture.release()
    cv2.destroyAllWindows()
    clip = VideoFileClip(output_all_file)
    file_path = f"{mvpy_path}{data_name}.mp4"
    ######===== 오류발생으로 임시수정
    # clip.write_videofile(f"{file_path}", codec="libx264", fps=fps)
    # shutil.rmtree(dummy_path, ignore_errors=True) # delete dum
    ######===== 오류발생으로 임시수정
    #print('debug')