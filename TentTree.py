import sys

#Open and read the input file
input_file = sys.argv[1]
file = open(input_file, "r")

#Variables to store input
rowCount, colCount = 0, 0
rowConstraints, colConstraints = [], []
firstLine, secondLine, thirdLine = True, False, False
rowIndex, colIndex = 0, 0
tents = []

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
    elif thirdLine:
        #Read the third line
        colConstraints = list(map(int, line.split()))
        thirdLine = False
    else:
        #Read the Board
        boardRow = list(line.strip())
        for elem in boardRow:
            if elem == 'T':
                #Place tent to the right
                if colIndex < colCount - 1 and boardRow[colIndex + 1] == '.':
                    tents.append((rowIndex, colIndex + 1))
            #Increase the column index
            colIndex += 1
        #Reset the column index and increase the row index
        colIndex = 0
        rowIndex += 1


print("Tents: ", tents)
