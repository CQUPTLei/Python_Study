# -*- coding = utf-8 -*-
# @TIME :     2022/10/27 上午 6:41
# @Author :   CQUPTLei
# @File :     video_play_tkinter.py
# @Software : PyCharm

from tkinter import *
from PIL import ImageTk, Image
import cv2

root = Tk()
# Create a frame
app = Frame(root, bg="white")
app.grid()
# Create a label in the frame
lmian = Label(app)
lmian.grid()

# Capture from camera
cap = cv2.VideoCapture('video331.mp4')


# function for video streaming
def video_stream():
    _, frame = cap.read()
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    img = Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=img)
    lmian.imgtk = imgtk
    lmian.configure(image=imgtk)
    lmian.after(1, video_stream)


video_stream()
root.mainloop()
