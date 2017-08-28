from __future__ import division
import os           # calls to os path navigation
import datetime     # keeps track of time
import csv          # allows reading and writing to csv files
import subprocess   # (different) calls to cmd line commands
import sys
import random       # used to shuffle array for better balancing
import gc           # garbage collector to save memory

# method returns currentdatetime
def time():
    return datetime.datetime.now()

# RedBlackTree
class RedBlackTree(object):
    # initializes the tree
    def __init__(self):
        self._tree = None
    # Adds node to tree and balances it
    def Insert(self, n, index):
        if self._tree == None:
            self._tree = RedBlackTreeNode(n, index)
            self._tree.SetColor("Black")
        else:
            self._tree = self._tree.Insert(n, index)
    # prints the tree
    def Print(self):
        if self._tree == None:
            print "Empty"
        else:
            self._tree.Print(1)
    # finds the closest node's value to a given value
    def closest(self, value):
        if self._tree == None:
            print "Empty"
        else:
            res = self._tree._closest(value)
            return res

# Node of tree
class RedBlackTreeNode(object):
    # initializes the node
    def __init__(self, value, index):
        self._left = None
        self._right = None
        self._value = value
        self.SetColor("Red")
        self._parent = None
        self.index = index
    # find the closest value to this node
    def _closest(self, value):
        if value == self._value:
            return self.index
        elif value < self._value:
            if self.hasLeftChild():
                return self.GetLeft()._closest(value)
            return self.index
        else:
            if self.hasRightChild():
                return self.GetRight()._closest(value)
            return self.index
    # returns the node's parent node
    def GetParent(self):
        return self._parent
    # changes the node's parent node
    def SetParent(self, parent):
        self._parent = parent
    # returns the node's color
    def GetColor(self):
        return self._color
    # changes the node's color
    def SetColor(self, color):
        self._color = color
    # returns the node's left node
    def GetLeft(self):
        return self._left
    # changes the node's left node
    def SetLeft(self, left):
        self._left = left
    # returns the node's right node
    def GetRight(self):
        return self._right
    # changes the node's right Node
    def SetRight(self, right):
        self._right = right
    # returns the node's grandparent node
    def GetGrandParent(self):
        if self.GetParent() != None:
            return self.GetParent().GetParent()
        else:
            return None
    # returns the node's uncle node
    def GetUncle(self):
        grand = self.GetGrandParent()
        if grand is not None:
            if grand.GetLeft() == self.GetParent():
                return grand.GetRight()
            else:
                return grand.GetLeft()
        else:
            return None
    # rebalances the tree's nodes
    def Rebalance(self):
        if self.GetParent() is None:
            self.SetColor("Black")
            return self
        if self.GetParent().GetColor() == "Black":
            return self.GetRoot()
        if self.GetUncle() is not None and self.GetUncle().GetColor() == "Red":
            self.GetUncle().SetColor("Black")
            self.GetParent().SetColor("Black")
            self.GetGrandParent().SetColor("Red")
            return self.GetGrandParent().Rebalance()
        return self.PivotAndRebalance()
    # returns the root node
    def GetRoot(self):
        if self.GetParent() is None:
            return self
        else:
            return self.GetParent().GetRoot()
    # pivots the tree to help rebalance
    def PivotAndRebalance(self):
        # First, distinguish between the case where where my parent is
        # a left child or a right child.
        if self.GetGrandParent().GetLeft() == self.GetParent():
            if self.GetParent().GetRight() == self:
            # WP case 4: I'm the right child of my parent, and my parent is the
            # left child of my grandparent. Pivot right around me.
                return self.PivotLeft(False)
            else:
            # WP case 5
            # If I'm the left child, and my parent is the left child, then
            # pivot right around my parent.
                return self.GetParent().PivotRight(True)
        else: # My parent is the right child.
            if self.GetParent().GetLeft() == self:
                # WP case 4, reverse.
                return self.PivotRight(False)
            else:
                # WY case 5 reverse
                return self.GetParent().PivotLeft(True)
    # pivots the tree to the right
    def PivotRight(self, recolor):
        right = self.GetRight()
        parent = self.GetParent()
        grand = self.GetGrandParent()
        parent.SetLeft(right)
        if right is not None:
            right.SetParent(parent)
        self.SetParent(grand)
        if grand is not None:
            if  grand.GetRight() == parent:
                grand.SetRight(self)
            else:
                grand.SetLeft(self)
        self.SetRight(parent)
        parent.SetParent(self)
        if recolor is True:
            parent.SetColor("Red")
            self.SetColor("Black")
            return self.GetRoot()
        else:
            return parent.Rebalance()
    # pivots the tree to the left
    def PivotLeft(self, recolor):
        left = self.GetLeft()
        parent = self.GetParent()
        grand = self.GetGrandParent()
        parent.SetRight(left)
        if left is not None:
            left.SetParent(parent)
        self.SetParent(grand)
        if grand is not None:
            if  grand.GetRight() == parent:
                grand.SetRight(self)
            else:
                grand.SetLeft(self)
        self.SetLeft(parent)
        parent.SetParent(self)
        if recolor is True:
            parent.SetColor("Red")
            self.SetColor("Black")
            return self.GetRoot()
        else:
            return parent.Rebalance()
    # inserts a value at an index in the tree
    def Insert(self, value, index):
        if self._value > value:
            if self.GetLeft() is None:
                self.SetLeft(RedBlackTreeNode(value,index))
                self.GetLeft().SetParent(self)
                return self.GetLeft().Rebalance()
            else:
                return self.GetLeft().Insert(value, index)
        else:
            if self.GetRight() is None:
                self.SetRight(RedBlackTreeNode(value,index))
                self.GetRight().SetParent(self)
                return self.GetRight().Rebalance()
            else:
                return self.GetRight().Insert(value, index)
    # prints the node
    def Print(self, indent):
        for i in range(indent):
            print "  ",
        print "%s (%s) - %s" % (self._value, self.GetColor(), self.index)
        if self.GetLeft() is None:
            for i in range(indent+1):
                print "  ",
            print "None(Black)"
        else:
            self.GetLeft().Print(indent+1)
        if self.GetRight() is None:
            for i in range(indent+1):
                print "  ",
            print "None(Black)"
        else:
            self.GetRight().Print(indent+1)
    # returns if node has a left child node
    def hasLeftChild(self):
        if self._left != None:
            return True
        return False
    # returns if node has a right child node
    def hasRightChild(self):
        if self._right != None:
            return True
        return False

print 'Start ' + str(time())

perm = time() # initial time

Base = '/Volumes'       # source folder to parse through
searchFolder = '/img'   # search for img folders
setSize = 1428672       # number of elements in the set
vehicleState = '/vehicleState.csv' # csv file

sys.setrecursionlimit(20000000) # Don't recurse too much. Helps when logic errors.

temp = time() # temporary time to check how long program has been running
print 'creating rowArr array'

# Opens vehicle state file and adds to an array
with open(Base + vehicleState, 'rb') as csvfile:
    rowArr = []
    csvReader = csv.reader(csvfile, delimiter=';', quotechar='|')#check the delimiter
    print 'csv opened'
    index = 0
    gc.disable()
    for row in csvReader:
        rowArr.append([float(item.replace(',','0')) for item in row])
        # prints status update
        if index%200000 == 0:
            print str(index) + ' rows added to rowArr: ' + (str(index/200000)[:5]) + '% done'
        index+=1

print 'rowArr array created. ' + str(time()-temp) + ' current time: ' + str(time())
random.shuffle(rowArr) #shuffles to balance tree better
print 'rowArr array shuffled. ' + str(time()-temp)  + ' current time: ' + str(time())

temp = time() # temporary time to check how long program has been running
print 'creating vsTime array' + ' current time: ' + str(time())
vsTime = [] # list of times from vehicleState.csv
index = 0   # keeps track of the index
# parses through file to extract a single column that we need
for row in rowArr:
    vsTime.append(row[0])
    # prints status update
    if index%1000000 == 0:
        print str(index) + ' rows added to vsTime: ' + (str(index/200000)[:5]) + '% done'
    index+=1
print 'vsTime array created. ' + str(time()-temp)

# creates the redBlackTree with vsTime data
temp=time() # temporary time to check how long program has been running
print 'Creating Binary Tree of vsTime'  + ' current time: ' + str(time())
tree = RedBlackTree() #creates Binary Tree
tree.__init__() #Initializes Binary Tree
for x in xrange(len(rowArr)):
    tree.Insert(vsTime[x],x)
    # prints status update
    if x%500000 == 0: #500000
        print str(x) + ' rows populated: ' + ((str(x/200000))[:5]) + '% done ' + str(time())
print 'Binary Tree built. ' + str(time()-temp)

temp=time() # temporary time to check how long program has been running

# create an array of imgFiles by searching through folders for searchFolders
print 'Creating imgName array' + ' current time: ' + str(time())
os.chdir(Base + searchFolder)
proc = subprocess.Popen('ls', stdout=subprocess.PIPE)
imgName = proc.stdout.read().splitlines() #list of names of image files
os.chdir(Base)
print 'imgName array created ' + str(time()-temp) + ' current time: ' + str(time())

temp=time() # temporary time to check how long program has been running

# create imgTime array from column of imgName files
print 'Creating imgTime array' + ' current time: ' + str(time())
imgTime = [] #list of imgTimes
for x in xrange(setSize):
    imgTime.append(float(imgName[x].split('cam')[1].split('.')[0].replace('_','.')))
    if x % 50000 == 0:
        print str(x) + ' imgTime created: ' + ((str(x/200000))[:5]) + '% done ' + str(time())
print'imgTime array created ' + str((time()-temp).microseconds) + ' current time: ' + str(time())

gc.enable()
gc.disable()

# Search through arrays and create a new array by matching up times.
print 'Commencing search. ' + ' current time: ' + str(time())
temp=time()
timeLocFile = '/timeLocAllv2.csv' #TimeLocation
with open(Base + timeLocFile, 'wb') as csvfile:
    csvWriter = csv.writer(csvfile,delimiter=',')
    index = 0
    csvWriter.writerow(['imgName','imgTime','vsTime','xLoc','yLoc','yaw','xSpeed','ySpeed'])
    for item in imgTime:
        x = tree.closest(item)
        csvWriter.writerow([imgName[index],imgTime[index]]+rowArr[x])
        if index % 100000 == 0:
            print str(index) + ' rows searched, matched and written: ' + (str(index/15000)[:5]) + '% done'
        index+=1
gc.enable()
print 'timeLocAll csv created. Done. ' + str(time()-temp) + ', total time: ' + str(time()-perm) + ' current time: ' + str(time())
