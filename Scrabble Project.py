from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from PIL import ImageTk, Image
import time
import sys
import random
import datetime
import os
import pickle
import winsound
import pygame
from pygame import mixer
from random import shuffle
from pynput.keyboard import Key, Controller


# The line below is calling a file the contains all the required function to run this game:
# Please Enter the path:
exec(open("func2.0.py").read())



exec(open("func3.0.py").read())

# Titescore is a dictionary that holds the score of indivisual alphabet
Tilescore = {"A": 1, "B": 3, "C": 3, "D": 2,
             "E": 1, "F": 4, "G": 2, "H": 4,
             "I": 1, "J": 8, "K": 5, "L": 1,
             "M": 3, "N": 1, "O": 1, "P": 3,
             "Q": 10, "R": 1, "S": 1, "T": 1,
             "U": 1, "V": 4, "W": 4, "X": 8,
             "Y": 4, "Z": 10, "#": 0}

board = Tk()                    # Initialising Main Board(Window)
pygame.init()                   # Initialising pygame to use its mixer

POC = IntVar()                  # Player Of Challange
counter = 1                     # Player Of Turn
TNOT = 0                        # Total No. Of Turns
nop = 4                         # No. Of Players
skip = 0                        # Player who's turn is going to get skipped.
# Flag Check For Wather  the words built in cross are valid or not
crossflag = 'True'
direction = IntVar()            # Direction in which the word is being played
racktemp = []                   # Temp. rack of Turn Player
# List conatins what letters was been used to subsitute a blank tile
blank = []
# List holding Player names and their respective scores
pname = ['', '', '', '', '']
tiles = {}                      # Racks placment on GUI is handled by tiles
# The whole board and its cordinates are accessed by grid dictionary
grid = {}
tempscore = 0                   # Temp. score calculated per turn before the turn finishes
tempword = ''
# How many Double word scores has been activated in a single turn
dw = 0
# How many Triple word scores has been activated in a single turn
tw = 0
# Which letters will be awarded Double score for a single turn
dl = []
# Which letters will be awarded Triple score for a single turn
tl = []
# Statistic analysis: list holds max score scored in a single turn adn its scorer
maxscore = [-1, "", ""]
conflag = False                 # Triggers when continue game is selected
start = time.time()  # start time of the game is

# Controller function is declared over a variable Keyboards
keyboard = Controller()
# This alters the default protocol of a Windows OS default window. When click the cross, instead of closing the game it will now call a function.
board.protocol('WM_DELETE_WINDOW', quit_func)

# Key binding: Control+s will result in shuffling the rack for the player
board.bind('<Control-z>', shuff_func)

# Key binding: Control+c on word space will result in clearing it out.
board.bind('<Control-c>', wordfunc)

# Key binding: Enter key will submit your turn
board.bind('<Return>', lambda event: change_turn(skip, nop))

# click sound
board.bind('<Button-1>', buttonclick)

# Key binding: Skip turn:
board.bind('<Control-t>', lambda event: change_turn(counter, nop))

# Key binding: Direction Down
board.bind('<Control-d>', down)

# Key binding: Direction Right
board.bind('<Control-r>', right)

# Key binding: Finish game
board.bind('<Control-Return>', lambda event: finish(pname))

# key binding: savegame
board.bind('<Control-s>', savegame)

# Changing Titlename and logo:
board.iconbitmap('Scrabble logo.ico')
board.title('Play Scrabble: Family Edition')
board.state('zoomed')

# Creating Scrabble Body/Grid/Board:
for x in range(15):
    for y in range(15):
        if (x, y) == (7, 7):

            but = Button(board, text='X', height=2, width=5,
                         borderwidth=5, bg='yellow', fg='black')
            but.grid(row=x+1, column=y)
            grid[(x, y)] = but
        elif (x, y) == (0, 0) or (x, y) == (0, 7) or (x, y) == (0, 14) or (x, y) == (7, 0) or (x, y) == (7, 14) or (x, y) == (14, 0) or (x, y) == (14, 7) or (x, y) == (14, 14):

            but = Button(board, text='TWS', height=2, width=5,
                         borderwidth=5, bg='red', fg='white')
            but.grid(row=x+1, column=y)
            grid[(x, y)] = but

        elif (x, y) == (1, 1) or (x, y) == (2, 2) or (x, y) == (3, 3) or (x, y) == (4, 4) or (x, y) == (10, 10) or (x, y) == (11, 11) or (x, y) == (12, 12) or (x, y) == (13, 13) or (x, y) == (1, 13) or (x, y) == (2, 12) or (x, y) == (3, 11) or (x, y) == (4, 10) or (x, y) == (10, 4) or (x, y) == (11, 3) or (x, y) == (12, 2) or (x, y) == (13, 1):

            but = Button(board, text='DWS', height=2, width=5,
                         borderwidth=5, bg='grey', fg='white')
            but.grid(row=x+1, column=y)
            grid[(x, y)] = but

        elif (x, y) == (0, 3) or (x, y) == (0, 11) or (x, y) == (2, 6) or (x, y) == (2, 8) or (x, y) == (3, 0) or (x, y) == (3, 7) or (x, y) == (3, 14) or (x, y) == (6, 2) or (x, y) == (6, 6) or (x, y) == (6, 8) or (x, y) == (6, 12) or (x, y) == (7, 3) or (x, y) == (7, 11) or (x, y) == (14, 3) or (x, y) == (14, 11) or (x, y) == (12, 6) or (x, y) == (12, 8) or (x, y) == (11, 0) or (x, y) == (11, 7) or (x, y) == (11, 14) or (x, y) == (8, 2) or (x, y) == (8, 6) or (x, y) == (8, 8) or (x, y) == (8, 12):
            but = Button(board, text='DLS', height=2, width=5,
                         borderwidth=5, bg='blue', fg='white')
            but.grid(row=x+1, column=y)
            grid[(x, y)] = but

        elif (x, y) == (1, 5) or (x, y) == (1, 9) or (x, y) == (5, 1) or (x, y) == (5, 5) or (x, y) == (5, 9) or (x, y) == (5, 13) or (x, y) == (13, 5) or (x, y) == (13, 9) or (x, y) == (9, 1) or (x, y) == (9, 5) or (x, y) == (9, 9) or (x, y) == (9, 13):

            but = Button(board, text='TLS', height=2, width=5,
                         borderwidth=5, bg='green', fg='white')
            but.grid(row=x+1, column=y)
            grid[(x, y)] = but

        else:
            but = Button(board, text='', height=2, width=5,
                         borderwidth=5, bg='#f2c4b1', fg='white')
            but.grid(row=x+1, column=y)
            grid[(x, y)] = but


# Info updated after generation of board:
# Temp hold the bg and fg color of each tile after its been selected;
# Its default value is setted according to position 7,7(center of the board)
temp = ['white', 'black']

# Yellow holds the color value of the pointer.
# When a tile is selected, its color values are change to whats being hold in Yellow
yellow = ['yellow', 'black']

# Details hold the vital info thats being presented on the board,
# the info of the selected tile. Its default value is setted according to position 7,7(center of the board)
details = [7, 7, grid[(7, 7)].cget('text')]

# Top Menu Bar:
topbar = Menu(board)
board.config(menu=topbar)

# File Option:
file = Menu(topbar, tearoff=0)
topbar.add_cascade(label='File', menu=file)
file.add_command(label='New Game', command=newgame)
file.add_separator()
file.add_command(label='Save Game           <Ctrl + S>', command=savegame)
file.add_separator()
file.add_command(label='Exit                <Alt + F4>', command=quit_func)

# Player Commands:
pcmd = Menu(topbar, tearoff=0)
topbar.add_cascade(label='Player Options', menu=pcmd)
pcmd.add_command(label='Submit Data                               <Enter>',
                 command=lambda: change_turn(skip, nop))
pcmd.add_separator()
pcmd.add_command(
    label='Shuffle Tray                              <Ctrl + Z>', command=shuff_func)
pcmd.add_separator()
pcmd.add_command(label='Skip Turn                                 <Ctrl + T>',
                 command=lambda: change_turn(counter, nop))
pcmd.add_separator()
pcmd.add_command(
    label='Clear Writing box                     <Ctrl + C>', command=wordfunc)
pcmd.add_separator()
pcmd.add_command(
    label='Select Downwards                  <Ctrl + D>', command=down)
pcmd.add_separator()
pcmd.add_command(
    label='Select Rightwards                     <Ctrl + R>', command=right)
pcmd.add_separator()
pcmd.add_command(label='End Match                         <Ctrl + Enter>',
                 command=lambda: finish(pname))

# Help Option:
helper = Menu(topbar, tearoff=0)
topbar.add_cascade(label='Help', menu=helper)
helper.add_command(label='Instructions', command=call_ins)
helper.add_separator()
helper.add_command(label='Contact', command=contact)
helper.add_separator()
helper.add_command(label='On-Screen Keyboard', command=open_osk)
helper.add_separator()
helper.add_command(label='Turn Off Background Music', command=stop_music)
helper.add_separator()
helper.add_command(label='Turn On Background Music', command=play_music)


# Score Board Frame:
scoreframe = LabelFrame(board, text='Welcome:')
scoreframe.grid(row=1, column=15, rowspan=3, columnspan=3, sticky=W+E, padx=10)

Player1 = Label(
    scoreframe, text='The minds behind the recreation of this GUI based Scrabble are:')
Player1.grid(row=0, column=0)

if len(pname) >= 3:
    Player2 = Label(
        scoreframe, text='Ramis Raza, Hussain Abbas, Muhammad Jawwad, Hamna Jamil and Muhammad Mehdi Raza')
    Player2.grid(row=1, column=0)

if len(pname) >= 4:
    Player3 = Label(scoreframe, text='It\'s recommended to have a resolution of 1366*768 and \n place your taskbar to the right-side of your screen for optimal UI experience.')
    Player3.grid(row=2, column=0)

if len(pname) == 5:
    Player4 = Label(
        scoreframe, text='Hope you enjoy the game, and if there is any room for imporvemnt do let us know :)')
    Player4.grid(row=3, column=0)

# Letter bag is generated and it will contain all the tiles which will be distributed through out the game
bag = generate_bag()

# Home Screen is called; there you get many options to access as NEWGAME, HIGHSCORE, INSTRUCTIONS and etc.
mixer.music.load("Good_Starts.wav")
mixer.music.play(-1)
home()
scoreboard()

# Time Clock:
status = Label(board, text="v1.0", bd=1, relief=SUNKEN, anchor=W)
status.grid(row=16, column=0, columnspan=10, sticky=W)
tick()

# Racks are being generated for all players, 7 tiles per player
if conflag == False:
    all_tiles = generating_racks(nop, bag)
print(all_tiles)

if len(pname) < 3:
    Player2.destroy()

if len(pname) < 4:
    Player3.destroy()

if len(pname) < 5:
    Player4.destroy()


# Generating Radio Buttons and its frame For Direction of the word:
direction.set(0)  # Setting default value for direction button
direcframe = LabelFrame(board, text='Select Your Prefered Direction:')
direcframe.grid(row=5, column=15, rowspan=2, columnspan=3, padx=10, sticky=W+E)

Radiobutton(direcframe, text='Downwards', variable=direction,
            value=1).grid(row=0, column=0)
Radiobutton(direcframe, text='Rightwards',
            variable=direction, value=2).grid(row=1, column=0)


# Binding Mouse left click to grid dictionary + color preserve:
for a in range(15):
    for b in range(15):
        grid[(a, b)].bind("<Button-1>", click)
        grid[(a, b)].bind("<Button-3>", point)


# End Of Match Button:
match_but = Button(board, text='End Match', height=2, width=30,
                   borderwidth=5, bg='black', fg='white', command=lambda: finish(pname))
match_but.grid(row=15, column=15, padx=10, sticky=W+E)
match_but.bind('<Enter>', buttonhover)


# Shuffle Button:
shuff_but = Button(board, text='Shuffle Tray', height=2,
                   width=13, borderwidth=5, command=shuff_func, bg='white')
shuff_but.grid(row=14, column=15, padx=10, sticky=E)
shuff_but.bind('<Enter>', buttonhover)


# Skip Turn Button and func:
skip_but = Button(board, text='Skip Turn', height=2, width=15, borderwidth=5,
                  bg='black', fg='white', command=lambda: change_turn(counter, nop))
skip_but.grid(row=13, column=15, padx=10, sticky=E)
skip_but.bind('<Enter>', buttonhover)


# On screen keyboard button
Onkey = Button(board, text='On-Screen Keyboard', height=2, width=17, borderwidth=5,
               bg='white', fg='black', command=open_osk)
Onkey.grid(row=14, column=15, padx=10, sticky=W)
Onkey.bind('<Enter>', buttonhover)


# Text box for word:
word = Entry(board, width=8, font=('DJB Letter Game Tiles', 20))
word.insert(0, 'Word Here')
word.grid(row=7, column=15, columnspan=10, sticky=W+E, padx=10)
# Key binding: Mouse left click on word space will result in clearing it out.
word.bind("<Button-3>", wordfunc)

# Player Tile:
tile_frame = LabelFrame(board, text='Player Tiles:')
tile_frame.grid(row=8, column=15, padx=10, rowspan=3, columnspan=3, sticky=W+E)
inserting_letters_into_player_tiles(all_tiles[0])

# Player Turn Alert frame and lable:
name_frame = LabelFrame(board, text='Player To Turn')
name_frame.grid(row=4, column=15, columnspan=3, padx=10, sticky=W+E)
name_dispaly = Label(name_frame, text=pname[counter][0]+'; It\'s your turn')
name_dispaly.grid(row=0, column=0, sticky=W)

# Submiting Details:
detail_frame = LabelFrame(board, text='Details of Submission:', pady=10)
detail_frame.grid(row=10, column=15, padx=10,
                  rowspan=3, columnspan=3, sticky=W+E)
detail_label = Label(detail_frame, text=details)
detail_label.grid(row=0, column=0, sticky=W)

# Submiting Details label:
detail_label2 = Label(
    detail_frame, text='--> This the cell you have selected.')
detail_label2.grid(row=0, column=1, sticky=E, padx=5)


# Writing a dictionary to a list for faster access:
class Node:
    def __init__(self, val: str) -> None:
        self._left = None
        self._right = None
        self._value = val

class Pagoda:
   def __init__(self):
      self._root:Node = None
   
   def is_empty(self):
      if self._root == None:
         return True
      return False

   def clear(self):
      self._root = None

   def Merge(self, root: Node, newnode: Node):
      if root == None:
         return newnode
      elif newnode == None:
         return root
      else:
         bottomroot: Node = root._right
         root._right = None
         bottomnew: Node = newnode._left
         newnode._left = None
         r:Node = None
         temp:Node = None

         while (bottomroot != None and bottomnew != None):
            if bottomroot._value < bottomnew._value:
               temp = bottomroot._right
               if r == None:
                  bottomroot._right = bottomroot
               else:
                  bottomroot._right = r._right
                  r._right = bottomroot
               
               r = bottomroot
               bottomroot = temp
            else:
               temp = bottomnew._left
               if r == None:
                  bottomnew._left = bottomnew
               else:
                  bottomnew._left = r._left
                  r._left = bottomnew
               
               r = bottomnew
               bottomnew = temp
         
         if bottomnew == None:
            root._right = r._right
            r._right = bottomroot
            return root
         else:
            newnode._left = r._left
            r._left = bottomnew
            return newnode

   def search(self, a):
       start = self._root
       while self._root._left != start:
           if self._root._value == a:
               return True
           self._root = self._root._left
       return False

   def print_root(self):
        return self._root._value

        # a:Node = self._root._right
        # b:Node = self._root._left

        # print("right    ",a._value)
        # print("left    ",b._value)

   def insert_2(self, n: Node, root: Node):
      n._left = n
      n._right = n
      return self.Merge(root, n)

   def insert_1(self, val):
      n = Node(val)
      self._root = self.insert_2(n, self._root)

   def delete_1(self):
      self._root = self.delete_2(self._root)

   def delete_2(self, root :Node):
      L : Node = None
      R : Node = None
      if root == None:
         print("is empty:((")
         return None

      else:
         if root._left == root:
            L = None
         else:
            L = root._left
            while L._left != root:
               L = L._left
            
            L._left = root._left

         if root._right == root:
            R = None
         else:
            R = root._right
            while R._right != root:
               R = R._right
            
            R._right = root._right

         return self.Merge(L,R)

dic = Pagoda()
f = open('dic.txt', "r")
for line in f:
    dic.insert_1(line[0:(len(line)-1)])         
f.close()


# Submit Button:
submit_but = Button(board, text='Submit Data', height=2, width=15, borderwidth=5,
                    bg='black', fg='white', command=lambda: change_turn(skip, nop))
submit_but.grid(row=13, column=15, padx=10, sticky=W)
submit_but.bind('<Enter>', buttonhover)
# print(details)

# Habib logo is placed on the window:
img = ImageTk.PhotoImage(Image.open('sherpng.png'))
Label(board, image=img, anchor=W).grid(
    row=12, column=29, padx=10, rowspan=50, columnspan=50, sticky=W)

htp = LabelFrame(board, text='How To Play:')
htp.grid(row=1, column=30, columnspan=3,
         rowspan=15, padx=5, sticky=W+N, pady=20)
htpt = Label(htp, text='Here are some brief guidelines about the \ngame, to read complete set of instructions \nplease select "Instructions" from \ndrop down menu.\n\n1. Each Player will be notified of his/her\n turn form th alert box "Player To Turn".\n\n2. To play a turn, each player must\ncreate a word from his/her provided rack.\n\n3. The word must be typed in the\n entry box mentioning "Word Here".\n\n4. The word played must be valid or else\nother players can challenge it; losing\na challenge will result in skip turn penalty.\n\n5. Player must select the direction for\nthe word before finishing the turn.\n\n6. Clicking left mouse button on board\nwill result in change of pointers location.\n\n7. Clicking right mouse button on board\nwill result in same actions as left\nbutton click + the letter underneath\nthe cursor will be added to the entry box.\n\n8. Clicking right mouse button on text field\nwill clear it.')
htpt.grid(row=0, column=0, sticky=W)

if conflag == True:
    change_turn(counter, nop)
    conflag = False

board.mainloop()
