import streamlit as st
#import streamlit_cookies 
# import pyrebase
# # from pyrebase import auth, firestore, db, storage
# from pyrebase import auth
from datetime import datetime
from PIL import Image
import os
import detect 
import numpy as np
from pyrebase import pyrebase
import cv2
import torch
app = pyrebase.initialize_app({
  "apiKey": "AIzaSyBycpbkiKIMWQZrKhkfXfr1KJBNrhLvQkE",
  "authDomain": "diseasedetection-3332e.firebaseapp.com",
  "databaseURL": "https://diseasedetection-3332e-default-rtdb.asia-southeast1.firebasedatabase.app",
  "projectId": "diseasedetection-3332e",
  "storageBucket": "diseasedetection-3332e.appspot.com",
  "messagingSenderId": "1037571143092",
  "appId": "1:1037571143092:web:2a3fce17792c2b90f66ee1"}
)

def imageInput():
    image_file = st.file_uploader("Upload An Image", type=['png', 'jpeg', 'jpg'])
    col1, col2 = st.columns(2)
    if image_file is not None:
        img = Image.open(image_file)
        with col1:
            st.image(img, caption='Uploaded Image', use_column_width='always')
        ts = datetime.timestamp(datetime.now())
        imgpath = os.path.join('uploads', str(ts).replace(".", "") + image_file.name)
        
        with open(imgpath, mode="wb") as f:
            f.write(image_file.getbuffer())
            upload_file(imgpath, 'initial')

        detect.detect(weights = 'models/best.pt', source = imgpath, project = 'uploads' , name= 'images', device = 0)
        
        #--Display predicton
        outputpath = os.path.join(str(newestFile('uploads')), os.path.basename(imgpath))
        img_ = Image.open(outputpath)
        upload_file(outputpath, 'detected')
        with col2:
            st.image(img_, caption='Model Prediction(s)', use_column_width='always')

def videoInput():
    uploaded_video = st.file_uploader("Upload Video", type=['mp4', 'mpeg', 'mov'])
    if uploaded_video != None:

        ts = datetime.timestamp(datetime.now())
        imgpath = os.path.join('uploads', str(ts).replace(".", "") + uploaded_video.name)
        outputpath = os.path.join(newestFile('uploads'), os.path.basename(imgpath))

        with open(imgpath, mode='wb') as f:
            f.write(uploaded_video.read())  # save video to disk

        st_video = open(imgpath, 'rb')
        video_bytes = st_video.read()
        st.video(video_bytes)
        st.write("Uploaded Video")
        upload_file(imgpath, 'initial')
        detect.detect(weights = 'models/best.pt', source = imgpath, project = 'uploads' , name= 'videos', device = 0)
        
        outputpath = os.path.join(str(newestFile('uploads')), os.path.basename(imgpath))
        st_video2 = open(outputpath, 'rb')
        video_bytes2 = st_video2.read()
        st.video(video_bytes2)
        upload_file(outputpath, 'detected')
        st.write("Model Prediction")

def newestFile(folder):
  # Get all the files in the folder and its subfolders.
  files = []
  for root, dirs, _ in os.walk(folder):
    for file in dirs:
      files.append(os.path.join(root, file))

  # Sort the files by their modification time.
  files.sort(key=os.path.getmtime, reverse=True)

  # Return the path to the newest file.
  return files[0]

def play_webcam(conf):

    capturedImg = st.camera_input("Camera", key = "webcam Picture")
    if capturedImg is not None:
        #img = Image.open(capturedImg)
        ts = datetime.timestamp(datetime.now())
        imgpath = os.path.join('uploads/', str(ts).replace(".", "") + "_" + capturedImg.name) 
        
        with open(imgpath, 'wb') as screenshot:
            screenshot.write(capturedImg.getbuffer())
            st.write("File saved at ", imgpath)
            st_frame = st.empty()
            detect.detect(weights = 'models/best.pt', source = imgpath, project = 'uploads' , name= 'webcam', conf_thres = conf)
            
            outputpath = os.path.join(str(newestFile('uploads')), os.path.basename(imgpath))

            st_frame.image(Image.open(outputpath),
                        caption='Detected Video',
                        channels="BGR",
                        use_column_width=True
                        )

def realtime():
    if st.button('Start Webcam'):
        camera = cv2.VideoCapture(0)
        detect.detect(weights = 'models/best.pt', source = "0", project = 'uploads' , name = 'realtime', device = "0", nosave = True)


def login_firebase():
    with st.form("Login"):
        email = st.text_input("Email", key="email")
        password = st.text_input("Password", type="password", key="password")
        submit = st.form_submit_button()
        if submit:
            try:
                user = app.auth().sign_in_with_email_and_password(email, password)
                user_id = user['localId'] #uid to find and search
                st.session_state.cookie = str(user_id) + str(datetime.timestamp(datetime.now())) 
                st.success("You have successfully logged in!")
            except Exception as e:
                st.error("Invalid email or password. Please try again.")
                st.exception(e)

def signup_firebase():
    with st.form("Signup"):    
        email = st.text_input("Email", key="email")
        password = st.text_input("Password", type="password", key="password")
        username = st.text_input("Username", key="username")
        submit = st.form_submit_button()

    # If the user clicks the signup button, try to sign up the user with the provided credentials
    if submit:
      try:
        app.auth().create_user_with_email_and_password(email, password)
        st.success("Signup successful!")
      except Exception as e:
                st.error("Signup failed")
                st.exception(e)

   
def upload_file(video, state):
    if st.session_state['cookie'] is not None:
        try:
            fileRef = app.storage().child(str(state)).child(video).put(video)
            st.success("Upload successful!")
        except Exception as e:
            # Handle the error
            st.write("An error occured, click this to read")
            st.exception(e)
    else:
        st.write("You can login/signup to backup your detection")