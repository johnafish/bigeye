bigeye
======
##Introduction
bigeye is an optical character recognition (ocr) tool built in Python 3.3.5. Feel free to mess around with it, but it's still buggy.

##How To Use
1. Install [pillow](https://github.com/python-imaging/Pillow). 
2. Take a picture of some letters, or a word, [i.e.](http://imgur.com/K1f9RH0). 
3. Run main.py.
4. Enter "l" when prompted if you would like to learn or check.
5. Enter the proper letters, case sensitive, into main.py.
6. Repeat steps 2-6 until you have all the letters in the alphabet.
7. Try checking, and checklearning, just to increase the size of your dictionary!

##How does it work?
If you truly want to understand how it works, I encourage you to read the code. But, to dumb it down:
>bigeye works by simulating a very basic neural network (if you can even call it that). First, the text is normalized to black and white at a set threshold - this eliminates any "gray" areas. Then, the bounding boxes of letters are found using rudimentary methods. Finally, the bounding box of each letter is broken up into a 10x10 grid, where each box in the grid has a value from 0-255 representing the average value in given box. These are recorded in the "dictionary" file. Further letters can be compared to those in the dictionary file to find out what is the "best fit" for the letter.

##To Do:
- Multiple line support
- Faster normalizing
- Space support

####Made by John Fish, 2014. Use with credit.