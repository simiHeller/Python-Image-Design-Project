from tkinter import filedialog

import cv2
import numpy as np
from tkinter import *
from tkinter import filedialog
from docutils.nodes import header
import imageio
import tkinter.colorchooser as colorchooser

class windows:
    def __init__(self,filePath):
        self.filePath=filePath
        self.image=imageio.imread(self.filePath)
        self.original_image=self.image.copy()
        self.start_point = 0
        self.end_point = 0
        self.cropping = False
        self.text_entry=None
        self.color = (255, 255, 255)  # Default text color is white
        self.chooseB=None
        self.display()
    def display(self):
        cv2.namedWindow("Image")
        cv2.imshow('Image', self.image)

    def draw_shape(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.start_point = (x, y)
            self.cropping = True
        elif event == cv2.EVENT_LBUTTONUP:
            self.end_point = (x, y)
            self.cropping = False
            radius=5
            center = (self.start_point[0], self.end_point[1])
            # pt1 = (100, 100)
            # pt2 = (200, 200)
            # pt3 = (300, 100)

            # draw lines between the vertices
            if(self.chooseB==1):
                cv2.circle(self.image, center, 20, self.bgr_color, 2)
            elif(self.chooseB==2):
               cv2.line(self.image, self.start_point, self.end_point, self.bgr_color, 2)
               cv2.line(self.image, self.start_point, center, self.bgr_color, 2)
               cv2.line(self.image, center, self.end_point, self.bgr_color, 2)
            # Draw the rectangle on the image
            # cv2.rectangle(self.image, self.start_point, self.end_point, self.bgr_color, 2)
          #  cv2.line(self.image,self.start_point, self.end_point, self.bgr_color, 25, cv2.LINE_AA)
            self.display()
            # Crop the image
            cropped_image = None
            if self.start_point and self.end_point:
                x1, y1 = self.start_point
                x2, y2 = self.end_point
                x1, x2 = min(x1, x2), max(x1, x2)
                y1, y2 = min(y1, y2), max(y1, y2)
                cropped_image = self.original_image[y1:y2, x1:x2]
                cv2.imshow('Image', self.image)
            return cropped_image

    # def add(self):
    #     cv2.imshow('Image',self.image)
    def add_text(self, user_text, user_color, x, y):
        cv2.putText(self.image, user_text, (x , y), cv2.FONT_HERSHEY_SIMPLEX, 1, user_color, 2)
        self.display()

    def write1(self):
        wind = Tk()
        wind.geometry("300x150")
        wind.title("Add Text")
        Label(wind, text="Enter text:").grid(row=0, column=0, padx=10, pady=10)
        self.text_entry = Entry(wind)
        self.text_entry.grid(row=0, column=1, padx=10, pady=10)

        color_label = Label(wind, text="Choose Color:")
        color_label.grid(row=1, column=0, padx=10, pady=10)

        color_button = Button(wind, text="Choose", command=lambda: self.choose_color(wind))
        color_button.grid(row=1, column=1, padx=10, pady=10)

        wind.mainloop()
    def choose_color(self,win):
        color = colorchooser.askcolor()[0]
        bgr_color = (color[2], color[1], color[0])
        if bgr_color:
            bgr_color = tuple([int(c) for c in bgr_color])
            # Convert color tuple from float to int
            self.bgr_color = bgr_color
            cv2.setMouseCallback("Image", self.on_mouse_place)
            self.text_entry=self.text_entry.get()
            win.destroy()

    def choose_color2(self, win):
        color = colorchooser.askcolor()[0]
        bgr_color = (color[2], color[1], color[0])
        if bgr_color:
            bgr_color = tuple([int(c) for c in bgr_color])
            # Convert color tuple from float to int
            self.bgr_color = bgr_color
            cv2.setMouseCallback("Image", self.draw_shape)
            # self.text_entry = self.text_entry.get()
            win.destroy()

    def on_mouse_place(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.start_point = (x, y)
            self.cropping = True
        elif event == cv2.EVENT_LBUTTONUP:
            self.end_point = (x, y)
            self.cropping = False
            # Add the text at the chosen location
            if self.start_point and self.end_point:
                x1, y1 = self.start_point
                x2, y2 = self.end_point
                x, y = min(x1, x2), min(y1, y2)
                self.add_text(self.text_entry, self.bgr_color, x, y)

    def cut1(self):
        self.image = self.image[60:90, 100:250]
        cv2.imshow("cut_new",self.image)
        # cv2.setMouseCallback('Image', self.draw_shape)
    def add_shape1(self):
        open=Tk()
        open.geometry("200x250")
        open.title("choose shape")
        radio = IntVar()

        r1 = Radiobutton(open, text="circle", variable=radio, value=1)
        r2 = Radiobutton(open, text="triangular", variable=radio, value=2)
        r3 = Radiobutton(open, text="rectangle", variable=radio, value=3)
        r4 = Radiobutton(open, text="line", variable=radio, value=4)
        r1.place(x=0,y=0)
        r2.place(x=0,y=50)
        r3.place(x=0,y=100)
        r4.place(x=0, y=150)
        self.chooseB = radio.get()

        self.text_entry = Entry(open)
        color_button = Button(open, text="Choose", command=lambda: self.choose_color2(open))
        color_button.grid(row=5, column=3, padx=110, pady=190)

    def save(self):
        filepath = filedialog.asksaveasfilename(defaultextension='.png')
        cv2.imwrite(filepath, self.image)
        cv2.destroyWindow("image")

    def change_color1(self):
        self.image = cv2.cvtColor(self.image, cv2.COLOR_BGRA2GRAY)
        cv2.imshow("Image", self.image)
