import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from datetime import datetime

def addAttendanceTime(id):


    ref = db.reference('FaceID')

    new_attendance_time = str(datetime.now())

    # Get the current data for "VANH" from the database
    data_of_id = ref.child(id).get()

    # Add the new attendance time to the list
    data_of_id["attendance time"].append(new_attendance_time)

    # Update the data in the database for "VANH"
    ref.child(id).update(data_of_id)

def removeAttendanceTimeByKey(id, key_to_remove):
    ref = db.reference('FaceID')

    # Lấy dữ liệu hiện tại của 'id' từ database
    data_of_id = ref.child(id).get()

    # Xóa phần tử tại key_to_remove nếu tồn tại
    if "attendance time" in data_of_id and key_to_remove in data_of_id["attendance time"]:
        data_of_id["attendance time"].pop(key_to_remove)

        # Cập nhật lại dữ liệu trong database
        ref.child(id).update({"attendance time": data_of_id["attendance time"]})

# Gọi hàm để xóa một attendance time cụ thể, ví dụ key = 0
# if _name_ == '_main_':
#     for i in range(5, 67):
#         removeAttendanceTimeByKey('VANH', i)

# cred = credentials.Certificate(".\serviceAccount.json")
# app = firebase_admin.initialize_app(cred, {
#     'databaseURL': "https://faceiot-7f1d0-default-rtdb.firebaseio.com/"
#     })
# addAttendanceTime('VANH')
