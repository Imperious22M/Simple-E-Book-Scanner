from pynput import mouse
from pynput import keyboard
import pyautogui
import img2pdf
import time
import os
import threading

#This program prints the location on the screen of two mouse clicks after the trigger key is pressed on the keyboard
#Then the program will grab the number if pages (images) that you set it to and flip the pages automatically
#Finally it will make a pdf of all the images :)

#Variables for the entire program, only these are meant to be modified!!!
bookname = "Test Name"
numberOfPages = 120 # remember 1 whole "image" counts as 1 page
pageFlipSpeed = 4
pageTurnKey = "right" # This variable is based on pyautogui key mappings, see their documentation for details
pageReturnKey = "left" #Since the program does not hold focus of the mouse, pages will turn when measuging the windows, this key will be pressed 3 times to return to the first page
triggerKey = "c"


#variables store the trigger key that records the two mouse locations where 
#the trigger flag is set to true when the trigger key is pressed, then reset
triggerFlag = False
curKey = ""
clickCnt = 0

#variables to calculate, and store the width and height of the region on the screen
xCords = [0,0]
yCords = [0,0]
imageWidth = 0
imageHeight = 0

#These variables are threading events to stop the thread
#When the .set() function is callcced from the stopEvent object the thread stops (returns False)
#The lock variable is used for Mutex exclusion for the global variables (prevents race conditions)
stopEvent = threading.Event()
lock  = threading.Lock()

#on_click function is the callback function for the mouse listener
#it tells you where the two clicks were once the triggerFlag variable is set
#Resets the triggerFlag and the clicCnt variables after 2 clicks
def on_click(x, y, button, pressed):
    global clickCnt, triggerFlag, xCords, yCords, imageWidth, imageHeight

    if stopEvent.is_set():
        return False

    lock.acquire()
    if pressed and triggerFlag==True:
        locationStr = ["top right corner", "bottom left corner"]
        
        if button.name == 'left':
            print(f"Mouse clicked at ({x}, {y}), for {locationStr[clickCnt]}")
            xCords[clickCnt] = x
            yCords[clickCnt] = y
       
        clickCnt+=1 

        if clickCnt==2:
            imageWidth = xCords[1]-xCords[0]
            imageHeight = yCords[1]-yCords[0]
            print(f"Box width: {imageWidth}, height {imageHeight}")
            clickCnt = 0
            triggerFlag = False

    lock.release()

#on_press function is the callback function for the keyboard listener
#It sets the trigger flag to true when the triggerKey is encountered
def on_press(key):
    global triggerFlag,curKey

    if stopEvent.is_set():
        return False

    if hasattr(key,'char') and key.char == triggerKey:
        print("Trigger pressed")
        lock.acquire()
        curKey = key
        triggerFlag = True
        lock.release()

#Instantiates the keyboard and mouse listeners
keyboardListener = keyboard.Listener(on_press=on_press)
mouseListener = mouse.Listener(on_click=on_click)
#Starts the listeners in the background
print("Listeners started")
keyboardListener.start()
mouseListener.start()

#Runs the program for until the width and height of the image is found
while imageHeight==0 or imageWidth ==0:
    pass

#Once image width is captured, sets the stopEvent and allows the thread to return and stop
stopEvent.set()        

#From here on the program will take a screenshot of the area clicked and store it
#It will also flip the pages by activating the key specified in pageTurnKey
for num in range(0,5):
    pyautogui.press(pageReturnKey)
    time.sleep(pageFlipSpeed)

for index,page in enumerate(range(0,numberOfPages)):
    pyautogui.screenshot(region=(xCords[0], yCords[0], imageWidth, imageHeight)).save(f"images/{index}.png")
    pyautogui.press(pageTurnKey)
    time.sleep(pageFlipSpeed) # just use if needed, can also be augmented by using random, though it is a basic method

#Once all the images have been taken, make a PDF of the images
with open(f"{bookname}.pdf", "wb") as pdf:
    pdf.write(img2pdf.convert(["images/"+str(img)+".png" for img in range(0,numberOfPages)]))
