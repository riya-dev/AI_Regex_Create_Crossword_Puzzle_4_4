# Riya Dev
# 3/2/2021

# Crosswrd Puzzle Rules
#     Crosswords are symmetric with respect to their center (Rotation by 180 degrees produces the same blocked positions)
#     Every open square appears in both a horizontal and vertical word
#     Every word is at least 3 characters
#     No word in the crossword may happen twice.
#     The open squares are connected.

# Sample Input: file.py heightxwidth dict.txt #ofBlocks HVposxHposWord VVposxHposWord
# 15x15 39 dct20k.txt H0x0Mute V0x0mule V10x13Locus H7x5# V3x4# H6x7# V11x3#

import sys; args = sys.argv[1:]
import re, random # os

# constants
blockchar = '#' # blocked square (black square)
openchar = '-' # open square (not decided yet)
protectedchar = '~' # reserved for word characters
counter = 0
# retest = [r"^\d+x\d+$", r"^\d+$", r"^\w+\.txt$", r"^v\d+x\d+\w+$", r"^h\d+x\d+\w+$"] # dimensions, num blocks, file, vertical, horizontal
# retest = [r"^\d+x\d+$", r"^\d+$", r"^\w+\.txt$", r"^v\d+x\d+\w+|v\d+x\d+(\w*#*)*$", r"^h\d+x\d+\w+|h\d+x\d+(\w*#*)*$"]
retest = [r"^\d+x\d+$", r"^\d+$", r"^\w+\.txt$", r"^v\d+x\d+.*$", r"^h\d+x\d+.*$"]

# variables
height = 0
width = 0
block_count = 0
file_name = 0

def display(board):
   for r in board:
      for c in r:
         print(c, end = " ")
      print()
   print()

def makeboard(board):
   global height, width, block_count, file_name
   
   for arg in args:
      for k, r in enumerate(retest):
         match = re.search(r, arg, re.I)
         if k == 0 and match != None: # dimensions
            height, width = arg.split('x') # set global value
            height = int(height)
            width = int(width)
            
            row = []
            for h in range(height):
               for w in range(width):
                  row.append("-")
               board.append(row)
               row = []
                     
         elif k == 1 and match != None: # number of blocks
            block_count = arg
            block_count = int(block_count)
         
            #if block_count == height * width:
            #   for h in range(height):
            #      for w in range(width):
            #         board[h][w] = blockchar
            
         elif k == 2 and match != None: # word list file
            file_name = arg
            
         elif k == 3 and match != None: # vertical
            arg = arg[1:]
            row, p2 = arg.split('x')
            # print("vertical", p2, re.findall(r"^(\d+)(.*)$", p2))
            res = re.findall(r"^(\d+)(.*)$", p2)[0] #re.findall(r"^(\d+)(\w+?)$", p2)[0]
            col, word = res
            row = int(row)
            col = int(col)
            length = len(word)
            
            charnum = 0
            for r in range(row, row + length):
               board[r][col] = word[charnum].upper()
               charnum += 1
            
         elif k == 4 and match != None: # horizontal
            arg = arg[1:]
            row, p2 = arg.split('x')
            # print("horizontal", re.findall(r"^(\d+)(.*)$", p2))
            res = re.findall(r"^(\d+)(.*)$", p2)[0] # res = re.findall(r"^(\d+)(\w+?)$", p2)[0]     |     re.findall(r"^(\d+)(\w*#*)$", p2)[0]
            col, word = res
            
            row = int(row)
            col = int(col)
            length = len(word)
            
            charnum = 0
            for c in range(col, col + length):
               board[row][c] = word[charnum].upper()
               charnum += 1
      
      #xw = blockchar*(width+3)
      #xw +=(blockchar*2).join([xword[p:p+width] for p in range(0,len(xword),width)])
      #xw += blockchar*(width+3)

def cleanprotected(board):
   for h in range(height):
      for w in range(width):
         if board[h][w].isalpha():
            board[h][w] = protectedchar
            #print("(" + str(h) + ", " + str(w) + ")", "and", "(" + str(width - w - 1) + ", " + str(height - h - 1) + ")")
            board[height - h - 1][width - w - 1] = protectedchar
   if height % 2 == 1 and width % 2 == 1:
      board[int(height/2)][int(width/2)] = protectedchar
      
   print()
   print("After adding given words:")
   display(board)
   
   print()
#   indexes = []
#   for h in range(height):
#      for w in range(width):
#         if board[h][w] == openchar:
#            # print("is open char", h * width + w, "(", h, w, ")")
#            indexes.append(h * width + w)
   indexes = gen_pos_list(board)
   print("pos list is:", indexes)
   display(board)

# palindrome method - in addition to clean protected
def makepalindrome(board):
   for h in range(height):
      for w in range(width):
         if board[h][w].isalpha():
            board[h][w] = protectedchar
            #print("(" + str(h) + ", " + str(w) + ")", "and", "(" + str(width - w - 1) + ", " + str(height - h - 1) + ")")
            board[height - h - 1][width - w - 1] = protectedchar
   if height % 2 == 1 and width % 2 == 1:
      board[int(height/2)][int(width/2)] = protectedchar

def addobviousblockedsquare(board):
   global counter
   counter = counter + 1
   print()
   print("New board", counter)
   
   if block_count == height * width:
      for h in range(height):
         for w in range(width):
            board[h][w] = blockchar
      return
   
   new_board = board
   
   # obvious blocks
   for h in range(height):
      for w in range(width):
         if board[h][w] == blockchar:
            # one space from edge
            if h == height - 2: # bottom
               board[h+1][w] = blockchar
            if h == 1: # top
               board[0][w] = blockchar
            if w == 1: # left
               board[h][0] = blockchar
            if w == width - 2: # right
               board[h][w + 1] = blockchar
            # two spaces from edge
            if h == height - 3: # bottom
               board[h+1][w] = blockchar
               board[h+2][w] = blockchar
            if h == 2: # top
               board[0][w] = blockchar
               board[1][w] = blockchar
            if w == 2: # left
               board[h][0] = blockchar
               board[h][1] = blockchar
            if w == width - 3:
               board[h][w + 1] = blockchar
               board[h][w + 2] = blockchar
            # one space in between
            
            # two spaces in between
        
   display(board)

def recursive_backtracking(temp, pos_list, block_count):
   display(temp)
   print("block count", block_count)
   if countblocks(temp) == block_count: return temp # check coutn number of blocks. if matching then passed
   elif countblocks(temp) > block_count: return None
   
   print("pos list", pos_list)
   
   # pos list outside while loop
   while len(pos_list) > 0:
      row, col = select_unassigned_var(pos_list) # choose randomly from position list (in while)
      tempcopy = [b[:] for b in temp]
      # put block in the selected position
      tempcopy[row][col] = blockchar
      # obvious blocks
      addobviousblockedsquare(tempcopy)
      # call palindrome
      makepalindrome(tempcopy)
      print("after palindrome")
      display(tempcopy)
      pos_list = gen_pos_list(tempcopy)
      #if isValid(value, var, assignment, variables, adjs):
        # call recursive method and get result (board)
      result = recursive_backtracking(tempcopy, pos_list, block_count)
      if result != None: return result # <<<<
   return None

def select_unassigned_var(pos_list):
   var = random.choice(pos_list)
   pos_list.remove(var)
   return var

   #if len(pos_list) == 0: return board, x
   #pick = random.randint(0, len(pos_list)-1)
   #picked_pos = pos_list[pick]
   #pos_list = pos_list[0:pick] + pos_list[pick+1:]
   #...
   #board = board[0:picked_pos] + BLOCKCHAR + board[picked_pos+1:]
   #... update the board (#s and ~s) ...
   #temp_board = recursive call with updated pos_list
   
# illegal board method (isValid)
# protected between two blocks
# protected and anything between two blocks
# space - two long
   
def countblocks(temp):
   realcount = 0
   for h in range(height):
      for w in range(width):
         if temp[h][w] == blockchar:
            realcount += 1
   print(realcount)
   return realcount
   
def gen_pos_list(board):
   pos_list = []
   for h in range(height):
      for w in range(width):
         if board[h][w] == openchar:
            # print("is open char", h * width + w, "(", h, w, ")")
            pos_list.append((h, w))
   return pos_list
   
def area_fill(board, sp, dirs = [-1, width, 1, -1*width]):
   if sp < 0 or sp >= len(board):
      return board
   if board[sp] in {openchar, protectedchar}:
      board = board[0:sp] + '?' + board[sp+1:]
      for d in dirs:
         if d == -1 and sp % width == 0:
            continue #left edge
         if d == 1 and sp+1 % width == 0:
            continue #right edge
         board = area_fill(board, sp+d, dirs)
   return board

def main():
   board = []
   makeboard(board)
   display(board)
   cleanprotected(board)
   addobviousblockedsquare(board)
   temp = [b[:] for b in board]
   finalboard = recursive_backtracking(temp, gen_pos_list(board), block_count)
   if finalboard != None:
      display(finalboard)
   
main()