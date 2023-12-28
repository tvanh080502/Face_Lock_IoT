import sys
import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime

path = 'D:/Face_Lock_IoT/Python/ImageAttendance/'
images = []
classNames = []
stime = 0
myList = os.listdir(path)
print(myList)

for cl in myList:
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])
print(classNames)


def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        # Kiểm tra xem có khuôn mặt nào trong ảnh không
        face_locations = face_recognition.face_locations(img)
        if face_locations:
            encode = face_recognition.face_encodings(img)[0]
            encodeList.append(encode)
    return encodeList


def markAttendance(name, time):
    with open('D:/Face_Lock_IoT/Python/Attendance.csv', 'r+') as f:
        myDataList = f.readlines()
        nameList = []
        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])
        if name not in nameList or time >= 10:
            now = datetime.now()
            dtString = now.strftime('%Y/%M/%D %H:%M:%S')
            f.writelines(f'\n{name},{dtString}')


encodeListKnown = findEncodings(images)
print('Encoding Complete')

for img_path in myList:
    img = cv2.imread(os.path.join(path, img_path))

    imgS = cv2.resize(img, (0, 0), None, fx=0.25, fy=0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    facesCurFrame = face_recognition.face_locations(imgS)
    encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

    etime = datetime.now().strftime('%S')

    for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
        print(faceDis)
        matchIndex = np.argmin(faceDis)

        if faceDis[matchIndex] < 0.50:
            name = classNames[matchIndex].upper()
            if abs(int(etime) - int(stime)) >= 10:
                time = abs(int(etime) - int(stime))
                markAttendance(name, time)
                stime = etime
                unlock = True
        else:
            name = 'Unknown'

        print(name)
        y1, x2, y2, x1 = faceLoc
        y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)

    cv2.imshow('Webcam', img)
    cv2.waitKey(1)

cv2.destroyAllWindows()
