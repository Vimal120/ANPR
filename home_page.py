# -*- coding: utf-8 -*-

from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
import pymysql, os

class home_page:
    def __init__(self, root):
         self.window = root
         self.window.title("Welcome to Number Plate Detection System")
         self.window.geometry("1280x900+0+0")
         self.window.config(bg = "lemon chiffon")
         
         self.bg_img = ImageTk.PhotoImage(file="img1.jpg")
         background = Label(self.window,image=self.bg_img).place(x=0,y=0,relwidth=1,relheight=1)
      
         frame = Frame(self.window, bg="white")
         frame.place(x=350,y=100,width=500,height=550)
         
         title1 = Label(frame, text="Car Number Plate Detection System", font=("times new roman",22,"bold"),bg="gray",fg="lemon chiffon").place(x=20, y=30)
         title2 = Label(frame, text="Registration", font=("times new roman",20,"bold"),bg="White",fg="LightSteelBlue4").place(x=20, y=100)

         f_name = Label(frame, text="First name", font=("helvetica",15,"bold"),bg="white").place(x=20, y=170)
         l_name = Label(frame, text="Last name", font=("helvetica",15,"bold"),bg="white").place(x=240, y=170)
         
         self.fname_txt = Entry(frame,font=("arial"))
         self.fname_txt.place(x=20, y=200, width=200)

         self.lname_txt = Entry(frame,font=("arial"))
         self.lname_txt.place(x=240, y=200, width=200)
         
         mblno = Label(frame, text="Mobile number", font=("helvetica",15,"bold"),bg="white").place(x=20, y=250)

         self.mblno_txt = Entry(frame,font=("arial"))
         self.mblno_txt.place(x=20, y=280, width=200)

         city = Label(frame, text="City", font=("helvetica",15,"bold"),bg="white").place(x=240, y=250)

         self.city_txt = Entry(frame,font=("arial"))
         self.city_txt.place(x=240, y=280, width=200)


         NoPlate = Label(frame, text="Enter vehicle number", font=("helvetica",15,"bold"),bg="white").place(x=20, y=330)

         self.NoPlate_txt = Entry(frame,font=("arial"))
         self.NoPlate_txt.place(x=20, y=360, width=250)

  
         self.search = Button(frame,text="Submit",command=self.submit,font=("times new roman",18, "bold"),bd=1,cursor="hand2",bg="SkyBlue2",fg="lemon chiffon").place(x=120,y=410,width=210)
         self.search = Button(frame,text="Already register",command=self.redirect_window_main,font=("times new roman",18, "bold"),bd=1,cursor="hand2",bg="SkyBlue2",fg="lemon chiffon").place(x=120,y=470,width=210)

    
    def submit(self):
        if self.fname_txt.get()=="" or self.lname_txt.get()=="" or self.mblno_txt.get()=="" or self.city_txt.get()=="" or self.NoPlate_txt.get()=="": 
            messagebox.showerror("Error!","Sorry!, All fields are required",parent=self.window)

        else:
            try:
                connection = pymysql.connect(host="localhost", user="root", password="root", database="user_database")
                cur = connection.cursor()
                cur.execute("select * from user_register where NoPlate=%s",self.NoPlate_txt.get())
                row=cur.fetchone()

                #Check if entered email id is already exists or not.
                if row!=None:
                    messagebox.showerror("Error!","Number plate is already exists",parent=self.window)
                else:
                    cur.execute("insert into user_register (f_name,l_name,mblno,city,NoPlate) values(%s,%s,%s,%s,%s)",
                                    (
                                        self.fname_txt.get(),
                                        self.lname_txt.get(),
                                        self.mblno_txt.get(),
                                        self.city_txt.get(),
                                        self.NoPlate_txt.get()
                                    ))
                    connection.commit()
                    connection.close()
                    messagebox.showinfo("Congratulations!","Register Successful",parent=self.window)
                    self.redirect_window_main()
                    self.reset_fields()
            except Exception as e:
                messagebox.showerror("Error!",f"Error due to {str(e)}",parent=self.window)

    def reset_fields(self):
        self.fname_txt.delete(0, END)
        self.lname_txt.delete(0, END)
        self.mblno_txt.delete(0, END)
        self.city_txt.current(0)
        self.NoPlate_txt.delete(0, END)
        
    
    def redirect_window_main(self):
         self.window.destroy()
      
         from Main import gui
         root = Tk()
         obj = gui(root)
         root.mainloop()


if __name__ == "__main__":
    root = Tk()
    obj = home_page(root)
    root.mainloop()
 