
from tkinter import  *
from tkinter import filedialog
import os
import subprocess as sub

root1=None
chk=None
t1=None
#globals



def main():
    global root
    try:
        root1.destroy()
    except:
        print("no root1")
    root = Tk()
    root.title("FACE AND GESTURE RECOGNITION")
    root.geometry('500x500')
    tkvar = StringVar(root)
    choices = { 'Picture','video_file','web cam'}
    tkvar.set('Picture') # set the default option

    popupMenu = OptionMenu(root, tkvar, *choices)

    A=Label(root, text="Choose any to find faces \n From any desired place")

    '''
    but1=Button(root1, text='Exit application', width=15, command=exiting)
    but1.place(relx=0.5, rely=0.65, anchor=CENTER)
'''
    #A.pack(expand=0)
    #popupMenu.pack(expand=1)


    B=Label(root, text="Choose the below option to \nrecognize a person based on gesture")

    tkvar1 = StringVar(root)
    choices1 = { 'Gesture Recognition'}
    tkvar1.set('Gesture Recognition') # set the default option

    popupMenu1 = OptionMenu(root, tkvar1, *choices1)

    #But=Button(root1, text='Use Gesture Recognition', width=25, command=gest)


    A.place(relx=0.5, rely=0.3, anchor=CENTER)
    #A.place(padx=10,pady=10,anchor=CENTER)
    #A.grid(padx=10,row=1,column=1,)
    popupMenu.place(relx=0.5, rely=0.4, anchor=CENTER)
    #popupMenu.grid(padx=5,row=1,column=2)

    B.place(relx=0.5,rely=0.5,anchor=CENTER)
    #But.place(relx=0.5,rely=0.6,anchor=CENTER)
    popupMenu1.place(relx=0.5,rely=0.6,anchor=CENTER)

    def change_dropdown(*args):
        print( tkvar.get())
        if tkvar.get() == 'Picture':
            print(f"doing {tkvar.get()}")
            show_picture()
        elif tkvar.get() == 'video_file':
            print(f"doing {tkvar.get()}")
            show_video()
        elif tkvar.get() == 'web cam':
            print(f'web cam running')
            show_webcam()
    
    def change_ges(*args):
        if tkvar1.get() == 'Gesture Recognition':
            print('Gesture Recognition running')
            gest()


        
    tkvar.trace('w', change_dropdown)
    tkvar1.trace('w', change_ges)
    root.mainloop()

def gest():
    root.destroy()
    global root1,chk
    #root1 = Toplevel(root)
    root1=Tk()
    root1.geometry('400x400')
    root1.title("Gesture")
    l1=Label(root1,text ='Updating')
    l2=Label(root1, text='enter the lable')
    global t1
    t1=Text(root1,width=10,height=1)
    b1=Button(root1, text='Click to run the updater', width=25, command=gest1)
    l3=Label(root1,text='Prediction')
    b2=Button(root1,text='click to Predict',width=25,command=gest2)
    
    l1.place(relx=.3,rely=.2,anchor=CENTER)
    l2.place(relx=.4,rely=.3,anchor=CENTER)
    t1.place(relx=.6,rely=.3,anchor=CENTER)
    b1.place(relx=.5,rely=.4,anchor=CENTER)
    l3.place(relx=.3,rely=.5,anchor=CENTER)
    b2.place(relx=.5,rely=.6,anchor=CENTER)



    '''l1.pack(pady=10,padx=8)
    l2.pack(pady=0,padx=10)
    t1.pack(pady=10,padx=10)
    b1.pack(pady=10,padx=10)
    l3.pack(pady=10,padx=8)
    b2.pack(pady=10,padx=10)'''


    b3=Button(root1, text='go back', width=25, command=main)
    b3.place(relx=.5,rely=.7,anchor=CENTER)
    #b3.pack(pady=10, padx=10)
    #root1.mainloop()


def gest1():
    print(t1.get("1.0","end-1c"))
    os.system(f'python tf-pose-estimation/update.py --name {t1.get("1.0","end-1c")}')
def gest2():
    os.system('python tf-pose-estimation/train_pred.py')


def show_picture():
    root.destroy()
    global root1,chk
    root1 = Tk()
    root1.geometry('400x400')
    root1.title("Picture")
    chk = IntVar()
    Checkbutton(root1, text="check the check box to train on new faces", variable=chk).pack(pady=10,padx=10)
    Label(root1,text="choose the location of the file for any single image").pack(pady=10,padx=10)
    b1=Button(root1, text='Click to Show the File', width=25, command=fileDialog)
    b1.pack(pady=10,padx=10)
    Label(root1, text="choose a folder location to check for all images")
    b2=Button(root1,text='select folder', width=25, command=fileDialog2)
    b2.pack(pady=10,padx=10)
    b3=Button(root1, text='go back', width=25, command=main)
    b3.pack(pady=10, padx=10)
    #root.destroy()

def show_video():
    root.destroy()
    global root1,chk
    root1 = Tk()
    root1.geometry('400x400')
    root1.title("Video")
    chk = IntVar()
    Checkbutton(root1, text="check the check box to train on new faces", variable=chk).pack(pady=10,padx=10)
    Label(root1,text="choose the location of the video file").pack(pady=10,padx=10)
    b1=Button(root1, text='Click to Show the File', width=25, command=fileDialog1)
    b1.pack(pady=10,padx=10)
    b2=Button(root1, text='go back', width=25, command=main)
    b2.pack(pady=10, padx=10)

def show_webcam():
    root.destroy()
    global root1,chk
    root1 = Tk()
    root1.geometry('400x400')
    root1.title("Video")
    chk = IntVar()
    Checkbutton(root1, text="check the check box to train on new faces", variable=chk).pack(pady=10,padx=10)
    b1=Button(root1, text='Click to Start', width=25, command=web_cam)
    b1.pack(pady=10,padx=10)
    b3=Button(root1, text='go back', width=25, command=main)
    b3.pack(pady=10, padx=10)
    #print("webcam",chk.get())

    '''
    root1 = Tk()
    root1.geometry('400x400')
    root1.title("V")
    Label(root1,text="choose the location of the video file").pack(pady=10,padx=10)
    b1=Button(root1, text='Click to Show the File', width=25, command=filedialog)
    b1.pack(pady=10,padx=10)
    root.destroy()'''

def fileDialog():

    filename = filedialog.askopenfilename(initialdir =  "/home/rahul/", title = "Select A File", filetypes=(("JPG ","*.jpg"),("png ","*.png"),("JPEG ","*.jpeg")))
    #label = Label(root1, text = "")
    #label.grid(column = 1, row = 2)
    #label.configure(text = filename)
    if(str(filename) == '()'):
        print("nothing selected")
    else:
        x=f'python face.py {filename} {chk.get()}'
        print(x)
        sub.run(x.split(" "))
'''
def des():
    root1.destroy()
    main()
'''
def fileDialog1():
    filename = filedialog.askopenfilename(initialdir =  "/home/rahul/", title = "Select A File", filetypes=(("MP4 ","*.mp4"),("AVI ","*.avi"),))
    if(str(filename) == '()'):
        print("nothing selected")
    else:
        x=f'python face_video.py -v {filename} {chk.get()}'
        print(x)
        sub.run(x.split(" "))

def fileDialog2():
    filename =filedialog.askdirectory()
    if(str(filename) == '()'):
        print("nothing selected")
    else:
        x=f'python face.py {filename} {chk.get()}'
        print(x)
        sub.run(x.split(" "))

def web_cam():
    x=f'python face_video.py -w {chk.get()}'
    print(x)
    sub.run(x.split(' '))



#fileDialog1()
main()
'''

import os
from tkinter import *
import subprocess as sub
import time
import pickle
from tkinter import filedialog
root = Tk()
root.title("FACE AND GESTURE RECOGNITION")
t=str()
#files={}
#v=''

        
    
def h(f,p,main):
    time.sleep(3)
    pass_manager(f,p)
    main.destroy()

def s(f,p,main):
    time.sleep(3)
    pass_checker(f,p)
    main.destroy()    

def lis(password,main):
    if(password=="123"):
        root1 = Tk()
        root1.geometry('300x300')
        l=Label(root1,text=str(ref()))
        l.pack(pady=10,padx=10)
        b1=Button(root1, text='Refresh', width=25, command=lambda:l.config(text=str(ref())))
        b1.pack(pady=10,padx=10)
        main.destroy()
    else:
        main.destroy()
        print("wrong password")   

def hide():
    root1 = Tk()
    root1.geometry('300x300')
    root1.title("Hide")
    Label(root1,text="enter the path of the file").pack(pady=10,padx=10)
    tb = Entry(root1)
    tb.pack(pady=10,padx=10)
    Label(root1,text="set a password for the file").pack(pady=10,padx=10)
    tb1 = Entry(root1)
    tb1.pack(pady=10,padx=10)
    b1=Button(root1, text='Click to Hide the File', width=25, command=lambda: h(tb.get(),tb1.get(),root1) )
    b1.pack(pady=10,padx=10)
    root.destroy()
    
    
def show():
    root1 = Tk()
    root1.geometry('300x300')
    root1.title("Show")
    Label(root1,text="enter the path of the file").pack(pady=10,padx=10)
    tb = Entry(root1)
    tb.pack(pady=10,padx=10)
    Label(root1,text="enter the password for the file").pack(pady=10,padx=10)
    tb1 = Entry(root1)
    tb1.pack(pady=10,padx=10)
    b1=Button(root1, text='Click to Show the File', width=25, command=lambda: s(tb.get(),tb1.get(),root1) )
    b1.pack(pady=10,padx=10)
    root.destroy()

def filelist():
    root1 = Tk()
    root1.geometry('300x300')
    root1.title("Files List")
    Label(root1,text="enter the password").pack(pady=10,padx=10)
    tb1 = Entry(root1)
    tb1.pack(pady=10,padx=10)
    b1=Button(root1, text='Click to Show the List', width=25, command=lambda: lis(tb1.get(),root1) )
    b1.pack(pady=10,padx=10)
    root.destroy()    
   


def show_picture():
	root1 = Tk()
    root1.geometry('400x400')
    root1.title("Picture")
    Label(root1,text="enter the path of the file").pack(pady=10,padx=10)
    tb = Entry(root1)
    tb.pack(pady=10,padx=10)
    Label(root1,text="enter the password for the file").pack(pady=10,padx=10)
    tb1 = Entry(root1)
    tb1.pack(pady=10,padx=10)
    b1=Button(root1, text='Click to Show the File', width=25, command=lambda: s(tb.get(),tb1.get(),root1) )
    b1.pack(pady=10,padx=10)
    root.destroy()

b1 = Button(root, text='Hide', width=25, command=hide) 
b1.pack(pady=10,padx=10) 
b2 = Button(root, text='Show', width=25, command=show) 
b2.pack(pady=10,padx=10)
b3 = Button(root, text='List Of Files Hidden', width=25, command=filelist)
b3.pack(pady=10,padx=10)

root.mainloop()


	
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
 
 
 
class Root(Tk):
    def __init__(self):
        super(Root, self).__init__()
        super()7675
        self.title("Python Tkinter Dialog Widget")
        self.minsize(640, 400)
        #self.wm_iconbitmap('icon.ico')
 
        self.labelFrame = ttk.LabelFrame(self, text = "Open File")
        self.labelFrame.grid(column = 0, row = 1, padx = 20, pady = 20)
 
        self.button()
 
 
 
    def button(self):
        self.button = ttk.Button(self.labelFrame, text = "Browse A File",command = self.fileDialog)
        self.button.grid(column = 1, row = 1)
 
 
    def fileDialog(self):
 
        self.filename = filedialog.askopenfilename(initialdir =  "/home/rahul/", title = "Select A File", filetypes=(("JPG ","*.jpg"),))
        self.label = ttk.Label(self.labelFrame, text = "")
        self.label.grid(column = 1, row = 2)
        self.label.configure(text = self.filename)
 
 
 
 
 
root = Root()
root.mainloop()
'''