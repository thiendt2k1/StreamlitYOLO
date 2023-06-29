import streamlit as st
from io import *

import wget
import time
import helper
#import firebase_admin
from pyrebase import pyrebase

## END OF CFG


#     cred_obj = firebase_admin.credentials.Certificate('diseasedetection-3332e-firebase-adminsdk-eofbd-9784e0582b.json')
#     admin = firebase_admin.initialize_app(cred_obj, {
# 	"databaseURL": "https://diseasedetection-3332e-default-rtdb.asia-southeast1.firebasedatabase.app"})
#     client = admin.client()
firebase = pyrebase.initialize_app(
{
"apiKey": "AIzaSyBycpbkiKIMWQZrKhkfXfr1KJBNrhLvQkE",
"authDomain": "diseasedetection-3332e.firebaseapp.com",
"databaseURL": "https://diseasedetection-3332e-default-rtdb.asia-southeast1.firebasedatabase.app",
"projectId": "diseasedetection-3332e",
"storageBucket": "diseasedetection-3332e.appspot.com",
"messagingSenderId": "1037571143092",
"appId": "1:1037571143092:web:2a3fce17792c2b90f66ee1"
}
)
if 'cookie' not in st.session_state:
    st.session_state['cookie'] = None
# -- Sidebar
st.sidebar.title('⚙️Options')

option = st.sidebar.radio("Select input type.", ['Image', 'Login/Signup'])

choice = st.sidebar.selectbox('Login/Signup', ["Login", "Signup"])
# -- End of Sidebar

st.header('Coffee diseases detection')
st.subheader('👈🏽 Select options left-haned menu bar.')
st.sidebar.markdown("https://github.com/thiendt2k1/StreamlitYOLO")

if option == "Image":    
    helper.imageInput()
elif option == "Video": 
    helper.videoInput()
elif option == "Webcam": 
    helper.play_webcam(0.4)
elif option == "Login/Signup":
    if choice == "Login":
        helper.login_firebase()
    elif choice == "Signup":
        helper.signup_firebase()
elif option == "What you detected":
    if st.session_state['cookie'] is None:
        st.write("You must login in order to use this function")
    else:
        helper.showResult()

hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)