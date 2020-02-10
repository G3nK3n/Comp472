def main():
 import numpy
 import copy
 
 gridSpace, startBoard, limDepth = initializeGrid()
 startDepth = 1
 dfs(gridSpace, startBoard, 0, 0, startDepth, limDepth)
 if len(openList) == 0:
  f = open("#_dfs_solution.txt", "a")
  f.write("No Solution")
  f.close()
  writeDFSSearch(gridSpace)



openList = []
closeList = []  

def dfs(someList, boardStart, posI, posJ, depthStart, depthEnd):
 try:
  goalAttained = goalCheck(someList)
  
  if goalAttained == False:
   currentValue = openList.pop() 
   
   if currentValue not in closeList:
    closeList.append(someList[posI][posJ].name)
    print("Current Value: " + currentValue)
   
    
    if depthStart != depthEnd: 
     if len(someList) != posI+1:
      if someList[posI+1][posJ].name not in closeList:
       openList.append(someList[posI+1][posJ].name)
     if len(someList) != posJ+1:
      if someList[posI][posJ+1].name not in closeList:
       openList.append(someList[posI][posJ+1].name)
    
      
    if int(someList[posI][posJ].value) == 1:
     changeValues(someList, posI, posJ)
   
    someList[posI][posJ].stateRep = stateRepresentation(someList)
    if depthStart != depthEnd:
     if posI+1 == len(someList) or posJ+1 == len(someList): 
      if len(someList) == posI+1 and len(someList) == posJ+1:
       print("Limit")
      elif len(someList) == posI+1 and someList[posI][posJ+1].name == openList[-1]:
       connectRight(someList, posI, posJ)
       dfs(someList, boardStart, posI, posJ+1, depthStart+1, depthEnd)
      elif len(someList) == posJ+1 and someList[posI+1][posJ].name == openList[-1]:
       connectDown(someList, posI, posJ)
       dfs(someList, boardStart, posI+1, posJ, depthStart+1, depthEnd)
     else: 
      if someList[posI+1][posJ].name == openList[-1]:
       connectDown(someList, posI, posJ)
       dfs(someList, boardStart, posI+1, posJ, depthStart+1, depthEnd)
       if someList[posI][posJ+1].name == openList[-1]:     
        connectRight(someList, posI, posJ)
        dfs(someList, boardStart, posI, posJ+1, depthStart+1, depthEnd)
      elif someList[posI][posJ+1].name == openList[-1]:
       connectRight(someList, posI, posJ)
       dfs(someList, boardStart, posI, posJ+1, depthStart+1, depthEnd)
       
       if someList[posI+1][posJ].name == openList[-1]:
        connectDown(someList, posI, posJ)
        dfs(someList, boardStart, posI+1, posJ, depthStart+1, depthEnd)
      else:
       print("Error")
    else:
     print("Depth limit exceeded.")   
   else:
    print("Already visited: " + someList[posI][posJ].name)
  else:
   print("SUCCESS")
   writeSuccess(someList, boardStart)
 except:
  pass

def writeDFSSearch(someList2):
 f = open("#_dfs_search.txt", "a")
 for i in range(len(someList2)):
  for j in range(len(someList2[i])): 
   f.write("0 0 0    ")
   for a in range(len(someList2[i][j].stateRep)):
    f.write(str(someList2[i][j].stateRep[a]))
   f.write("\n")

def writeSuccess(someList2, initBoard):
  f = open("#_dfs_solution.txt", "a")
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
  
  f = open("#_dfs_search.txt", "a")
  for k in range(len(closeList)):
   for i in range(len(someList2)):
    for j in range(len(someList2[i])): 
     if str(closeList[k]) == str(someList2[i][j].name):
      f.write("0 0 0    ")
      for a in range(len(someList2[i][j].stateRep)):
       f.write(str(someList2[i][j].stateRep[a]) + " ")
   f.write("\n")
         
def connectRight(someList2, x, y):
 someList2[x][y].right = someList2[x][y+1]
 someList2[x][y+1].parent = someList2[x][y]
 
def connectDown(someList2, x, y):
 someList2[x][y].down = someList2[x+1][y]
 someList2[x+1][y].parent = someList2[x][y]

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

def stateRepresentation(currentList):
 tempList = []
 for i in range(len(currentList)):
  for j in range(len(currentList[i])):
   tempList.append(int(currentList[i][j].value))
 
 return tempList
 

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
 
 print("Current values of Grid: ")
 for i in range(len(theList)):
  for j in range(len(theList[i])):
   print(theList[i][j].value, end=" ")
  print()

class MyList(list): 
 def __getitem__(self, index):
  if index < 0:
   raise IndexError("list index out of range")
  return super(MyList, self).__getitem__(index)
        
class Node:
   def __init__(self):
       self.name = ""
       self.value = 0
       self.parent = Node
       self.down = Node
       self.right = Node
       self.stateRep = []
        


#Initializes Grid
def initializeGrid():
 filename = "dfs_boards.txt"

 with open(filename, "r") as f:
  content = f.readline().split()

  #while content:
   #content = 
   #print(content)

 theDepth = int(content[1])
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
  
 openList.append(theGrid[0][0].name)

 return theGrid, initBoard, theDepth

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

#NEXT: - FIX DOCUMENT REPRESENTATION, FIX TIE BREAKER FOR BOARDS
