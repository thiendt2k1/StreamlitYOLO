import torch
import cv2
import streamlit as st
import firebase_admin
from firebase_admin import firestore, db,auth, storage
import datetime

#cred_obj = firebase_admin.credentials.Certificate('google-services.json')
firebaseConfig = {
  "apiKey": "AIzaSyBycpbkiKIMWQZrKhkfXfr1KJBNrhLvQkE",
  "authDomain": "diseasedetection-3332e.firebaseapp.com",
  "projectId": "diseasedetection-3332e",
  "storageBucket": "diseasedetection-3332e.appspot.com",
  "messagingSenderId": "1037571143092",
  "appId": "1:1037571143092:web:2a3fce17792c2b90f66ee1"
}

# app = firebase_admin.initialize_app(cred_obj, {
#     "databaseURL": "https://diseasedetection-3332e-default-rtdb.asia-southeast1.firebasedatabase.app"
# })
app = firebase_admin.initialize_app(firebaseConfig)
bucket = storage.bucket()

#app = firebase_admin.initialize_app(cred_obj, {
	# "apiKey": "AIzaSyBycpbkiKIMWQZrKhkfXfr1KJBNrhLvQkE",
    # "authDomain": "diseasedetection-3332e.firebaseapp.com",
    # "databaseURL": "https://diseasedetection-3332e-default-rtdb.asia-southeast1.firebasedatabase.app",
    # "storageBucket": "diseasedetection-3332e.appspot.com",
    # "serviceAccount": "serviceAccountCredentials.json"
	# })
db = firestore.client()


def play_webcam(conf):
    if st.sidebar.button('Detect Objects'):
        try:
            vid_cap = cv2.VideoCapture(1)
            st_frame = st.empty()
            while (vid_cap.isOpened()):
                success, image = vid_cap.read()
                if success:
                    # _display_detected_frames(conf,
                    #                          model,
                    #                          st_frame,
                    #                          image,
                    #                          is_display_tracker,
                    #                          tracker,
                    #                          )
                    model = torch.hub.load('ultralytics/yolov5', 'custom', path='models/best.pt', force_reload=True) 
                    res = model(source = image, conf_thres = conf, device = 0)
                    # Plot the detected objects on the video frame
                    res_plotted = res[0].plot()
                    st_frame.image(res_plotted,
                                caption='Detected Video',
                                channels="BGR",
                                use_column_width=True
                                )
                else:
                    vid_cap.release()
                    break
        except Exception as e:
            st.sidebar.error("Error loading video: " + str(e))

def play_stored_video(conf):
    """
    Plays a stored video file. Tracks and detects objects in real-time using the YOLOv8 object detection model.

    Parameters:
        conf: Confidence of YOLOv8 model.
        model: An instance of the `YOLOv8` class containing the YOLOv8 model.

    Returns:
        None

    Raises:
        None
    """
    source_vid = st.sidebar.file_uploader(
        "Choose a video...", type=['mp4', 'mov'])

    with open(source_vid, 'rb') as video_file:
        video_bytes = video_file.read()
    if video_bytes:
        st.video(video_bytes)

    if st.sidebar.button('Detect Video Objects'):
        try:
            vid_cap = cv2.VideoCapture(source_vid)
            st_frame = st.empty()
            while (vid_cap.isOpened()):
                success, image = vid_cap.read()
                if success:
                    # _display_detected_frames(conf,
                    #                          model,
                    #                          st_frame,
                    #                          image,
                    #                          is_display_tracker,
                    #                          tracker
                    #                          )
                    model = torch.hub.load('ultralytics/yolov5', 'custom', path='models/best.pt', force_reload=True) 
                    res = model(source = image, conf_thres = conf, device = 0)
                    # Plot the detected objects on the video frame
                    res_plotted = res[0].plot()
                    st_frame.image(res_plotted,
                                caption='Detected Video',
                                channels="BGR",
                                use_column_width=True
                                )
                else:
                    vid_cap.release()
                    break
        except Exception as e:
            st.sidebar.error("Error loading video: " + str(e))


def display_tracker_options():
    display_tracker = st.radio("Display Tracker", ('Yes', 'No'))
    is_display_tracker = True if display_tracker == 'Yes' else False
    if is_display_tracker:
        tracker_type = st.radio("Tracker", ("bytetrack.yaml", "botsort.yaml"))
        return is_display_tracker, tracker_type
    return is_display_tracker, None

def login_firebase():
    email = st.sidebar.text_input("Email")
    password = st.sidebar.text_input("Password", type="password")
    if st.button("Log In"):
        try:
            auth.sign_in_with_email_and_password(email, password)
            st.success("You have successfully logged in!")
        except:
            st.error("Invalid email or password. Please try again.")
    return email

def signup_firebase():
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    name = st.text_input("Name")
    if st.button("Sign Up"):
        try:
            user = auth.create_user(
                email = email,
                password = password,
                name = name
            )
            st.success("You have successfully signed up!")
        except:
            st.error("Something went wrong. Please try again.")

def upload_file(video):
    ts = datetime.timestamp(datetime.now())
    filename = str(ts) + video.name 
    blob = bucket.blob(filename)
    blob.upload_from_file(video)