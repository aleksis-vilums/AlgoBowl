import sys
import random
import copy

#Open and read the input file
input_file = sys.argv[1]
file = open(input_file, "r")

#Variables to store input
rowCount, colCount = 0, 0
rowConstraints, colConstraints = [], []
firstLine, secondLine, thirdLine = True, False, False
rowIndex, colIndex = 0, 0
startBoard = []

bestTents, bestViolationCount = [], float('inf') 

#Read the input file
for line in file:
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

        #remove rows with zero constraints
        removedRows = [i+1 for i, num in enumerate(rowConstraints) if num == 0]

    elif thirdLine:
        #Read the third line
        colConstraints = list(map(int, line.split()))
        thirdLine = False

        #remove cols with zero constraints
        removedCols = [i+1 for i, num in enumerate(colConstraints) if num == 0]

    else:
        #Read the Board
        boardRow = list(line.strip())
        startBoard.append(boardRow)

#Close the file
file.close()

for i in range(25):
    tents, treeLocations = [], []
    tentTreePairs = {}
    board = copy.deepcopy(startBoard)

    #Iterate through the board
    for row in range(rowCount):
        for col in range(colCount):
            if board[row][col] == 'T':
                #All the potential tent locations up, right, down, left
                potentialTents = [(row+1, col+2, 'L'), (row+1, col, 'R'), (row+2, col+1, 'U'), (row, col+1, 'D')]

                potentialTents = [
                    (r, c, d) for r, c, d in potentialTents 
                    if not (
                        r < 1 or r >= rowCount + 1 or 
                        c < 1 or c >= colCount + 1 or 
                        board[r - 1][c - 1] == 'T' or 
                        board[r - 1][c - 1] == 'X' or
                        r in removedRows or 
                        c in removedCols
                    )
                ]

                #From the potential tents, add a random tent to the list of tents
                if potentialTents:
                    #Choose a random tent from the list
                    chosenTent = random.choice(potentialTents)
                    tentRow, tentCol, direction = chosenTent

                    #Place Tree
                    treeLocations.append((row+1, col+1))
                    tents.append(chosenTent)
                    board[tentRow-1][tentCol-1] = 'X'

    #Place tents in the board
    for tent in tents:
        row, col, direction = tent
        board[row-1][col-1] = 'X'

        #Add tent to the tenTreePair with the corresponding tree
        if direction == 'L':
            tree = (row, col - 1)
            tentTreePairs[tent] = tree

        if direction == 'R':
            tree = (row, col + 1)
            tentTreePairs[tent] = tree

        if direction == 'U':
            tree = (row - 1, col)
            tentTreePairs[tent] = tree

        if direction == 'D':
            tree = (row + 1, col)
            tentTreePairs[tent] = tree

    #Calulate violation count
    currViolationCount = 0

    #Check if tent has an adjacent tent
    for tent in tents:
        row, col, direction = tent

        rowIndex = row - 1
        colIndex = col - 1
        
        #Check if the tents have a corresponding tree
        if direction == 'X':
            currViolationCount += 1

        #Check up
        if rowIndex > 0 and board[rowIndex - 1][colIndex] == 'X':
            currViolationCount += 1
            continue

        #Check down
        if rowIndex < rowCount - 1 and board[rowIndex + 1][colIndex] == 'X':
            currViolationCount += 1
            continue

        #Check left
        if colIndex > 0 and board[rowIndex][colIndex - 1] == 'X':
            currViolationCount += 1
            continue

        #Check right
        if colIndex < colCount - 1 and board[rowIndex][colIndex + 1] == 'X':
            currViolationCount += 1
            continue

        #Check up and right
        if rowIndex > 0 and colIndex < colCount - 1 and board[rowIndex - 1][colIndex + 1] == 'X':
            currViolationCount += 1
            continue

        #Check up and left
        if rowIndex > 0 and colIndex > 0 and board[rowIndex - 1][colIndex - 1] == 'X':
            currViolationCount += 1
            continue

        #Check down and right
        if rowIndex < rowCount - 1 and colIndex < colCount - 1 and board[rowIndex + 1][colIndex + 1] == 'X':
            currViolationCount += 1
            continue

        #Check down and left
        if rowIndex < rowCount - 1 and colIndex > 0 and board[rowIndex + 1][colIndex - 1] == 'X':
            currViolationCount += 1
            continue

    for tree in treeLocations:
        #Check if tree is a value in tentTreePairs
        if tree in tentTreePairs.values():
            continue
        else:
            currViolationCount += 1

    #Check if row constraints are violated
    for i in range(rowCount):
        rowSum = 0
        for j in range(colCount):
            if board[i][j] == 'X':
                rowSum += 1
        if rowSum != rowConstraints[i]:
            #Violation count is the difference between the row sum and the row constraint
            currViolationCount += abs(rowSum - rowConstraints[i])

    #Check if column constraints are violated
    for j in range(colCount):
        colSum = 0
        for i in range(rowCount):
            if board[i][j] == 'X':
                colSum += 1
        if colSum != colConstraints[j]:
            #Violation count is the difference between the column sum and the column constraint
            currViolationCount += abs(colSum - colConstraints[j])

    #print row and col constraints
    #print('Row Constraints: ', rowConstraints)
    #print('Column Constraints: ', colConstraints)

    #Print the board
    #for row in board:
        #print(' '.join(row))

    #Print the number of violations
    print('Number of Violations: ', currViolationCount)

    if currViolationCount < bestViolationCount:
        bestViolationCount = currViolationCount
        bestTents = tents

#Write to output file
output_file = sys.argv[2]
file = open(output_file, "w")

#Write the violation count to the output file
file.write(str(bestViolationCount) + '\n')
#Write number of tents
file.write(str(len(bestTents)) + '\n')
#Write the tents to the output file
for tent in bestTents:
    row, col, direction = tent
    file.write(str(row) + ' ' + str(col) + ' ' + direction + '\n')
