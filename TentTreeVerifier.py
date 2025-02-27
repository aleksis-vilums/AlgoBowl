import sys

#Open and read the file
input_file = open(sys.argv[1], "r")

#Read the first line
violationCountFromFile = int(input_file.readline().strip())

#Read the second line
tentCount = int(input_file.readline().strip())

#Read the rest of the file
tents = []
for line in input_file:
    tents.append(line.strip().split())

#Close the file
input_file.close()

#Open and read second file
input_file = open(sys.argv[2], "r")

firstLine, secondLine, thirdLine = True, False, False
tentTreePairs = {}
board, treeLocations = [], []
rowIndex, colIndex = 0, 0

#Read the input file
for line in input_file:
    if firstLine:
        #Read the first line
        rowCount, colCount = map(int, line.split())
        firstLine = False
        secondLine = True
    elif secondLine:
        #Read the second line
        rowConstraints = list(map(int, line.split()))
        secondLine = False
        thirdLine = True
    elif thirdLine:
        #Read the third line
        colConstraints = list(map(int, line.split()))
        thirdLine = False
    else:
        #Read the Board
        boardRow = list(line.strip())
        board.append(boardRow)
        for elem in boardRow:
            if elem == 'T':
                #Place tree
                treeLocations.append((rowIndex+1, colIndex+1))
            #Increase the column index
            colIndex += 1
        #Reset the column index and increase the row index
        colIndex = 0
        rowIndex += 1

#Close the file
input_file.close()

#Place tents in the board
for tent in tents:
    row, col, direction = tent
    row = int(row)
    col = int(col)

    board[row-1][col-1] = 'X'

    #Add tent to the tenTreePair with the corresponding tree
    if direction == 'L':
        tree = (row, col - 1)
        tentTreePairs[(row, col, direction)] = tree

    if direction == 'R':
        tree = (row, col + 1)
        tentTreePairs[(row, col, direction)] = tree

    if direction == 'U':
        tree = (row - 1, col)
        tentTreePairs[(row, col, direction)] = tree

    if direction == 'D':
        tree = (row + 1, col)
        tentTreePairs[(row, col, direction)] = tree

#Calulate violation count
violationCount = 0

#Check if tent has an adjacent tent
for tent in tents:
    row, col, direction = tent

    row = int(row)
    col = int(col)

    rowIndex = row - 1
    colIndex = col - 1
    
    #Check if the tents have a corresponding tree
    if direction == 'X':
        violationCount += 1

    #Check up
    if rowIndex > 0 and board[rowIndex - 1][colIndex] == 'X':
        violationCount += 1
        continue

    #Check down
    if rowIndex < rowCount - 1 and board[rowIndex + 1][colIndex] == 'X':
        violationCount += 1
        continue

    #Check left
    if colIndex > 0 and board[rowIndex][colIndex - 1] == 'X':
        violationCount += 1
        continue

    #Check right
    if colIndex < colCount - 1 and board[rowIndex][colIndex + 1] == 'X':
        violationCount += 1
        continue

    #Check up and right
    if rowIndex > 0 and colIndex < colCount - 1 and board[rowIndex - 1][colIndex + 1] == 'X':
        violationCount += 1
        continue

    #Check up and left
    if rowIndex > 0 and colIndex > 0 and board[rowIndex - 1][colIndex - 1] == 'X':
        violationCount += 1
        continue

    #Check down and right
    if rowIndex < rowCount - 1 and colIndex < colCount - 1 and board[rowIndex + 1][colIndex + 1] == 'X':
        violationCount += 1
        continue

    #Check down and left
    if rowIndex < rowCount - 1 and colIndex > 0 and board[rowIndex + 1][colIndex - 1] == 'X':
        violationCount += 1
        continue

for tree in treeLocations:
    #Check if tree is a value in tentTreePairs
    if tree in tentTreePairs.values():
        continue
    else:
        violationCount += 1

#Check if row constraints are violated
for i in range(rowCount):
    rowSum = 0
    for j in range(colCount):
        if board[i][j] == 'X':
            rowSum += 1
    if rowSum != rowConstraints[i]:
        #Violation count is the difference between the row sum and the row constraint
        violationCount += abs(rowSum - rowConstraints[i])

#Check if column constraints are violated
for j in range(colCount):
    colSum = 0
    for i in range(rowCount):
        if board[i][j] == 'X':
            colSum += 1
    if colSum != colConstraints[j]:
        #Violation count is the difference between the column sum and the column constraint
        violationCount += abs(colSum - colConstraints[j])

#Print the violation count
print(violationCount, violationCountFromFile)

#Check if the violation count is equal to the violation count in the first file
if violationCount == violationCountFromFile:
    print("CORRECT")
else:
    print("INCORRECT")
