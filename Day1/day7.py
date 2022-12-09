import os
from heapq import heappush, heappop

def readInputFile(fileName):
    __location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__))) + '\\' + fileName
    inputFile = open(__location__, 'r')
    inputLines = inputFile.readlines()
    inputLines = [x.strip('\n') for x in inputLines ]

    return inputLines

class Node:
    def __init__(self, name, parent, isFile, children, size):
        self.name = name
        self.parent = parent
        self.isFile = isFile
        self.children = children # Files cannot have children
        self.size = size # Dirs can have size but must not be set in constructor

        assert ((isFile and not children) or (not isFile))

    # Swap around between part 1 and 2 for easier easiness
    def __lt__(self, other):
        return self.size < other.size

    
# DFS
# State is split/wonky between the tree and heap
def getDirSizes(root, daHeap):
    size = 0
    if root.isFile:
        size = root.size
    else:
        for child in root.children:
            size += getDirSizes(root.children[child], daHeap)

        root.size = size
        heappush(daHeap, root)
    
    return size

def generateTree(inputLines, root):
    rootTrue = root
    modeInput = False
    modeLs = False
    modeDir = False
    modeDirSize = False
    modeCd = False
    modeFile = False
    fileSize = 0
    for line in inputLines:
        splitLine = line.split()
        for word in splitLine:
            if word == "$":
                modeLs = False
                modeDir = False
                modeCd = False
                modeInput = True
            elif modeCd:
                dir = word
                if dir == "/":
                    root = rootTrue
                elif dir == "..":
                    assert(root.name != "/")
                    root = root.parent
                else:
                    assert(dir in root.children) # Must ls prior to cd
                    root = root.children[dir]
                modeCd = False
                modeInput = False
            elif word == "dir":
                modeDir = True
            elif modeDir:
                dir = word
                assert(dir not in root.children) # Cannot add existing dir
                root.children[dir] = Node(dir, root, False, {}, 0)
                modeDir = False
            elif modeInput:
                if word == "cd":
                    modeCd = True
                elif word == "ls":
                    modeLs = True
                modeInput = False
            elif modeFile:
                fileName = word
                root.children[fileName] = Node(fileName, root, True, {}, fileSize)
                modeFile = False
            elif modeLs: # File size
                modeFile = True
                fileSize = int(word)

    daHeap = []
    getDirSizes(rootTrue, daHeap)

    return daHeap
                
root = Node("/", None, False, {}, 0)

inputLines = readInputFile("input.txt")
daHeap = generateTree(inputLines, root)

daSum = 0
for dir in daHeap:
    daSum += dir.size

# Find largest value greater than the target free space
spaceFree = 70000000 - daHeap[-1].size
freeTarget = 30000000
lastGreatest = 0
while daHeap:
    newGreatest = heappop(daHeap).size
    if (spaceFree + newGreatest) >= freeTarget:
        lastGreatest = newGreatest
        break
    else:
        lastGreatest = newGreatest

# print(daSum) # Part 1
print(lastGreatest) # Part 2