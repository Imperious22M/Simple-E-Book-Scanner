# Simple-E-Book-Scanner
This is a simple Python E-Book scanner that will automatically take pictures of an ebook, flip the pages, and convert them to PDF format. It requires pynput, pyautogui and the img2pdf python libraries.

The program must be run from a directory that contains a folder called "images" This folder will contain the images and the PDF created by the program.

### Important details
Make sure to change the first 6 variables of the program to the values required. Otherwise your PDF will have the wrong name or the page will not turn.

### To use the program
1) Download and run the program from a directory with a folder named "images"
2) Once the program is running, press "C" to activate "capture mode" In this mode the first right mouse click will select the top left of the portion of the screen the program will capture, and the second right mouse click will select the bottom right of the screen capture area.
3) Once the program has detected the two mouse clicks, it will automatically calculate the area it needs to capture (as a rectangle) and then start taking pictures of the area it has calculated. It will automatically "flip" the page right a few times based on the pageReturnKey and pageFlipSpeed variables. Then it will "flip" the page left and start taking pictures automatically, and stop only when the picture count is the same as the number of pages indicated.
4) Once the pictures have been taken, the program will automatically create and save a PDF file in the images directory and exit.


