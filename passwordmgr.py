from tkinter import *
from PIL import Image, ImageTk
import webbrowser
from tkinter import messagebox
import pymysql


passwordMgr_window = Tk()
passwordMgr_window.geometry('990x660+280+90')
passwordMgr_window.resizable(0, 0)
passwordMgr_window.title('Lock Box Password Manager  : As a project From Niladri Ghoshal')

# Set the absolute path to the icon file
icon_path = "key.png"

# Try to open the icon using PIL
try:
    icon = Image.open(icon_path)
    icon_photo = ImageTk.PhotoImage(icon)
    passwordMgr_window.iconphoto(True, icon_photo)
except Exception as e:
    print("Error loading and setting window icon:", e)

bgImage = ImageTk.PhotoImage(file='passwordmngr_bg.jpg')
bgLabel = Label(passwordMgr_window, image=bgImage)
bgLabel.image = bgImage
bgLabel.place(x=0, y=0)


passwordMgr_window.mainloop()