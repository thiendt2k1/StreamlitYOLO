import streamlit as st
from io import *

import wget
import time
import helper
import firebase_admin

## CFG
cfg_model_path = "models/best.pt" 

cfg_enable_url_download = False
if cfg_enable_url_download:
    url = "https://archive.org/download/best/best.pt" #Configure this if you set cfg_enable_url_download to True
    cfg_model_path = f"models/{url.split('/')[-1:][0]}" #config model path from url name




## END OF CFG

def main():
    #cred_obj = firebase_admin.credentials.Certificate('diseasedetection-3332e-firebase-adminsdk-eofbd-9784e0582b.json')
    # app = firebase_admin.initialize_app(cred_obj, {
	# "databaseURL": "https://diseasedetection-3332e-default-rtdb.asia-southeast1.firebasedatabase.app"})
    
    firebaseConfig = {
  "apiKey": "AIzaSyBycpbkiKIMWQZrKhkfXfr1KJBNrhLvQkE",
  "authDomain": "diseasedetection-3332e.firebaseapp.com",
  "databaseURL": "https://diseasedetection-3332e-default-rtdb.asia-southeast1.firebasedatabase.app",
  "projectId": "diseasedetection-3332e",
  "storageBucket": "diseasedetection-3332e.appspot.com",
  "messagingSenderId": "1037571143092",
  "appId": "1:1037571143092:web:2a3fce17792c2b90f66ee1"
}

    app = firebase_admin.initialize_app(firebaseConfig)
	
    # -- Sidebar
    st.sidebar.title('⚙️Options')
    
    option = st.sidebar.radio("Select input type.", ['Image', 'Video', 'Webcam'])

    choice = st.sidebar.selectbox('Login/Signup', ['Login', 'Sign up'])
    # -- End of Sidebar

    st.header('Coffee diseases detection')
    st.subheader('👈🏽 Select options left-haned menu bar.')
    st.sidebar.markdown("Github")
    if option == "Image":    
        helper.imageInput()
    elif option == "Video": 
        helper.videoInput()
    elif option == "Webcam": 
        helper.play_webcam(0.4)
    elif choice == "Login":
        helper.login_firebase()
    elif choice == "Signup":
        helper.signup_firebase()
    
def helper_function():
  # Get a reference to the app
  app = firebase_admin.get_app()

if __name__ == '__main__':
    
    main()

# Downlaod Model from url.    
@st.cache
def loadModel():
    start_dl = time.time()
    model_file = wget.download(url, out="models/")
    finished_dl = time.time()
    print(f"Model Downloaded, ETA:{finished_dl-start_dl}")
if cfg_enable_url_download:
    loadModel()