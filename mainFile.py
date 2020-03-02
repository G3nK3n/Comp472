from queue import PriorityQueue
import numpy
import copy

openList = PriorityQueue()
openList2 = []
closeList = []

# The main function
def main():
 filename = "dfs_boards.txt"
 counter = 0
 with open(filename, "r") as f:
  while True:
   content = f.readline().split() 
    
   if not content:
    break
   closeList.clear()
   
   #gridSpace, startBoard, limDepth = initializeGrid(content)
   #startDepth = 1
   #dfs(gridSpace, startBoard, 0, 0, startDepth, limDepth, counter) 
   #print(closeList)
  
   closeList.clear()
   gridSpace, startBoard, limPathLength = initializeGrid(content)
   
   if int(gridSpace[0][0].value) == 1:
    changeValues(gridSpace, 0, 0) 
 
   initialNodeHeuristic = heuristicFunction(gridSpace)
   gridSpace[0][0].heuristicValue = initialNodeHeuristic 
   gridSpace[0][0].stateRep = stateRepresentation(gridSpace)
   gridSpace[0][0].fOfN = gridSpace[0][0].gOfN + gridSpace[0][0].heuristicValue
   openList.put((gridSpace[0][0].heuristicValue, gridSpace[0][0].name))
 
   print("Initial values of Grid: ")
   for i in range(len(gridSpace)):
    for j in range(len(gridSpace[i])):
     print(gridSpace[i][j].value, end=" ")
    print()

   bfs(gridSpace, limPathLength, counter, startBoard)
   print(closeList)

   closeList.clear()
   reInitionalizeNode(gridSpace)

   gridSpace, startBoard, limPathLength = initializeGrid(content)
 
 
   if int(gridSpace[0][0].value) == 1:
    changeValues(gridSpace, 0, 0) 
 
   initialNodeHeuristic = heuristicFunction(gridSpace)
   gridSpace[0][0].heuristicValue = initialNodeHeuristic 
   gridSpace[0][0].stateRep = stateRepresentation(gridSpace)
   gridSpace[0][0].fOfN = gridSpace[0][0].gOfN + gridSpace[0][0].heuristicValue
   openList.put((gridSpace[0][0].fOfN, gridSpace[0][0].name))
 
   print("Initial values of Grid: ")
   for i in range(len(gridSpace)):
    for j in range(len(gridSpace[i])):
     print(gridSpace[i][j].value, end=" ")
    print()
  
   algorithmA(gridSpace, limPathLength, counter, startBoard)
   print(closeList)
   
   counter = counter + 1


#--------------------------------------------------------------------------------

#--- DFS function 
def dfs(someList, boardStart, posI, posJ, depthStart, depthEnd, puzzleNumber):
 try:
  goalAttained = goalCheck(someList)
  functionName = "DFS"
  
  if goalAttained == False:
   
   currentValue = openList2.pop() 
   if currentValue not in closeList:
    closeList.append(someList[posI][posJ].name)
    print("Current Value: " + currentValue)  
    
    if depthStart != depthEnd:  
     if len(someList) != posI+1:
      if someList[posI+1][posJ].name not in closeList:
       openList2.append(someList[posI+1][posJ].name)
     if len(someList) != posJ+1:
      if someList[posI][posJ+1].name not in closeList:
       openList2.append(someList[posI][posJ+1].name)
      
    if int(someList[posI][posJ].value) == 1:
     changeValues(someList, posI, posJ)
   
    someList[posI][posJ].stateRep = stateRepresentation(someList)
    if depthStart != depthEnd:
     if posI+1 == len(someList) or posJ+1 == len(someList): 
      if len(someList) == posI+1 and len(someList) == posJ+1:
       print("Limit")
      elif len(someList) == posI+1 and someList[posI][posJ+1].name == openList2[-1]:
       connectRight(someList, posI, posJ)
       dfs(someList, boardStart, posI, posJ+1, depthStart+1, depthEnd)
      elif len(someList) == posJ+1 and someList[posI+1][posJ].name == openList2[-1]:
       connectDown(someList, posI, posJ)
       dfs(someList, boardStart, posI+1, posJ, depthStart+1, depthEnd)
     else: 
      if someList[posI+1][posJ].name == openList2[-1]:
       connectDown(someList, posI, posJ)
       dfs(someList, boardStart, posI+1, posJ, depthStart+1, depthEnd)
       if someList[posI][posJ+1].name == openList2[-1]:     
        connectRight(someList, posI, posJ)
        dfs(someList, boardStart, posI, posJ+1, depthStart+1, depthEnd)
      elif someList[posI][posJ+1].name == openList2[-1]:
       connectRight(someList, posI, posJ)
       dfs(someList, boardStart, posI, posJ+1, depthStart+1, depthEnd)
       
       if someList[posI+1][posJ].name == openList2[-1]:
        connectDown(someList, posI, posJ)
        dfs(someList, boardStart, posI+1, posJ, depthStart+1, depthEnd)
     
      #else:
      # print("Error")
    else:
     print("Depth limit exceeded.")   
   else:
    print("Already visited: " + someList[posI][posJ].name)
  else:
   print("SUCCESS")
   writeSuccess(someList, boardStart)

  print("DFS")
  if goalAttained==True:
   print("SUCCESS")
   writeSuccess(someList, boardStart, puzzleNumber, functionName, goalAttained)
   writeSearch(someList, puzzleNumber, functionName)
  if goalAttained==False:
   print("No Solution")
   writeSuccess(someList, boardStart, puzzleNumber, functionName, goalAttained)
   writeSearch(someList, puzzleNumber, functionName) 
 except:
  pass


#--- Best First Search Function
def bfs(someList, maxPathLength, puzzleNumber, initBoard):
 try:
  goalAttained = False
  currentPathTotal = 0
  posI = 0
  posJ = 0  
  while openList.empty() == False:
   
   goalAttained = goalCheck(someList)
   
   if goalAttained == False:
    
    if currentPathTotal < maxPathLength:
     currentValue = openList.get(block=False)
     openList.task_done()

     if posI != 0 and posJ !=0:
      if any(currentValue[0] in item for item in openList.queue) == True:
       currentValue = tieBreaker(currentValue, currentValue[0], someList)
     
     posI, posJ = pointerBoard(someList, currentValue[1])
     currentPathTotal = currentPathTotal + someList[posI][posJ].heuristicValue 

     if currentValue[1] not in closeList:
      closeList.append(someList[posI][posJ].name)
      if len(someList) != posI+1:
       if someList[posI+1][posJ].name not in closeList:
        if any(someList[posI+1][posJ].name in item for item in openList.queue) == False:   
         nodeBoardRepresentation = ''.join(str(e) for e in someList[posI][posJ].stateRep)
         createBoard(someList, nodeBoardRepresentation)
         if int(someList[posI+1][posJ].value) == 1:
          changeValues(someList, posI+1, posJ) 
         currentHeuristic = heuristicFunction(someList)
         someList[posI+1][posJ].heuristicValue = currentHeuristic
         someList[posI+1][posJ].stateRep = stateRepresentation(someList)
         print(someList[posI+1][posJ].stateRep)
         connectDown(someList, posI, posJ)
         someList[posI+1][posJ].fOfN = someList[posI+1][posJ].gOfN + someList[posI+1][posJ].heuristicValue
         openList.put((someList[posI+1][posJ].heuristicValue, someList[posI+1][posJ].name))
      if len(someList) != posJ+1:
       if someList[posI][posJ+1].name not in closeList:
        if any(someList[posI][posJ+1].name in item for item in openList.queue) == False:
         nodeBoardRepresentation = ''.join(str(e) for e in someList[posI][posJ].stateRep)
         createBoard(someList, nodeBoardRepresentation)
         if int(someList[posI][posJ+1].value) == 1:
          changeValues(someList, posI, posJ+1)
         currentHeuristic = heuristicFunction(someList)
         someList[posI][posJ+1].heuristicValue = currentHeuristic
         someList[posI][posJ+1].stateRep = stateRepresentation(someList)
         print(someList[posI][posJ+1].stateRep)
         connectRight(someList, posI, posJ)
         someList[posI][posJ+1].fOfN = someList[posI][posJ+1].gOfN + someList[posI][posJ+1].heuristicValue
         openList.put((someList[posI][posJ+1].heuristicValue, someList[posI][posJ+1].name))
    else:
     print("Max length exceeded")
     break 
   elif goalAttained == True and openList.empty() == False:
     print("Success!")
     break  

  functionName = "BFS"
  writeSuccess(someList, initBoard, puzzleNumber, functionName, goalAttained)
  
  writeSearch(someList, puzzleNumber, functionName)
 
 except:
  pass 


#---- Algorthim A Function
def algorithmA(someList, maxPathLength, puzzleNumber, initBoard):
 try:
  currentPathTotal = 0
  goalAttained = False
  posI = 0
  posJ = 0  
  while openList.empty() == False:
   
   goalAttained = goalCheck(someList)
   
   if goalAttained == False:
    
    if currentPathTotal < maxPathLength:
     currentValue = openList.get(block=False)
     openList.task_done()

     if posI != 0 and posJ !=0:
      if any(currentValue[0] in item for item in openList.queue) == True:
       currentValue = tieBreaker(currentValue, currentValue[0], someList)
     
     posI, posJ = pointerBoard(someList, currentValue[1])
     currentPathTotal = currentPathTotal + someList[posI][posJ].heuristicValue 

     if currentValue[1] not in closeList:
      closeList.append(someList[posI][posJ].name)
      if len(someList) != posI+1:
       if someList[posI+1][posJ].name not in closeList:
        if any(someList[posI+1][posJ].name in item for item in openList.queue) == False:   
         nodeBoardRepresentation = ''.join(str(e) for e in someList[posI][posJ].stateRep)
         createBoard(someList, nodeBoardRepresentation)
         if int(someList[posI+1][posJ].value) == 1:
          changeValues(someList, posI+1, posJ) 
         currentHeuristic = heuristicFunction(someList)
         someList[posI+1][posJ].heuristicValue = currentHeuristic
         someList[posI+1][posJ].stateRep = stateRepresentation(someList)
         connectDown(someList, posI, posJ)
         someList[posI+1][posJ].gOfN = int(someList[posI][posJ].gOfN) + 1
         someList[posI+1][posJ].fOfN = someList[posI+1][posJ].gOfN + someList[posI+1][posJ].heuristicValue
         openList.put((someList[posI+1][posJ].fOfN, someList[posI+1][posJ].name))
      if len(someList) != posJ+1:
       if someList[posI][posJ+1].name not in closeList:
        if any(someList[posI][posJ+1].name in item for item in openList.queue) == False:
         nodeBoardRepresentation = ''.join(str(e) for e in someList[posI][posJ].stateRep)
         createBoard(someList, nodeBoardRepresentation)
         if int(someList[posI][posJ+1].value) == 1:
          changeValues(someList, posI, posJ+1)
         currentHeuristic = heuristicFunction(someList)
         someList[posI][posJ+1].heuristicValue = currentHeuristic
         someList[posI][posJ+1].stateRep = stateRepresentation(someList)
         connectRight(someList, posI, posJ)
         someList[posI][posJ+1].gOfN = int(someList[posI][posJ].gOfN) + 1
         someList[posI][posJ+1].fOfN = someList[posI][posJ+1].gOfN + someList[posI][posJ+1].heuristicValue
         openList.put((someList[posI][posJ+1].fOfN, someList[posI][posJ+1].name))
    else:
     print("Max length exceeded")
     break 
   elif goalAttained == True and openList.empty() == False:
     print("Success!")  
     break

  functionName = "A*"
  writeSuccess(someList, initBoard, puzzleNumber, functionName, goalAttained)
  writeSearch(someList, puzzleNumber, functionName)
 except:
  pass 

#--------------------------------------------------------------------------------

#--- This function writes to the solution file depending if there is a solution or not
def writeSuccess(someList2, initBoard, puzzleNum, funcName, SucOrNot):
  fileName = "solution.txt"
  if funcName == "BFS": 
   fullFileName = str(puzzleNum) + "_BFS_" + fileName
  elif funcName == "A*":
   fullFileName = str(puzzleNum) + "_astar_" + fileName
  elif funcName == "DFS":
   fullFileName = str(puzzleNum) + "_DFS_" + fileName 
  
  f = open(fullFileName, "a")
  f.write("Puzzle number " + str(puzzleNum) + " Representation(Solutions)\n")
  f.write("-------------------------\n")


  if SucOrNot == True:
   f.write("0    ")
   for i in range(len(initBoard)):
    for j in range(len(initBoard[i])):  
     f.write(initBoard[i][j].value + " ")
   f.write("\n")
  
   for k in range(len(closeList)):
    for i in range(len(someList2)):
     for j in range(len(someList2[i])): 
      if str(closeList[k]) == str(someList2[i][j].name):
       f.write(someList2[i][j].name + "    ")
       for a in range(len(someList2[i][j].stateRep)):
        f.write(str(someList2[i][j].stateRep[a]) + " ")
    f.write("\n")
  else:
   f.write("No Solution\n") 

#This writes the DFS Search to the text file
def writeSearch(someList2, puzzleNum, funcName):
 fileName = "search.txt"
 if funcName == "BFS": 
  fullFileName = str(puzzleNum) + "_BFS_" + fileName
 elif funcName == "A*":
  fullFileName = str(puzzleNum) + "_astar_" + fileName
 elif funcName == "DFS":
  fullFileName = str(puzzleNum) + "_DFS_" + fileName
 f = open(fullFileName, "a")
 
 f.write("Puzzle number " + str(puzzleNum) + " Representation(Search)\n")
 f.write("-------------------------\n")
 for i in range(len(someList2)):
  for j in range(len(someList2[i])):
   f.write(str(someList2[i][j].fOfN) + " " + str(someList2[i][j].gOfN) + " " + str(someList2[i][j].heuristicValue) + " ")
   for a in range(len(someList2[i][j].stateRep)):
    f.write(str(someList2[i][j].stateRep[a]))
   f.write("\n")
 f.write("\n")

#--- This calculates the heuristic function
def heuristicFunction(someList):
 totalBlack = 0
 for i in range(len(someList)):
  for j in range(len(someList[i])):
   if int(someList[i][j].value) == 1: 
    totalBlack = totalBlack + 1
 return totalBlack

#--- This function compares the equivalent boards if the openList has the same heuristic value
def tieBreaker(currentNode, currentValueNode, theList):
 try:
  temp = openList.get()
  curI, curJ = pointerBoard(theList, currentNode[1])
  i, j = pointerBoard(theList, temp[1])
  currentRep = theList[curI][curJ].stateRep
  tempRep = theList[i][j].stateRep
  sameBoard = True
  theLength = len(currentRep)-1
  for t in range(theLength): 
   if currentRep[t] != tempRep[t]:
    sameBoard = False 
    if currentRep[t] == 0 and tempRep[t] == 1:
     openList.put((temp))
     print("Priority goes to: " + currentNode[1])
     return currentNode
    elif currentRep[t] == 1 and tempRep[t] == 0:
     openList.put((currentNode))
     print("Priority goes to: " + temp[1])
     return temp
    break
  if sameBoard == True: 
   openList.put(temp)
   print("They are equal")
   return currentNode 
 except:
  pass
  print("Not working")


#This funtion connects the current Node to the right Node 
def connectRight(someList2, x, y):
 someList2[x][y].right = someList2[x][y+1]
 someList2[x][y+1].parent = someList2[x][y]

#This funtion connects the current Node to the bottom of the Node 
def connectDown(someList2, x, y):
 someList2[x][y].down = someList2[x+1][y]
 someList2[x+1][y].parent = someList2[x][y]

#---This function checks if the goal is met, in this case all of the values should be white(Or value 0)
def goalCheck(someList2):
 isGoal = True
 for i in range(len(someList2)):
  for j in range(len(someList2[i])):
   if int(someList2[i][j].value) == 1:
    isGoal = False
    break
  if isGoal == False:
   break
 return isGoal

#This function creates the State Representation for each Nodes passed.
def stateRepresentation(currentList):
 tempList = []
 for i in range(len(currentList)):
  for j in range(len(currentList[i])):
   tempList.append(int(currentList[i][j].value))
 return tempList

#---This function returns the indexes of the Node currently popped from the openList 
def pointerBoard(someList, nodeName):
 isFound = False
 for i in range(len(someList)):
  for j in range(len(someList[i])):
   if someList[i][j].name == nodeName:
    isFound = True
    break
  if isFound == True:
   break
 return i, j

# Test to see if we can change the values of the other directions 
def changeValues(theList, pI, pJ):
 theList[pI][pJ].value = 0
 
 try:
  if int(theList[pI+1][pJ].value) == 1:
   theList[pI+1][pJ].value = 0
  elif int(theList[pI+1][pJ].value) == 0:
   theList[pI+1][pJ].value = 1
 except:
  pass
 
 try:
  if int(theList[pI-1][pJ].value) == 1:
   theList[pI-1][pJ].value = 0
  elif int(theList[pI-1][pJ].value) == 0:
   theList[pI-1][pJ].value = 1
 except:
  pass
 
 try: 
  if int(theList[pI][pJ+1].value) == 1:
   theList[pI][pJ+1].value = 0
  elif int(theList[pI][pJ+1].value) == 0:
   theList[pI][pJ+1].value = 1
 except:
  pass
 
 try:
  if int(theList[pI][pJ-1].value) == 1:
   theList[pI][pJ-1].value = 0
  elif int(theList[pI][pJ-1].value) == 0:
   theList[pI][pJ-1].value = 1
 except:
  pass

#--------------------------------------------------------------------------------

#---This function initializes the State Space(The game board)
def initializeGrid(content):

 thePathLength = int(content[2])
 gridValues = content[3]
   
 theGrid = MyList([MyList([Node() for i in range(int(content[0]))]) for j in range(int(content[0]))])
 initBoard = MyList([MyList([Node() for i in range(int(content[0]))]) for j in range(int(content[0]))])

 createBoard(theGrid, gridValues)
 createBoard(initBoard, gridValues)

 # This outputs the grid
 print()
 print("Current values of Grid: ")
 for i in range(len(theGrid)):
  for j in range(len(theGrid[i])):
   print(theGrid[i][j].value, end=" ")
  print()
 
 print()

 # This outputs the name of the Node
 print("Outputting names of nodes: ") 
 for i in range(len(theGrid)):
  for j in range(len(theGrid[i])):
   print(theGrid[i][j].name, end=" ")
  print()
 
 print()

 return theGrid, initBoard, thePathLength

#Creates the board with the List of Nodes and its values
def createBoard(theList, theValues):
 counter = 0
 for i in range(len(theList)):
  for j in range(len(theList[i])):
   if counter != len(theValues):
    theList[i][j].value = theValues[counter]
    counter+=1
         
    if i == 0:
     theList[i][j].name = "A" + str(j)
    elif i == 1:
     theList[i][j].name = "B" + str(j)
    elif i == 2:
     theList[i][j].name = "C" + str(j)
    elif i == 3:
     theList[i][j].name = "D" + str(j)
    elif i == 4:
     theList[i][j].name = "E" + str(j)
    elif i == 5:
     theList[i][j].name = "F" + str(j)
    elif i == 6:
     theList[i][j].name = "G" + str(j)
    elif i == 7:
     theList[i][j].name = "H" + str(j)
    elif i == 8:
     theList[i][j].name = "I" + str(j)
    elif i == 9:
     theList[i][j].name = "J" + str(j)

def reInitionalizeNode(theList):
 for i in range(len(theList)):
  for j in range(len(theList[i])):
   theList[i][j].name = ""
   theList[i][j].value = 0
   theList[i][j].parent = Node
   theList[i][j].down = Node
   theList[i][j].right = Node
   theList[i][j].stateRep = []
   theList[i][j].heuristicValue = 0
   theList[i][j].gOfN = 0
   theList[i][j].fOfN = 0
#--------------------------------------------------------------------------------

#This class is a random class that throws an out of bound negative integer when accessing a list.
class MyList(list): 
 def __getitem__(self, index):
  if index < 0:
   raise IndexError("list index out of range")
  return super(MyList, self).__getitem__(index)

#The Node class and its values        
class Node:
   def __init__(self):
       self.name = ""
       self.value = 0
       self.parent = Node
       self.down = Node
       self.right = Node
       self.stateRep = []
       self.heuristicValue = 0
       self.gOfN = 0
       self.fOfN = 0

