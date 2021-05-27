def quit_func():                ##Quits and Destroys the board(main window)
    global quitflag
    quit_box = messagebox.askyesno('Play Scrabble: Family Edition','Do you want to quit ?')
    if quit_box == 1:
        board.quit()
        board.destroy()
    return

def generate_bag():             ##Generates letters and append them to bag
    bag=[]
    for i in range(9):
        bag.append("A")
    for i in range(2):
        bag.append("B")
    for i in range(2):
        bag.append("C")
    for i in range(4):
        bag.append("D")
    for i in range(12):
        bag.append("E")
    for i in range(2):
        bag.append("F")
    for i in range(3):
        bag.append("G")
    for i in range(1):
        bag.append("H")
    for i in range(9):
        bag.append("I")
    for i in range(9):
        bag.append("J")
    for i in range(1):
        bag.append("K")
    for i in range(4):
        bag.append("L")
    for i in range(2):
        bag.append("M")
    for i in range(6):
        bag.append("N")
    for i in range(8):
        bag.append("O")
    for i in range(2):
        bag.append("P")
    for i in range(1):
        bag.append("Q")
    for i in range(6):
        bag.append("R")
    for i in range(4):
        bag.append("S")
    for i in range(6):
        bag.append("T")
    for i in range(4):
        bag.append("U")
    for i in range(2):
        bag.append("V")
    for i in range(2):
        bag.append("W")
    for i in range(1):
        bag.append("X")
    for i in range(2):
        bag.append("Y")
    for i in range(1):
        bag.append("Z")
    for i in range(2):
        bag.append("#")
    shuffle(bag)
    return bag

def generating_racks(number_of_players,bag):            ##Generates rack for each player
    players_racks=[]
    for i in range(number_of_players):
        tmp=[]
        for k in range(7):
            tmp.append(bag.pop())
        players_racks.append(tmp)
    return players_racks

def inserting_letters_into_player_tiles(letters_lst):   ##Overwriting tile's text with rack alphabets
    global tiles
    y=0
    for x in letters_lst:
        but = Button(tile_frame, text = x, height = 2, width = 5, borderwidth = 5, bg = 'white', fg = 'black')
        if y<=4:
            but.grid(row = 0, column = y)

        else:
            but.grid(row = 1, column = y-5)
        tiles[(y)] = but
        tiles[(y)].bind("<Button-1>",tilefunc)
        tiles[(y)].bind('<Enter>', buttonhover)
        y=y+1
    return

def word_challenge(word):       ##Calls a function what checks the work through the dictionary
    return dic.search(word)
        
def check_word(arr, l, r, x):   ##Binary search implementaion, searches through the dictionary for the word  
    while l <= r: 
        mid = l + (r - l) // 2
        if arr[mid] == x: 
            return True 
        elif arr[mid] < x: 
            l = mid + 1
        else: 
            r = mid - 1
    return False

def radio_check(radio,wordlen,x,y): ##With repect to direction selected, it checks the word should not go out of bounds of board
    radiolen = False
    if radio == 0:
        return False
    elif radio == 1:
        if wordlen <= (15-x):
            radiolen = True
    elif radio == 2:
        if wordlen <= (15-y):
            radiolen = True
    
    if radiolen == False:
        messagebox.showerror('Play Scrabble: Family Edition','Your word lenght exceeded the block available.\n Try Again!')
        return False
    return True

def partition(arr,low,high):    ##These 3 functions are used when a challenge is made
    i = ( low-1 )         # index of smaller element 
    pivot = arr[high]     # pivot 
  
    for j in range(low , high): 
  
        # If current element is smaller than the pivot 
        if   arr[j] < pivot: 
          
            # increment index of smaller element 
            i = i+1 
            arr[i],arr[j] = arr[j],arr[i] 
  
    arr[i+1],arr[high] = arr[high],arr[i+1] 
    return ( i+1 ) 

def quickSort(arr,low,high):    ##When a new word is introduced to our dictionary it gets appended
    if low < high: 
  
        # pi is partitioning index, arr[p] is now 
        # at right place 
        pi = partition(arr,low,high) 
  
        # Separately sort elements before 
        # partition and after partition 
        quickSort(arr, low, pi-1) 
        quickSort(arr, pi+1, high) 

def sort_dictionary(words):     ##and then our dictionary is sorted so we can use binary search again
    #l=len(words)
    #quickSort(words,0,l-1)
    words.sort()

    #testing
    if os.path.exists("dic.txt"): 
        os.remove("dic.txt") 
    
    file = open("dic.txt", "w")
    for k in words:
        file.write(k+"\n") 
    file.close()
    return words

def temprefill(racktemp):       ##When an error occurs, this function restores the rack with its default letters
    tmp_rack = all_tiles[counter-1]
    for x in racktemp:
        tmp_rack.append(x)
    all_tiles[counter-1] = tmp_rack
    racktemp = []

def refilling_tray():           ##After each turn this function makes sure that players rack has 7 letters
    tmp_rack = all_tiles[counter-1]
    while len(tmp_rack) < 7:
        tmp = bag.pop()
        tmp_rack.append(tmp)
    all_tiles[counter-1] = tmp_rack

def check_if_word_in_rack(word_main,counter):   ##This functions check that are the letters required available in the rack 
    global racktemp, blank
    tmp_rack = all_tiles[counter-1]
    if word_main in tmp_rack:
        tmp_rack.remove(word_main)
        racktemp.append(word_main)
        all_tiles[counter-1] = tmp_rack
        return True
    elif '#' in tmp_rack:
        blank.append(word_main)
        tmp_rack.remove('#')
        racktemp.append('#')
        all_tiles[counter-1] = tmp_rack
        return True
    return False

def rack_empty(counter):    ##It checks for the lenght of the rack for scoring purpose
	if len(all_tiles[counter-1]) == 0:
		return True
	return False
 
def score_checker(word, list_of_scores):    ##Calculates indivisual tile's score
    global dl ,tl, blank
    score = 0
    my_string = list(word)

    for i in my_string:
        if i in dl:
            score = score + (2*Tilescore[i])
            dl.pop(dl.index(i))
        elif i in tl:
            score = score + (3*Tilescore[i])
            tl.pop(tl.index(i))
        else:
            score = score + (Tilescore[i])
    
    for x in blank:
        score = score - (Tilescore[x])
    
    blank = []
    return score

def scoring(word,counter):      ##It checks and applies DWS & TWS and updates the score
    global tempscore, dw, tw
    winsound.PlaySound('Score.wav', winsound.SND_FILENAME + winsound.SND_ASYNC)
    tempscore = tempscore + score_checker(word, Tilescore)
    if dw > 0:
        tempscore = tempscore*(2*dw)
        dw = 0

    if tw > 0:
        tempscore = tempscore*(3*tw)
        tw = 0

    if rack_empty(counter) == True:
        tempscore = tempscore + 50