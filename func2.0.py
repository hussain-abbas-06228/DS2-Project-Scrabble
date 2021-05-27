class Node1:
   def __init__(self, val: str, dat: str) -> None:
      self._left = None
      self._right = None
      self._value = val
      self._data = dat

class Pagoda1:
   def __init__(self):
      self._root:Node1 = None
   
   def is_empty(self):
      if self._root == None:
         return True
      return False

   def clear(self):
      self._root = None

   def Merge(self, root: Node1, newnode: Node1):
      if root == None:
         return newnode
      elif newnode == None:
         return root
      else:
         bottomroot: Node1 = root._right
         root._right = None
         bottomnew: Node1 = newnode._left
         newnode._left = None
         r:Node1 = None
         temp:Node1 = None

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

   def print_root(self):
      return ((self._root._value, self._root._data))
    #   a:Node = self._root._right
    #   b:Node = self._root._left

    #   print("right    ",a._value, a._data)
    #   print("left    ",b._value, b._data)

   def insert_2(self, n: Node1, root: Node1):
      n._left = n
      n._right = n
      return self.Merge(root, n)

   def insert_1(self, val, dat):
      n = Node1(val, dat)
      self._root = self.insert_2(n, self._root)

   def delete_1(self):
      self._root = self.delete_2(self._root)

   def delete_2(self, root :Node1):
      L : Node1 = None
      R : Node1 = None
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

   def sort_dic(self, inpt):
        lst = []
        dic = {}
        for x,y in  inpt.items():
            self.insert_1(y,x)

        while self.is_empty() == False:
            temp = self.print_root()
            self.delete_1()
            lst.append((temp[1],temp[0]))

        return lst



class NodeTree(object):

    def __init__(self, left=None, right=None):
        self.left = left
        self.right = right

    def children(self):
        return (self.left, self.right)

    def nodes(self):
        return (self.left, self.right)

    def __str__(self):
        return '%s_%s' % (self.left, self.right)

def huffman_code_tree(node, left=True, binString=''):
    if type(node) is str:
        return {node: binString}
    (l, r) = node.children()
    d = dict()
    d.update(huffman_code_tree(l, True, binString + '0'))
    d.update(huffman_code_tree(r, False, binString + '1'))
    return d

def compression(string):
    lst = []
    freq = {}
    for c in string:
        if c in freq:
            freq[c] += 1
        else:
            freq[c] = 1

    P = Pagoda1()

    freq = P.sort_dic(freq)

    nodes = freq

    while len(nodes) > 1:
        (key1, c1) = nodes[-1]
        (key2, c2) = nodes[-2]
        nodes = nodes[:-2]
        node = NodeTree(key1, key2)
        nodes.append((node, c1 + c2))

        nodes = sorted(nodes, key=lambda x: x[1], reverse=True)

    huffmanCode = huffman_code_tree(nodes[0][0])

    d = dict()
    for (char, frequency) in freq:
        d.update({char: huffmanCode[char]})
    lst.append(d)

    encoded_string = ''
    for char in string:
        encoded_string += d[char]
    lst.append(str(encoded_string))

    return lst

def huffman_decoding(encoded_string, codes):
    decoded_string = ''
    keys = list(codes.keys())
    values = list(codes.values())
    interchanged_dict = dict()
    for i in range(len(keys)):
        interchanged_dict.update({values[i]: keys[i]})
    temp = ''
    for char in encoded_string:
        if temp not in values:
            temp += char
        else:
            decoded_string += interchanged_dict[temp]
            temp = ''
            temp += char
    decoded_string += interchanged_dict[temp]
    return decoded_string

def titlescreen():          ##TopLevel Window(not main)
    title = Toplevel()
    title.title('Play Scrabble: Family Edition')
    title.iconbitmap('Scrabble logo.ico')
    title.grab_set()
    title.bind('<Button-1>', buttonclick)
    title.after(1, lambda: title.focus_force())

    ##Generating required frames:
    frame1 = LabelFrame(title,text = 'Select Number of Players')
    frame1.grid(row=0, column = 1,padx = 10,pady=10,sticky = N+S)

    frame2 = LabelFrame(title,text = 'Name The Players')
    frame2.grid(row=0, column = 10,padx = 10,pady=10,sticky = N+S)

    frame3 = LabelFrame(title,text = 'Select Game Mode')
    frame3.grid(row=1, column = 1,padx = 10,pady=10,sticky = W)

    ##This function enables and disables writing space for required no. of players
    def func(val):
        if val == 2:
            P3.config(state = DISABLED)
            P4.config(state = DISABLED)
        elif val == 3:
            P3.config(state = NORMAL)
            P4.config(state = DISABLED)
        elif val == 4:
            P3.config(state = NORMAL)
            P4.config(state = NORMAL)    

    ##Generation of writing space
    def wordfunc(event):
        event.widget.delete(0,END)
        event.widget.focus()

    #No. of Players (local)
    np = IntVar()
    np.set(2)

    ##Options is a list containing menu options.
    options = [2, 3, 4]
    Label(frame1,text ='Number of Players:').grid(row=1, column = 1, padx=5, pady=10)
    drop = OptionMenu(frame1, np, *options, command=func)
    drop.grid(row= 1, column = 2, padx=5, pady=10)
    drop.bind('<Enter>', buttonhover)

    ##Initialsing each writing space to each player
    Label(frame2,text= 'Player 1:').grid(row = 1, column = 5)
    P1 = Entry(frame2,width=10,font = ('DJB Letter Game Tiles',15))
    P1.grid(row = 1, column = 6,padx = 5, pady = 1)
    P1.insert(0, 'Player 1')
    P1.bind("<Button-1>",wordfunc)

    Label(frame2,text= 'Player 2:').grid(row = 2, column = 5)
    P2 = Entry(frame2,width=10, font = ('DJB Letter Game Tiles',15))
    P2.grid(row = 2, column = 6,padx = 5, pady = 1)
    P2.insert(0, 'Player 2')
    P2.bind("<Button-1>",wordfunc)

    Label(frame2,text= 'Player 3:').grid(row = 3, column = 5)
    P3 = Entry(frame2,width=10, font = ('DJB Letter Game Tiles',15))
    P3.grid(row = 3, column = 6,padx = 5, pady = 1)
    P3.insert(0, 'Player 3')
    P3.bind("<Button-1>",wordfunc)

    Label(frame2,text= 'Player 4:').grid(row = 4, column = 5)
    P4 = Entry(frame2,width=10, font = ('DJB Letter Game Tiles',15))
    P4.grid(row = 4, column = 6,padx = 5, pady = 1)
    P4.insert(0, 'Player 4')
    P4.bind("<Button-1>",wordfunc)

    P3.config(state = DISABLED)
    P4.config(state = DISABLED)

    ##Writing space if practice mode is activated
    def pracfunc(val):
        if val == 1:
            np.set(2)
            drop.config(state = NORMAL)
            P2.config(state = NORMAL)
            P3.config(state = DISABLED)
            P4.config(state = DISABLED)

        elif val == 2:
            np.set(1)
            drop.config(state = DISABLED)
            P2.config(state = DISABLED)
            P3.config(state = DISABLED)
            P4.config(state = DISABLED)

    ##Players have 2 mode options, presented in Radio Buttons form
    mode = IntVar()
    mode.set(1)
    Radiobutton(frame3, text = 'Original', variable = mode, value = 1,command = lambda :pracfunc(mode.get())).grid(row= 0, column= 0)
    Radiobutton(frame3, text = 'Practice', variable = mode, value = 2, command = lambda :pracfunc(mode.get())).grid(row= 0, column= 2)
    Radiobutton(frame3, text = 'Arcade', state = DISABLED, variable = mode, value = 3).grid(row= 0, column= 3)


    ##Function triggered when startgame is selected
    def startfunc(np, one, two, three, four): 
        global nop, pname, pscore
        pname = ['',]
        #print(np, one, two, three, four,sep = '\n')
        if np == 1:
            if one == '':
                messagebox.showerror('Play Scrabble: Family Edition','Player 1: Please Write Your Name')
                title.after(1, lambda: title.focus_force())
                return
            nop = np
            pname.append([one,0])

        elif np == 2:
            if one == '':
                messagebox.showerror('Play Scrabble: Family Edition','Player 1: Please Write Your Name')
                title.after(1, lambda: title.focus_force())
                return
            if two == '':
                messagebox.showerror('Play Scrabble: Family Edition','Player 2: Please Write Your Name')
                title.after(1, lambda: title.focus_force())
                return
            nop = np
            pname.append([one,0])
            pname.append([two,0])

        elif np == 3:
            if one == '':
                messagebox.showerror('Play Scrabble: Family Edition','Player 1: Please Write Your Name')
                title.after(1, lambda: title.focus_force())
                return
            if two == '':
                messagebox.showerror('Play Scrabble: Family Edition','Player 2: Please Write Your Name')
                title.after(1, lambda: title.focus_force())
                return
            if three == '':
                messagebox.showerror('Play Scrabble: Family Edition','Player 3: Please Write Your Name')
                title.after(1, lambda: title.focus_force())
                return
            nop = np
            pname.append([one,0])
            pname.append([two,0])
            pname.append([three,0])


        elif np == 4:
            if one == '':
                messagebox.showerror('Play Scrabble: Family Edition','Player 1: Please Write Your Name')
                title.after(1, lambda: title.focus_force())
                return
            if two == '':
                messagebox.showerror('Play Scrabble: Family Edition','Player 2: Please Write Your Name')
                title.after(1, lambda: title.focus_force())
                return
            if three == '':
                messagebox.showerror('Play Scrabble: Family Edition','Player 3: Please Write Your Name')
                title.after(1, lambda: title.focus_force())
                return
            if four == '':
                messagebox.showerror('Play Scrabble: Family Edition','Player 4: Please Write Your Name')
                title.after(1, lambda: title.focus_force())
                return
            nop = np
            pname.append([one,0])
            pname.append([two,0])
            pname.append([three,0])
            pname.append([four,0])

        print(nop, pname,sep = '\n')
        ##Closes Title (Top level window)
        title.grab_release()
        title.quit()
        title.destroy()


    B1 = Button(title, text = 'On-Screen Keyboard',height = 2, width = 17, borderwidth = 5, bg = 'white', fg = 'black', command = open_osk)
    B1.place(x = 294, y = 170)
    B2 = Button(title, text = 'Start Game',height = 2, width = 10, borderwidth = 5, bg = 'white', fg = 'black',command = lambda: startfunc(np.get(),P1.get(),P2.get(),P3.get(),P4.get()))
    B2.place(x = 430, y = 170)
    
    B1.bind('<Enter>', buttonhover)
    B2.bind('<Enter>', buttonhover)
    title.bind('<Return>', lambda event:startfunc(np.get(),P1.get(),P2.get(),P3.get(),P4.get()))
    
    title.protocol('WM_DELETE_WINDOW', quit_func)

    title.mainloop()

def home():                 ##Home Screen(Top Level)
    home = Toplevel() 
    home.geometry("+%d+%d" % (825, 210))
    home.grab_set()          
    global nop, pname
    home.title('Play Scrabble: Family Edition')
    home.iconbitmap('Scrabble logo.ico')
    home.bind('<Button-1>', buttonclick)
    home.after(1, lambda: home.focus_force())

    ##When new game is selected, this function gets triggered and closes current window as well as call the titlescreen function
    def call_title():
        home.grab_release()
        titlescreen()
        home.quit()
        home.destroy()

    def call_congame():
        home.grab_release()
        congame()
        home.grab_release()
        home.quit()
        home.destroy()

    ##Generating Button with their our commands
    start = Button(home, text = 'New Game',height = 3,  width = 20, borderwidth = 10, bg = 'white', fg = 'black',command = call_title)
    start.grid(row = 0, column = 0, padx = 100, pady = 10, sticky = E+W)

    con = Button(home, text = 'Continue Game',height = 3, width = 20, borderwidth = 10, bg = 'white', fg = 'black',command = call_congame)
    con.grid(row = 1, column = 0, padx = 100, pady = 10)

    #hs = Button(home, text = 'Hight Score',height = 3, width = 20, borderwidth = 10, bg = 'white', fg = 'black',state = DISABLED)
    #hs.grid(row = 2, column = 0, padx = 100, pady = 10)

    ins = Button(home, text = 'Instructions',height = 3, width = 20, borderwidth = 10, bg = 'white', fg = 'black',command = call_ins)
    ins.grid(row = 3, column = 0, padx = 100, pady = 10)

    quitbut = Button(home, text = 'Quit Game',height = 3, width = 20, borderwidth = 10, bg = 'white', fg = 'black', command = quit_func)
    quitbut.grid(row = 4, column = 0, padx = 100, pady = 10)

    start.bind('<Enter>', buttonhover)
    con.bind('<Enter>', buttonhover)
    #hs.bind('<Enter>', buttonhover)
    ins.bind('<Enter>', buttonhover)
    quitbut.bind('<Enter>', buttonhover)

    home.protocol('WM_DELETE_WINDOW', quit_func)
    home.mainloop()

def open_osk():             ##On Screen Keyboard
    keyboard.press(Key.cmd)
    keyboard.press('r')
    keyboard.release('r')
    keyboard.release(Key.cmd)

    time.sleep(0.5)

    keyboard.press('o')
    keyboard.release('o')
    keyboard.press('s')
    keyboard.release('s')
    keyboard.press('k')
    keyboard.release('k')

    keyboard.press(Key.enter)
    keyboard.release(Key.enter)

def scoreboard():           ##It checks NOP and then create scoreboard
    scoreframe.config(text = 'ScoreBoard:')

    Player1.config(text = pname[1][0]+':   '+str(pname[1][1]))
    Player1.grid(row = 0, column = 0)

    if len(pname) >= 3:
        Player2.config(text = pname[2][0]+':   '+str(pname[2][1]))
        Player2.grid(row = 1, column = 0)

    if len(pname) >= 4:
        Player3.config(text = pname[3][0]+':   '+str(pname[3][1]))
        Player3.grid(row = 2, column = 0)

    if len(pname) == 5:
        Player4.config(text = pname[4][0]+':   '+str(pname[4][1]))
        Player4.grid(row = 3, column = 0)

def tick():                 ##Time Clock display
    global start
    time2 = time.time()
    rn=round(time2-start,0)
    status.config(text=str(datetime.timedelta(seconds=rn)))
    status.after(200, tick)

def click(event):           ##Preserves the default color value of a tile when selected and unselected and updates global variable details
    global details, yellow, temp
    (x,y) = (event.widget.grid_info()['row']-1,event.widget.grid_info()['column'])
    old= detail_label.cget('text').split()
    t = grid[(x,y)].cget('text')
    details = [x,y,t]
    grid[(int(old[0]),int(old[1]))]['bg'] = temp[0]
    grid[(int(old[0]),int(old[1]))]['fg'] = temp[1]

    temp[0]= grid[(details[0],details[1])]['bg']
    temp[1] = grid[(details[0],details[1])]['fg']

    grid[(details[0],details[1])]['bg'] = yellow[0]
    grid[(details[0],details[1])]['fg'] = yellow[1]
    detail_func()

def point(event):
    global details, yellow, temp
    (x,y) = (event.widget.grid_info()['row']-1,event.widget.grid_info()['column'])
    old= detail_label.cget('text').split()
    t = grid[(x,y)].cget('text')
    details = [x,y,t]
    grid[(int(old[0]),int(old[1]))]['bg'] = temp[0]
    grid[(int(old[0]),int(old[1]))]['fg'] = temp[1]

    temp[0]= grid[(details[0],details[1])]['bg']
    temp[1] = grid[(details[0],details[1])]['fg']

    grid[(details[0],details[1])]['bg'] = yellow[0]
    grid[(details[0],details[1])]['fg'] = yellow[1]
    detail_func()

    if grid[(x,y)].cget('state') == DISABLED:
        if word.get() == 'Word Here':
            word.delete(0,END)
            word.focus()
        word.insert(END,grid[(x,y)].cget('text'))

def shuff_func(event = None):       ##Shuffle rack
    for x in range(7):
        var = random.randint(0,6)
        tiles[x]['text'],tiles[var]['text'] = tiles[var]['text'],tiles[x]['text']

def wordfunc(event=None):        ##Clears the writing space for word play, used with keybinding
    word.delete(0,END)
    word.focus()

def tilefunc(event):        ##Triggers OSK when '#' Tile is selected
    temp = word.get()
    if temp == 'Word Here':
        word.delete(0,END)
        word.focus()
    temp = event.widget.cget('text')
    if temp == '#':
        open_osk()
        return
    word.insert(END,temp)

def detail_func():          ##Displays the content of global variable Details
    detail_label['text'] = details
    detail_label.grid(row = 0, column = 0, sticky = W)

def donebut(radio):         ##Updating global varibale POC(player of challange)
    global POC, pname, counter
    POC = radio

def createselect():         ##Creates a TopLevel for selection of player of challange
    global counter, pname
    select = Toplevel()

    select.iconbitmap('Scrabble logo.ico')
    select.title('Play Scrabble: Family Edition')
    select.bind('<Button-1>', buttonclick)
    select.grab_set()
    select.after(1, lambda: select.focus_force())

    ##POCL = POC(local)
    POCL = IntVar()
    POCL.set(0)
    

    pselect = LabelFrame(select, text = 'Select the Player Challanging the word:',pady = 10)
    pselect.grid(row =1, column = 1, padx = 10, rowspan = 5, columnspan = 3, sticky = W+E)

    R1 = Radiobutton(pselect, text = 'Player 1', variable = POCL, value = 1, command= lambda: donebut(POCL.get()))
    R1.grid(row = 1, column = 1)
    R1.bind('<Enter>', buttonhover)

    if len(pname) >= 3:
        R2 = Radiobutton(pselect, text = 'Player 2', variable = POCL, value = 2, command= lambda: donebut(POCL.get()))
        R2.grid(row = 2, column = 1)
        R2.bind('<Enter>', buttonhover)

    if len(pname) >= 4:
        R3 = Radiobutton(pselect, text = 'Player 3', variable = POCL, value = 3, command= lambda: donebut(POCL.get()))
        R3.grid(row = 3, column = 1)
        R3.bind('<Enter>', buttonhover)

    if len(pname) == 5:
        R4 = Radiobutton(pselect, text = 'Player 4', variable = POCL, value = 4, command= lambda: donebut(POCL.get()))
        R4.grid(row = 4, column = 1)
        R4.bind('<Enter>', buttonhover)

    ##A function that will quit and destroy select (Toplevel)
    def closefunc():
        if (POCL.get()) == 0:
            no_word = messagebox.showwarning('Play Scrabble: Family Edition','Please Select the challenging Player.')
            return
        select.grab_release()
        select.quit()
        select.destroy()

    done = Button(select, text = 'Done', height = 2, width = 30, borderwidth = 5, bg = 'black',fg='white',command = closefunc)
    done.grid(row=10, column = 1, padx = 10,pady = 10, sticky = W+E)
    done.bind('<Enter>', buttonhover)
    
    ##The button of the player whos playing the turn will be disabled
    if counter == 1:
        R1.config(state = DISABLED)
    elif counter == 2:
        R2.config(state = DISABLED)
    elif counter == 3:
        R3.config(state = DISABLED)
    elif counter == 4:
        R4.config(state = DISABLED)

    def warn():
        no_word = messagebox.showwarning('Play Scrabble: Family Edition','A player must challenge now!')
        return

    select.protocol('WM_DELETE_WINDOW', warn)
    select.mainloop()

def finish(pname):          ##Create a new window to annouce the winner
    global TNOT, bag, maxscore, nop, Tilescore
    board.quit()
    board.destroy()
    winner = Tk()
    winner.title('Play Scrabble: Family Edition')
    winner.iconbitmap('Scrabble logo.ico')
    pname.pop(0)

    cheer_sound = mixer.Sound('Cheers.wav')
    cheer_sound.play()

    for x in range(nop):
        temp = 0
        for y in all_tiles[x]:
            temp = temp + Tilescore[y]
        pname[x][1] = pname[x][1] - temp

    for i in range(1, len(pname)): 
        key = pname[i]
        j = i-1
        while j >=0 and key[1] > pname[j][1] : 
                pname[j+1] = pname[j] 
                j -= 1
        pname[j+1] = key
    print(pname)
    
    leader = LabelFrame(winner, text = 'LeaderBoard:')
    leader.grid(row = 1, column = 1,padx = 10, pady = 10,sticky = W+E)
    for x in range(len(pname)):
        Label(leader, text = str(x+1)+'.     '+pname[x][0]+':   '+str(pname[x][1])).grid(row = x,padx = 10, pady = 3, column = 1,sticky = W+E)

    stats = LabelFrame(winner, text= 'Statistics:')
    stats.grid(row = 1, column = 5,padx = 10, pady = 10,sticky = W+E)
    Label(stats, text= 'No. of Turns Played: '+str(TNOT)).grid(row = 1,padx = 10, pady = 3, column = 1,sticky = W+E)
    Label(stats, text= 'No. of Titles Left In The Bag: '+str(len(bag))).grid(row = 2,padx = 10, pady = 3, column = 1,sticky = W+E)
    Label(stats, text= 'Highest Score Scored In A Single Turn : '+str(maxscore[0])).grid(row = 3,padx = 10, pady = 3, column = 1,sticky = W+E)
    Label(stats, text= 'Player Who Scored The Highest Scored Turn : '+maxscore[1]).grid(row = 4,padx = 10, pady = 3, column = 1,sticky = W+E)
    Label(stats, text= 'Best Word played was : '+maxscore[2]).grid(row = 5,padx = 10, pady = 3, column = 1,sticky = W+E)

    declare = LabelFrame(winner, text= 'Winner:')
    declare.grid(row = 3, column = 1,padx = 10, pady = 10,columnspan = 10)
    Label(declare,text = 'The Winner Is: '+pname[0][0]+' By Scoring '+str(pname[0][1])+' Points.\nCongrats!').grid(row = 1,padx = 10, pady = 3, column = 1,sticky = W)
    
    def byes():         ##Good bye msg box
        messagebox.showinfo('Play Scrabble: Family Edition','Thank You For Playing Scrabble: Family Edition.\nHope To See You Soon. Good Bye :)')
        winner.quit()
        winner.destroy()

    winner.protocol('WM_DELETE_WINDOW', byes)
    winner.mainloop()

def dirbut(value):          ##Direction Check for word if left unselected
    if value == 0:
        messagebox.showerror('Play Scrabble: Family Edition','You didn\'t select any direction.\n Try Again!')
    return value

def cross_check(radio, mx, my, w):      ##It checks if any invalid or valid words are made when new turns are played but in cross directions
    x = mx
    y = my
    word = ''
    if radio == 1:
        if y >0:
            while y > 0:
                if grid[(x,y-1)].cget('state') == DISABLED:
                    word = grid[(x,y-1)].cget('text') + word
                    y = y - 1
                    continue
                break

        word = word + w
        
        if w == grid[(mx,my)].cget('text') and grid[(mx,my)].cget('state') == DISABLED:
            return 'True'

        y = my
        if y < 14:
            while y < 14:
                if grid[(x,y+1)].cget('state') == DISABLED:
                    word = word + grid[(x,y+1)].cget('text')
                    y = y + 1
                    continue
                break

        if len(word) > 1:
            if word_challenge(word) == True:
                print(word)
                scoring(word,counter)       ##A valid word is made and sent for score calculation
                return 'True'
            else:
                messagebox.showerror('Play Scrabble: Family Edition','Error occured while word crossing.\nAn invalid word was created: '+word+'.')
                return 'Error'

    else:
        ##y axis check
        if x > 0:
            while x > 0:
                if grid[(x-1,y)].cget('state') == DISABLED:
                    word = grid[(x-1,y)].cget('text') + word
                    x = x - 1
                    continue
                break
        
        word = word + w

        if w == grid[(mx,my)].cget('text') and grid[(mx,my)].cget('state') == DISABLED:
            return 'True'

        x = mx
        if x < 14:
            while x < 14:
                if grid[(x+1,y)].cget('state') == DISABLED:
                    word = word + grid[(x+1,y)].cget('text')
                    x = x + 1
                    continue
                break

        if len(word) > 1:
            if word_challenge(word) == True:
                print(word)
                scoring(word,counter)       ##A valid word is made and sent for score calculation
                return 'True'
            else:
                messagebox.showerror('Play Scrabble: Family Edition','Error occured while word crossing.\nAn invalid word was created: '+word+'.')
                return 'Error'
    return 'False'

def new_word(a):
    dic.insert_1(a)
    print(dic.search(a))

def Submitfunc():           ##The Brains of the game:
    global words,TNOT, POC, skip, nop, counter, crossflag, racktemp, dl, dw, tl, tw, blank, tempscore, tempword, maxscore
    wordtemp = []
    racktemp = []
    (s_x,s_y) = (details[0],details[1])     ##row, column of starting point
    (x,y)=(s_x,s_y)
    word_main = word.get().upper()      ##Upper case the input words
    wordlen = len(word_main)
    radio = dirbut(direction.get())     ##Validating that a direction is selected
    
    if radio_check(radio,wordlen,x,y) != True:  ##Validating that the word wont go beyond boards bound
        return False

    dic_ans = word_challenge(word_main)     ##Checking word from dictionary
    if dic_ans == False:
        messagebox.showwarning('Play Scrabble: Family Edition','Your word wasn\'t available in our dictionary.')
        challange_box = messagebox.askyesnocancel('Play Scrabble: Family Edition','Do other player\'s want to challange this word ?')
        
        if challange_box == True:
            createselect()      
            Challenge_success= messagebox.askyesno('Play Scrabble: Family Edition','Was challenge successful?')
            if Challenge_success == False:
                ##If challenge wan't successful then the new word will be included in our dictionary
                dic_ans = True
                new_word(word_main.upper())
                ##As a penalty, POC will have its upcoming turn skipped
                skip = POC
                
            
            if Challenge_success == True:
                ##Losing to a challenge will cause the player to loss its ongoing turn
                return change_turn(counter,nop)
        
        if challange_box == False:
            ##If no one challenges, then the word is accepted as a valid word and added to the dictionary
            dic_ans = True
            new_word(word_main.upper())

    if dic_ans and radio == 1:
        if x > 0:
            if grid[(x-1,y)].cget('state') == DISABLED:
                messagebox.showerror('Play Scrabble: Family Edition','You can\'t overwite an exisiting word')
                return False
        ##First word center check
        if TNOT == 0:
            if s_x < 7 and s_y == 7:
                if (s_x + wordlen - 1) >= 7:
                    pass
                else:
                    messagebox.showerror('Play Scrabble: Family Edition','First word must pass through the center of the board.\n Try Again!')
                    return False
            elif s_y == s_x == 7:
                pass
            else:
                messagebox.showerror('Play Scrabble: Family Edition','First word must pass through the center of the board.\n Try Again!')
                return False

        for w in word_main:
            ##Word is printed on the board letter by letter after required checks have been performed
            tempflag = cross_check(radio, x, y, w) 
            if tempflag == 'True':
                crossflag = 'True'

            elif tempflag == 'Error':
                ##If an error occurs, all values are retured to their original state
                temprefill(racktemp)
                tempscore = 0
                dw = 0
                tw = 0
                dl = []
                tl = []
                blank = []
                for x in wordtemp:
                    grid[(x[0],x[1])].config(text=x[2])
                    grid[(x[0],x[1])].config(state = NORMAL)
                    if (x[0],x[1]) != (s_x,s_y):
                        grid[(x[0],x[1])].config(bg=x[3])
                        grid[(x[0],x[1])].config(fg=x[4])
                return False
                
            if grid[(x,y)].cget('state') != DISABLED:
                ##It means their is no prior letter written on the box
                if check_if_word_in_rack(w,counter) == True:
                    wordtemp.append([x,y,grid[(x,y)].cget('text'),grid[(x,y)].cget('bg'),grid[(x,y)].cget('fg')])
                    ##Before printing the letter, the above mentioned attributes are recorded for each turn
                    ##and used when an error is occured to reset values to their original state
                    ##Then its checked that does the current box give any bonus score
                    if grid[(x,y)].cget('text') == 'DWS':
                        dw = dw + 1
                    elif grid[(x,y)].cget('text') == 'TWS':
                        tw = tw + 1
                    elif grid[(x,y)].cget('text') == 'DLS':
                        dl.append(w)
                    elif grid[(x,y)].cget('text') == 'TLS':
                        tl.append(w)
                    grid[(x,y)].config(text=w)
                    grid[(x,y)].config(state= DISABLED)
                else:
                    ##If letter is not available in rack error is showed
                    messagebox.showerror('Play Scrabble: Family Edition',w+': is not available in your rack')
                    temprefill(racktemp)
                    tempscore = 0
                    dw = 0
                    tw = 0
                    dl = []
                    tl = []
                    blank = []
                    for x in wordtemp:
                        grid[(x[0],x[1])].config(text=x[2])
                        grid[(x[0],x[1])].config(state = NORMAL)
                        if (x[0],x[1]) != (s_x,s_y):
                            grid[(x[0],x[1])].config(bg=x[3])
                            grid[(x[0],x[1])].config(fg=x[4])
                    return False
                if (x,y) != (s_x,s_y):
                    grid[(x,y)].config(bg= 'white')
            else:
                if grid[(x,y)].cget('text') != w:
                    ##If the box is disabled, which means that it already contains a letter. 
                    # If the new letter is not same as the existing one it will pop-up un error.
                    messagebox.showerror('Play Scrabble: Family Edition','You can\'t overwrite an existing word.\n Try Again!')
                    temprefill(racktemp)
                    tempscore = 0
                    dw = 0
                    tw = 0
                    dl = []
                    tl = []
                    blank = []
                    for x in wordtemp:
                        grid[(x[0],x[1])].config(text=x[2])
                        grid[(x[0],x[1])].config(state = NORMAL)
                        if (x[0],x[1]) != (s_x,s_y):
                            grid[(x[0],x[1])].config(bg=x[3])
                            grid[(x[0],x[1])].config(fg=x[4])
                    return False
            x=x+1
        if crossflag == 'False':
            messagebox.showerror('Play Scrabble: Family Edition','New words must be connected to the exisiting words')
            temprefill(racktemp)
            tempscore = 0
            dw = 0
            tw = 0
            dl = []
            tl = []
            blank = []
            for x in wordtemp:
                grid[(x[0],x[1])].config(text=x[2])
                grid[(x[0],x[1])].config(state = NORMAL)
                if (x[0],x[1]) != (s_x,s_y):
                    grid[(x[0],x[1])].config(bg=x[3])
                    grid[(x[0],x[1])].config(fg=x[4])
            return False
        crossflag = 'False'
        temp[0] = 'white'
        word.delete(0,END)
        word.insert(0, 'Word Here')
        direction.set(0)
        print(word_main)
        scoring(word_main,counter)
        tempword = word_main
        return True

    elif dic_ans and radio == 2:
        if y > 0:
            if grid[(x,y-1)].cget('state') == DISABLED:
                messagebox.showerror('Play Scrabble: Family Edition','You can\'t overwite an exisiting word')
                return False
        if TNOT == 0:
            ##First word center check
            if s_y < 7 and s_x == 7:
                if (s_y + wordlen - 1) >= 7:
                    pass
                else:
                    messagebox.showerror('Play Scrabble: Family Edition','First word must pass through the center of the board.\n Try Again!')
                    return False ##error
            elif s_x == s_y == 7:
                pass
            else:
                messagebox.showerror('Play Scrabble: Family Edition','First word must pass through the center of the board.\n Try Again!')
                return False ##error

        for w in word_main:
            tempflag = cross_check(radio, x, y, w)

            if tempflag == 'True':
                crossflag = 'True'
            elif tempflag == 'Error':
                temprefill(racktemp)
                tempscore = 0
                dw = 0
                tw = 0
                dl = []
                tl = []
                blank = []
                for x in wordtemp:
                    grid[(x[0],x[1])].config(text=x[2])
                    grid[(x[0],x[1])].config(state = NORMAL)
                    if (x[0],x[1]) != (s_x,s_y):
                        grid[(x[0],x[1])].config(bg=x[3])
                        grid[(x[0],x[1])].config(fg=x[4])
                return False
            if grid[(x,y)].cget('state') != DISABLED:
                if check_if_word_in_rack(w,counter) == True:
                    if grid[(x,y)].cget('text') == 'DWS':
                        dw = dw + 1
                    elif grid[(x,y)].cget('text') == 'TWS':
                        tw = tw + 1
                    elif grid[(x,y)].cget('text') == 'DLS':
                        dl.append(w)
                    elif grid[(x,y)].cget('text') == 'TLS':
                        tl.append(w)
                    wordtemp.append([x,y,grid[(x,y)].cget('text'),grid[(x,y)].cget('bg'),grid[(x,y)].cget('fg')])
                    grid[(x,y)].config(text=w)
                    grid[(x,y)].config(state= DISABLED)
                else:
                    messagebox.showerror('Play Scrabble: Family Edition',w+': is not available in your rack')
                    temprefill(racktemp)
                    tempscore = 0
                    dw = 0
                    tw = 0
                    dl = []
                    tl = []
                    blank = []
                    for x in wordtemp:
                        grid[(x[0],x[1])].config(text=x[2])
                        grid[(x[0],x[1])].config(state = NORMAL)
                        if (x[0],x[1]) != (s_x,s_y):
                            grid[(x[0],x[1])].config(bg=x[3])
                            grid[(x[0],x[1])].config(fg=x[4])
                    return False

                if (x,y) != (s_x,s_y):
                    grid[(x,y)].config(bg= 'white')
            else:
                if grid[(x,y)].cget('text') != w:
                    messagebox.showerror('Play Scrabble: Family Edition','You can\'t overwrite an existing word.\n Try Again!')
                    temprefill(racktemp)
                    tempscore = 0
                    dw = 0
                    tw = 0
                    dl = []
                    tl = []
                    blank = []
                    for x in wordtemp:
                        grid[(x[0],x[1])].config(text=x[2])
                        grid[(x[0],x[1])].config(state = NORMAL)
                        if (x[0],x[1]) != (s_x,s_y):
                            grid[(x[0],x[1])].config(bg=x[3])
                            grid[(x[0],x[1])].config(fg=x[4])
                    return False
            y=y+1
        if crossflag == 'False':
            messagebox.showerror('Play Scrabble: Family Edition','New words must be connected to the exisiting words')
            temprefill(racktemp)
            tempscore = 0
            dw = 0
            tw = 0
            dl = []
            tl = []
            blank = []
            for x in wordtemp:
                grid[(x[0],x[1])].config(text=x[2])
                grid[(x[0],x[1])].config(state = NORMAL)
                if (x[0],x[1]) != (s_x,s_y):
                    grid[(x[0],x[1])].config(bg=x[3])
                    grid[(x[0],x[1])].config(fg=x[4])
            return False
        crossflag = 'False'
        temp[0] = 'white'
        word.delete(0,END)
        word.insert(0, 'Word Here')
        direction.set(0)  
        print(word_main)
        scoring(word_main,counter)
        tempword = word_main
        return True
    else:
        return False

def change_turn(skipt, nop,event = None):       ##When you end your turn, this function is called and if all checks and validations are cleared, turn is changed
    global counter, TNOT, skip, racktemp, pname, tempscore, dl, dw, tl, tw, blank, maxscore, tempword
    ##Same function is called when one either plays his turn or skips it because the consequent is same. 
    #The turn gets changed.
    if counter == skipt:
        ##First it checks for skiping of the turn.
        skip = 0
        if counter == nop:
            counter = 0
        scoreboard()
        counter = counter + 1
        name_dispaly.config(text = pname[counter][0]+'; It\'s your turn')
        inserting_letters_into_player_tiles(all_tiles[counter-1])
        word.delete(0,END)
        word.insert(0, 'Word Here')
        direction.set(0)
        #In case of changing of turn the above mentioned steps are taken:
        # 1) Turn notification bar chnages it text. 
        # 2) The rack gets changed. 
        # 3) The writing space gets it default text back. 
        # 4) The direction button is unselected
        return

    status = Submitfunc()
    ##If not skipped, then word played is checked
    if status == True:
        if TNOT == 0:
            tempscore = tempscore * 2
        pname[counter][1] = pname[counter][1] + tempscore
        scoreboard()
        if tempscore > maxscore[0]:
            maxscore[0] = tempscore
            maxscore[1] = pname[counter][0]
            maxscore[2] = tempword
        tempscore = 0
        dw = 0
        tw = 0
        dl = []
        tl = []
        blank = []
        print(pname)
        refilling_tray()
        if counter == nop:
            counter = 0
        counter = counter + 1
        TNOT = TNOT + 1
        for x in range(nop):
            print(x+1,' :',all_tiles[x])
        print('\n')
        name_dispaly.config(text = pname[counter][0]+'; It\'s your turn')
        inserting_letters_into_player_tiles(all_tiles[counter-1])
    ##If a valid word is created above mentioned steps are taken:
    # 1) Scoreboard is updated. 
    # 2) Score related global varibales are reseted. 
    # 3) Racks are refilled. 
    # 4) Turn notification bar changes its text. 
    # 5) Rack is changed
    # 6) Lastly, its checked should the upcoming player get his turn skipped becuase of lossing a challenge

    if counter == skip:
        skip = 0
        if counter == nop:
            counter = 0
        scoreboard()
        counter = counter + 1
        name_dispaly.config(text = pname[counter][0]+'; It\'s your turn')
        inserting_letters_into_player_tiles(all_tiles[counter-1])
        word.delete(0,END)
        word.insert(0, 'Word Here')
        direction.set(0)

def newgame():
    python = sys.executable
    os.execl(python, python, * sys.argv)

def savegame(event = None):
    global counter, TNOT, nop, skip, pname, tiles, grid, maxscore, bag, all_tiles, start
    save = {}
    lst = []
    for a in range(15):
        for b in range(15):
            lst.append([a,b,grid[(a,b)].cget('text')])

    con = ''
    for x in lst:
        for y in x:
            con+=str(y) +'.'
        con+= ','

    #print(con)

    lst = []
    lst = compression(con)
    #print(lst)

    save['counter'] = counter
    save['TNOT'] = TNOT
    save['nop'] = nop
    save['skip'] = skip
    save['pname'] = pname
    save['maxscore'] = maxscore
    save['bag'] = bag
    save['all_tiles'] = all_tiles
    save['grid'] = lst
    save['time'] = start

    dbfile = filedialog.asksaveasfile(title= 'Select The Saving Directory', mode='wb', defaultextension=".bin", filetypes=(('Binary Files','*.bin'),('All Files','*.*')))
    pickle.dump(save, dbfile)                      
    dbfile.close()

def congame():
    global counter, TNOT, nop, skip, pname, tiles, grid, maxscore, bag, all_tiles, conflag, start
    ret = {}
    con = ''
    filename = filedialog.askopenfilename(title= 'Select a Saved File:',filetypes=(('Binary Files','*.bin'),('All Files','*.*')))
    dbfile = open(filename, 'rb')      
    db = pickle.load(dbfile) 
    dbfile.close()
    #print(db)

    counter = db['counter'] - 1
    TNOT = db['TNOT']
    nop = db['nop']
    skip = db['skip']
    pname = db['pname']
    maxscore = db['maxscore']
    bag = db['bag']
    all_tiles = db['all_tiles']
    lst = db['grid']
    start = db['time']

    if counter == 0:
        counter = len(pname) - 1

    con = huffman_decoding(lst[1],lst[0])
    lst= []
    con = con.split(',')
    con = con[:-1]
    for x in con:
        a = x.split('.')
        a = a[:-1]
        for i in range(0, 2):
            a[i] = int(a[i])
        lst.append(a)
    

    for x in lst:
        grid[(x[0],x[1])].config(text = x[2])

    for a in range(15):
        for b in range(15):
            if grid[(a,b)].cget('text') != 'TWS' and grid[(a,b)].cget('text') != 'DWS' and grid[(a,b)].cget('text') != 'TLS' and grid[(a,b)].cget('text') != 'DLS' and grid[(a,b)].cget('text') != '':
                grid[(a,b)].config(state = DISABLED)
                grid[(a,b)].config(bg = 'white')

    conflag = True

def call_ins():
    os.startfile('Scrabble Family Edition PDF.pdf')
    return

def buttonclick(event):
    winsound.PlaySound('Mouse-Click-00.wav', winsound.SND_FILENAME + winsound.SND_ASYNC)

def buttonhover(event):
    return
    #hover_sound = mixer.Sound('button-hover.wav')
    #hover_sound.play()
    
def down(event=None):
    direction.set(1)

def right(event = None):
    direction.set(2)

def contact():
    con = Toplevel()
    con.title('Play Scrabble: Family Edition')
    con.iconbitmap('Scrabble logo.ico')
    con.grab_set()
    con.bind('<Button-1>', buttonclick)
    con.after(1, lambda: con.focus_force())

    frame1 = LabelFrame(con,text = 'Project Participents:')
    frame1.grid(row=0, column = 1,padx = 10,pady=10,sticky = N+S)

    Label(frame1,text ='Muhammad Jawwad: mj05516@st.habib.edu.pk').grid(row=1, column = 1, padx=5, pady=10)
    Label(frame1,text ='Hussain Abbas: ha06228@st.habib.edu.pk').grid(row=2, column = 1, padx=5, pady=10)
    Label(frame1,text ='Ramis Raza: af04372@st.habib.edu.pk').grid(row=3, column = 1, padx=5, pady=10)
    Label(frame1,text ='Hamna Jamil: af04372@st.habib.edu.pk').grid(row=4, column = 1, padx=5, pady=10)
    Label(frame1,text ='Mehdi Raza: mr05967@st.habib.edu.pk').grid(row=5, column = 1, padx=5, pady=10)

def stop_music():
    mixer.music.stop()

def play_music():
    mixer.music.load("Good_Starts.wav")
    mixer.music.play(-1)