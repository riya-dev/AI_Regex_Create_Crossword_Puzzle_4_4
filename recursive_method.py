def backtracking_search(variables, adjs, shapes, frame): 
   return recursive_backtracking({}, variables, adjs, shapes, frame)

def recursive_backtracking(assignment, variables'''pos list''', adjs, shapes, frame): # pass goal as argument
   # Refer the pseudo code given in class.
   ''' your code goes here '''
   if check_complete(assignment, variables, adjs): return assignment # check coutn number of blocks. if matching then apssed
   # pos list outside while loop
   for value in variables[var]: # while loop until pos list is empty
      var = select_unassigned_var(assignment, variables, adjs) # choose randomly from position list (in while)
      # put block in the selected position
      # obvious blocks
      # call palindrome
      if isValid(value, var, assignment, variables, adjs):
         # call recursive method and get result (board)
         result = recursive_backtracking(assignmentcopy, variablescopy, adjs, shapes, frame)
         if result != None: return result # <<<<
   return None
   
# need isValid method