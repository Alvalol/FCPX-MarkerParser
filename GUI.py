from Tkinter import *
import tkFileDialog
import main


def askopenfile():
    miamimi =  tkFileDialog.askopenfilename(title='Chose a file')
    print miamimi



MainWin = Tk()
frame = Frame(MainWin, width=500,height=200)
MainWin.minsize(500,200)
MainWin.maxsize(500,200)
frame.pack()

browseButton = Button(frame,text="Browse",command=askopenfile)
browseButton.pack()





MainWin.mainloop()