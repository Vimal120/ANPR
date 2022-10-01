# Main.py
#@ Spectrum tech 
import cv2 as cv
import numpy as np
import os
import DetectChars
import DetectPlates
import PossiblePlate

import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
from tkinter import filedialog
import sys
from tkinter.filedialog import askopenfilename
import pymysql


class gui:
    def __init__(self, root):
          self.window = root
          self.window.title("Welcome to Number Plate Detection System")
          self.window.geometry("1180x900+0+0")
          self.window.config(bg = "lemon chiffon")
         
    
        
          title1 = Label(self.window, text="Number Plate Detection System", font=("times new roman",25,"bold"),bg="gray",fg="lemon chiffon").place(x=370, y=50)
        

          self.browse = Button(self.window,text="Browse Image",command= self.browse,font=("times new roman",18, "bold"),bd=0,cursor="hand2",bg="SkyBlue2",fg="lemon chiffon").place(x=500,y=450,width=180)
          self.analysis = Button(self.window,text="Analysis Image",command= main,font=("times new roman",18, "bold"),bd=0,cursor="hand2",bg="SkyBlue2",fg="lemon chiffon").place(x=500,y=510,width=180)
          self.redirect = Button(self.window,text="Registration",command= self.register,font=("times new roman",18, "bold"),bd=0,cursor="hand2",bg="SkyBlue2",fg="lemon chiffon").place(x=500,y=570,width=180)



    def register(self):
         self.window.destroy()
       
         from home_page import home_page
         root = Tk()
         obj = home_page(root)
         root.mainloop()

    
        
    def browse(self):
        global fileName
        dirPath = "LicPlateImages"
        fileList = os.listdir(dirPath)  
        fileName = askopenfilename(initialdir=r'C:\Users\DELL\Downloads\Licence plate detection\Module_1\LicPlateImages', title='Select image for analysis ',
                                filetypes=[('image files', '.jpg'),('image files', '.jpeg'),('image files', '.png')])

   
        load = Image.open(fileName)
        render = ImageTk.PhotoImage(load)
        img = tk.Label(image=render, height="290", width="480")
        img.image = render
        img.place(x=350, y=150)
        
        #### module level variables ##########################################################################
SCALAR_BLACK = (0.0, 0.0, 0.0)
SCALAR_WHITE = (255.0, 255.0, 255.0)
SCALAR_YELLOW = (0.0, 255.0, 255.0)
SCALAR_GREEN = (0.0, 255.0, 0.0)
SCALAR_RED = (0.0, 0.0, 255.0)

showSteps = False

###################################################################################################
def main():
 
    global fileName
    global licPlate
 
    blnKNNTrainingSuccessful = DetectChars.loadKNNDataAndTrainKNN()         # attempt KNN training

    if blnKNNTrainingSuccessful == False:                               # if KNN training was not successful
        print("\nerror: KNN traning was not successful\n")  # show error message
        return                                                          # and exit program
    # end if
    imageName = str(fileName)
    imgOriginalScene  = cv.imread(imageName, 1)            

    if imgOriginalScene is None:                            # if image was not read successfully
        print("\nerror: image not read from file \n\n")  # print error message to std out
        os.system("pause")                                  # pause so user can see error message
        return                                              # and exit program
    # end if

    listOfPossiblePlates = DetectPlates.detectPlatesInScene(imgOriginalScene)           # detect plates

    listOfPossiblePlates = DetectChars.detectCharsInPlates(listOfPossiblePlates)        # detect chars in plates

    cv.imshow("imgOriginalScene", imgOriginalScene)            # show scene image

    if len(listOfPossiblePlates) == 0:                          # if no plates were found
        print("\nno license plates were detected\n")  # inform user no plates were found
    else:                                                       # else
                # if we get in here list of possible plates has at leat one plate

                # sort the list of possible plates in DESCENDING order (most number of chars to least number of chars)
        listOfPossiblePlates.sort(key = lambda possiblePlate: len(possiblePlate.strChars), reverse = True)

                # suppose the plate with the most recognized chars (the first plate in sorted by string length descending order) is the actual plate
        licPlate = listOfPossiblePlates[0]

        cv.imshow("imgPlate", licPlate.imgPlate)           # show crop of plate and threshold of plate
           
        cv.imshow("imgThresh", licPlate.imgThresh)
      
        if len(licPlate.strChars) == 0:                     # if no chars were found in the plate
            print("\nno characters were detected\n\n")  # show message
            return                                          # and exit program
        # end if

        drawRedRectangleAroundPlate(imgOriginalScene, licPlate)             # draw red rectangle around plate
        print("----------------------------------------")
        print("RC Details")
        print("----------------------------------------")
        print("license plate read from image = " + licPlate.strChars + "\n")  # write license plate text to std out
                      
        
        no=licPlate.strChars
        
        connection=pymysql.connect(host="localhost",user="root",password="root",database="user_database")
        cur = connection.cursor()
        cur.execute("select * from user_register where NoPlate=%s",no)
        row=cur.fetchone()
        if row == None:
            print("not registered")
            messagebox.showerror("Error!", "This number is not registered")
        else:      
            root=Toplevel()
            root.title("Rc details")
            root.geometry("400x440+450+200")
            root.config(bg="lemon chiffon")
            root.focus_force()
            root.grab_set()
            
            
            l1 = Label(root, text="First name:", font=("times new roman",20,"bold"),bg="white", fg="maroon").place(x=10, y=10)
            l2 = Label(root, text="Last name:", font=("times new roman",20,"bold"),bg="white", fg="maroon").place(x=10, y=50)
            l3 = Label(root, text="Mobile number:", font=("times new roman",20,"bold"),bg="white", fg="maroon").place(x=10, y=90)
            l4 = Label(root, text="City:", font=("times new roman",20,"bold"),bg="white", fg="maroon").place(x=10, y=130)

            t1 = Label(root, text=row[0], font=("times new roman",16,"bold"),bg="white", fg="DodgerBlue4").place(x=160, y=15)
            t2 = Label(root, text=row[1], font=("times new roman",16,"bold"),bg="white", fg="DodgerBlue4").place(x=160, y=55)
            t3 = Label(root, text=row[2], font=("times new roman",16,"bold"),bg="white", fg="DodgerBlue4").place(x=210, y=95)
            t4 = Label(root, text=row[3], font=("times new roman",16,"bold"),bg="white", fg="DodgerBlue4").place(x=120, y=135)
        
            connection.close()
        
        
        
        
        writeLicensePlateCharsOnImage(imgOriginalScene, licPlate)           # write license plate text on the image

        cv.imshow("imgOriginalScene", imgOriginalScene)                # re-show scene image
        if cv.waitKey(0) & 0xFF == ord('q'):
            cv.destroyAllWindows()


        cv.imwrite("imgOriginalScene.png", imgOriginalScene)           # write image out to file

    cv.waitKey(0)					# hold windows open until user presses a key

    return



                
  
# end main

###################################################################################################
# def drawRedRectangleAroundPlate(imgOriginalScene, licPlate):

#     p2fRectPoints = cv2.boxPoints(licPlate.rrLocationOfPlateInScene)            # get 4 vertices of rotated rect

#     cv2.line(imgOriginalScene, tuple(p2fRectPoints[0]), tuple(p2fRectPoints[1]), SCALAR_RED, 2)         # draw 4 red lines
#     cv2.line(imgOriginalScene, tuple(p2fRectPoints[1]), tuple(p2fRectPoints[2]), SCALAR_RED, 2)
#     cv2.line(imgOriginalScene, tuple(p2fRectPoints[2]), tuple(p2fRectPoints[3]), SCALAR_RED, 2)
#     cv2.line(imgOriginalScene, tuple(p2fRectPoints[3]), tuple(p2fRectPoints[0]), SCALAR_RED, 2)
# # end function



def drawRedRectangleAroundPlate(imgOriginalScene, licPlate):
    # get 4 vertices of rotated rect
    p2fRectPoints = cv.boxPoints(licPlate.rrLocationOfPlateInScene)
    # convert float arrays to int tuples for use with cv2.line()
    p0 = (int(p2fRectPoints[0][0]), int(p2fRectPoints[0][1]))
    p1 = (int(p2fRectPoints[1][0]), int(p2fRectPoints[1][1]))
    p2 = (int(p2fRectPoints[2][0]), int(p2fRectPoints[2][1]))
    p3 = (int(p2fRectPoints[3][0]), int(p2fRectPoints[3][1]))
    # draw 4 red lines
    cv.line(imgOriginalScene, p0, p1, SCALAR_RED, 2)
    cv.line(imgOriginalScene, p1, p2, SCALAR_RED, 2)
    cv.line(imgOriginalScene, p2, p3, SCALAR_RED, 2)
    cv.line(imgOriginalScene, p3, p0, SCALAR_RED, 2)

###################################################################################################
def writeLicensePlateCharsOnImage(imgOriginalScene, licPlate):
    ptCenterOfTextAreaX = 0                             # this will be the center of the area the text will be written to
    ptCenterOfTextAreaY = 0

    ptLowerLeftTextOriginX = 0                          # this will be the bottom left of the area that the text will be written to
    ptLowerLeftTextOriginY = 0

    sceneHeight, sceneWidth, sceneNumChannels = imgOriginalScene.shape
    plateHeight, plateWidth, plateNumChannels = licPlate.imgPlate.shape

    intFontFace = cv.FONT_HERSHEY_SIMPLEX                      # choose a plain jane font
    fltFontScale = float(plateHeight) / 30.0                    # base font scale on height of plate area
    intFontThickness = int(round(fltFontScale * 1.5))           # base font thickness on font scale

    textSize, baseline = cv.getTextSize(licPlate.strChars, intFontFace, fltFontScale, intFontThickness)        # call getTextSize

            # unpack roatated rect into center point, width and height, and angle
    ( (intPlateCenterX, intPlateCenterY), (intPlateWidth, intPlateHeight), fltCorrectionAngleInDeg ) = licPlate.rrLocationOfPlateInScene

    intPlateCenterX = int(intPlateCenterX)              # make sure center is an integer
    intPlateCenterY = int(intPlateCenterY)

    ptCenterOfTextAreaX = int(intPlateCenterX)         # the horizontal location of the text area is the same as the plate

    if intPlateCenterY < (sceneHeight * 0.75):                                                  # if the license plate is in the upper 3/4 of the image
        ptCenterOfTextAreaY = int(round(intPlateCenterY)) + int(round(plateHeight * 1.6))      # write the chars in below the plate
    else:                                                                                       # else if the license plate is in the lower 1/4 of the image
        ptCenterOfTextAreaY = int(round(intPlateCenterY)) - int(round(plateHeight * 1.6))      # write the chars in above the plate
    # end if

    textSizeWidth, textSizeHeight = textSize                # unpack text size width and height

    ptLowerLeftTextOriginX = int(ptCenterOfTextAreaX - (textSizeWidth / 2))           # calculate the lower left origin of the text area
    ptLowerLeftTextOriginY = int(ptCenterOfTextAreaY + (textSizeHeight / 2))          # based on the text area center, width, and height

            # write the text on the image
    cv.putText(imgOriginalScene, licPlate.strChars, (ptLowerLeftTextOriginX, ptLowerLeftTextOriginY), intFontFace, fltFontScale, SCALAR_YELLOW, intFontThickness)
# end function

###################################################################################################


if __name__ == "__main__":
    
    root = Tk()
    obj = gui(root)
    root.mainloop()

    # main()


















