from tkinter import *
from PIL import Image, ImageTk

def main():
    root = Tk()
    root.title = ("Slot Machine")
    canvas = Canvas(root, width=1500, height=800)
    canvas.pack()

    im = Image.open("page_1.jpg")
    wheelw = im.size[0] #width of source image
    wheelh = im.size[1] #height of source image
    showsize = 400 #amount of source image to show at a time - part of 'wheel' you can see
    speed = 3 #spin speed of wheel
    bx1 = 250 #Box 1 x - where the box will appear on the canvas
    by = 250 #box 1 y
    numberofspins = 100  #spin a few times through before stopping

    cycle_period = 0  #amount of pause between each frame

    for spintimes in range(1,numberofspins):
        for y in range(wheelh,showsize,-speed):  #spin to end of image, from bottom to top

            cropped = im.crop((0, y-showsize, wheelw, y))  #crop which part of wheel is seen
            tk_im = ImageTk.PhotoImage(cropped)
            canvas.create_image(bx1, by, image=tk_im)  #display image

            canvas.update()                 # This refreshes the drawing on the canvas.
            canvas.after(cycle_period)       # This makes execution pause

        for y in range (speed,showsize,speed):  #add 2nd image to make spin loop
            cropped1 = im.crop((0, 0, wheelw, showsize-y)) #img crop 1
            cropped2 = im.crop((0, wheelh - y, wheelw, wheelh)) #img crop 2
            tk_im1 = tk_im2 = None
            tk_im1 = ImageTk.PhotoImage(cropped1)
            tk_im2 = ImageTk.PhotoImage(cropped2)

            #canvas.delete(ALL)
            canvas.create_image(bx1, by, image=tk_im2)  ###THIS IS WHERE THE PROBLEM IS..
            canvas.create_image(bx1, by + y, image=tk_im1)  ###PROBLEM

            #For some reason these 2 lines are overdrawing where they should be.  as y increases, the cropped img size should decrease, but doesn't

            canvas.update()                 # This refreshes the drawing on the canvas
            canvas.after(cycle_period)       # This makes execution pause

    root.mainloop()

if __name__ == '__main__':
    main()