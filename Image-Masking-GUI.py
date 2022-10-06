import tkinter as tk
from tkinter import *
from PIL import Image
from PIL import ImageTk
from tkinter import filedialog
import cv2
import numpy as np

class App:
    original_image = None
    hsv_image = None
    image_mask = None

    def __init__(self, master):
        self.img_path = None

        width  = root.winfo_screenwidth()
        height = root.winfo_screenheight()

        root.geometry('{}x{}'.format(width,height))

        self.low_hue = tk.Scale(master, label='Low',from_=0, to=180, length=300,showvalue=2,orient=tk.HORIZONTAL, command=self.show_changes)
        self.low_hue.place(x=75, y=530)

        self.high_hue = tk.Scale(master,label='High', from_=0, to=180, length=300,orient=tk.HORIZONTAL, command=self.show_changes)
        self.high_hue.place(x=75, y=600)
        self.high_hue.set(180)
###########################################################################################################

        self.low_sat = tk.Scale(master, label='Low',from_=0, to=255, length=300,orient=tk.HORIZONTAL, command=self.show_changes)
        self.low_sat.place(x=525, y=530)

        self.high_sat = tk.Scale(master, label="High", from_=0, to=255, length=300,orient=tk.HORIZONTAL, command=self.show_changes)
        self.high_sat.place(x=525, y=600)
        self.high_sat.set(255)
###########################################################################################################

        self.low_val = tk.Scale(master, label="Low",from_=0, to=255, length=300,orient=tk.HORIZONTAL, command=self.show_changes)
        self.low_val.place(x=975, y=530)

        self.high_val = tk.Scale(master, label="High",from_=0, to=255, length=300,orient=tk.HORIZONTAL, command=self.show_changes)
        self.high_val.place(x=975, y=600)
        self.high_val.set(255)

###########################################################################################################
# buttons
        # Open
        self.open_btn = tk.Button(text="Pilih Gambar", command=self.open_file ,width=12)
        self.open_btn.place(x=20, y=460)

########################################################################################################## Images
# frame
        frame0 = Frame(root, width = 404, height = 404, highlightbackground="#4a4a49", highlightcolor="#4a4a49", highlightthickness=2, bd=0)
        l = Entry(frame0, borderwidth=0, relief="flat", bg="#dedcd7")
        l.place(width=400, height=400)
        frame0.pack()
        frame0.place(x = 25, y = 25)

        frame1 = Frame(root, width = 404, height = 404, highlightbackground="#4a4a49", highlightcolor="#4a4a49", highlightthickness=2, bd=0)
        l1 = Entry(frame1, borderwidth=0, relief="flat", bg="#dedcd7")
        l1.place(width=400, height=400)
        frame1.pack()
        frame1.place(x = 475, y = 25)

        frame2 = Frame(root, width = 404, height = 404, highlightbackground="#4a4a49", highlightcolor="#4a4a49", highlightthickness=2, bd=0)
        l2 = Entry(frame2, borderwidth=0, relief="flat", bg="#dedcd7")
        l2.place(width=400, height=400)
        frame2.pack()
        frame2.place(x = 925, y = 25)

##########################################################################################################
    def open_file(self):
        global once
        once = True
        img_file = filedialog.askopenfilename(filetypes = [
        ("image", ".jpeg"),
        ("image", ".png"),
        ("image", ".jpg")])   # pilih file
        # this makes sure you select a file otherwise program crashes if not
        if img_file  != '':      # Si La imagen existe
            self.img_path = img_file 
            # This just makes sure that the image is displayed after opening it.
            self.low_hue.set(self.low_hue.get()+1)
            self.low_hue.set(self.low_hue.get()-1)
        else:
            print('ERORR')
            return 0


    def show_changes(self, a):
        global once, img_screenshot

        if self.img_path == None:  # If the image does nothing
            return 0

        low_hue = self.low_hue.get()
        low_sat = self.low_sat.get()
        low_val = self.low_val.get()
        # Altos
        high_hue = self.high_hue.get()
        high_sat = self.high_sat.get()
        high_val = self.high_val.get()
        # Does nothing if low values ​​go higher than high values
        if low_val > high_val or low_sat > high_sat or low_hue > high_hue:
            return 0

        # Get image from file                
        self.original_image = cv2.imread(self.img_path,1)
        # image resized
        self.original_image = cv2.resize(self.original_image,(400,400))

        lower_color = np.array([low_hue,low_sat,low_val]) 
        upper_color= np.array([high_hue,high_sat,high_val])
        #convert image to hsv
        self.hsv_image = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2HSV)
        self.original_image = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2RGB)
        self.mask = cv2.inRange(self.hsv_image, lower_color, upper_color)
        self.res = cv2.bitwise_and(self.original_image, self.original_image, mask=self.mask)
        
        # konversi ke format PIL
        self.original_image = Image.fromarray(self.original_image)
        self.original_image = ImageTk.PhotoImage(self.original_image)
        label_img = tk.Label(root, image=self.original_image, relief=tk.SOLID )
        label_img.image = self.original_image
        label_img.place(x=25, y=25)
        # once = False

        # convierte a formato PIL
        self.mask = Image.fromarray(self.mask)
        self.mask = ImageTk.PhotoImage(self.mask)
        labelm_img = tk.Label(root, image=self.mask, relief=tk.SOLID )
        labelm_img.image = self.mask
        labelm_img.place(x=475, y=25)
        
        self.res = Image.fromarray(self.res)
        self.res = ImageTk.PhotoImage(self.res)
        label_Ires1 = tk.Label(root, image=self.res, relief=tk.SOLID)
        label_Ires1.image = self.res
        label_Ires1.place(x=925, y=25)

# Instance of Tkinter
root = tk.Tk()
# New tkinter instnace of app
app = App(root)
# loops over to keep window active
root.mainloop()