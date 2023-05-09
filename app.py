import streamlit as st
import torch
from detect import detect
from PIL import Image
import PIL
from io import *
import glob
from datetime import datetime
import os
import wget
import time
import helper


## CFG
cfg_model_path = "models/best.pt" 

cfg_enable_url_download = False
if cfg_enable_url_download:
    url = "https://archive.org/download/best/best.pt" #Configure this if you set cfg_enable_url_download to True
    cfg_model_path = f"models/{url.split('/')[-1:][0]}" #config model path from url name
## END OF CFG

def imageInput(device):
    
    image_file = st.file_uploader("Upload An Image", type=['png', 'jpeg', 'jpg'])
    col1, col2 = st.columns(2)
    if image_file is not None:
        img = Image.open(image_file)
        with col1:
            st.image(img, caption='Uploaded Image', use_column_width='always')
        ts = datetime.timestamp(datetime.now())
        imgpath = os.path.join('data/uploads', str(ts)+image_file.name)
        outputpath = os.path.join('data/outputs', os.path.basename(imgpath))
        with open(imgpath, mode="wb") as f:
            f.write(image_file.getbuffer())
            upload_file(image_file)

        #call Model prediction--
        model = torch.hub.load('ultralytics/yolov5', 'custom', path='models/best.pt', force_reload=True) 
        model.cuda() if device == 'cuda' else model.cpu()
        pred = model(imgpath)
        pred.render()  # render bbox in image
        for im in pred.ims:
            im_base64 = Image.fromarray(im)
            im_base64.save(outputpath)

        #--Display predicton
        
        img_ = Image.open(outputpath)
        upload_file(img_)
        with col2:
            st.image(img_, caption='Model Prediction(s)', use_column_width='always')

def videoInput(device):
    uploaded_video = st.file_uploader("Upload Video", type=['mp4', 'mpeg', 'mov'])
    if uploaded_video != None:

        ts = datetime.timestamp(datetime.now())
        imgpath = os.path.join('data/uploads', str(ts)+uploaded_video.name)
        outputpath = os.path.join('data/video_output', os.path.basename(imgpath))

        with open(imgpath, mode='wb') as f:
            f.write(uploaded_video.read())  # save video to disk

        st_video = open(imgpath, 'rb')
        video_bytes = st_video.read()
        st.video(video_bytes)
        st.write("Uploaded Video")
        upload_file(video_bytes)
        detect(weights=cfg_model_path, source=imgpath, device=0) if device == 'cuda' else detect(weights=cfg_model_path, source=imgpath, device='cpu')
        st_video2 = open(outputpath, 'rb')
        video_bytes2 = st_video2.read()
        st.video(video_bytes2)
        upload_file(video_bytes)
        st.write("Model Prediction")

def main():
    # -- Sidebar
    st.sidebar.title('⚙️Options')
    
    
    option = st.sidebar.radio("Select input type.", ['Image', 'Video', 'Webcam', 'video'])
    if torch.cuda.is_available():
        deviceoption = st.sidebar.radio("Select compute Device.", ['cpu', 'cuda'], disabled = False, index=1)
    else:
        deviceoption = st.sidebar.radio("Select compute Device.", ['cpu', 'cuda'], disabled = True, index=0)

    choice = st.sidebar.selectbox('login/Signup', ['Login', 'Sign up'])
    # -- End of Sidebar

    st.header('📦Obstacle Detection')
    st.subheader('👈🏽 Select options left-haned menu bar.')
    st.sidebar.markdown("https://github.com/thepbordin/Obstacle-Detection-for-Blind-people-Deployment")
    if option == "Image":    
        imageInput(deviceoption)
    elif option == "Video": 
        videoInput(deviceoption)
    elif option == "Webcam": 
        helper.play_webcam(40)
    elif option == "video": 
        helper.play_stored_video(40)
    elif choice == "Login":
        helper.login_firebase()
    elif choice == "Signup":
        helper.signup_firebase()
    

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