import os
from datetime import datetime
import cv2
from PIL import Image
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

ts = 1564643213.135456
imgpath = os.path.join('uploads', str(ts).replace(".", "") + "123.png")
outputpath = os.path.join(newestFile('uploads'), os.path.basename(imgpath))

print(newestFile('uploads'))
print('\n')
print(imgpath)
print('\n')
print(outputpath)
Image.open(r"E:\Downloads\YOLOv5-Streamlit-Deployment-main\uploads\images3\1683723334378502138.jpg")