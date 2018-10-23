#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import numpy as np

# This class is used to biild FP-tree.
class node():
    def __init__(self, value=None, parentNode=None):
        self.count = 0
        self.value = value
        self.parentNode = parentNode
        self.sonNodes = []
    def setParent(self, parent):
        self.parentNode = parent
    def addSon(self, son):
        self.sonNodes.append(son)
    def removeSon(self, son):
        self.sonNodes.remove(son)
    def addCount(self):
        self.count = self.count + 1
    def setCount(self, count):
        self.count = count
    def getValue(self):
        return self.value
    def getCount(self):
        return self.count
    def getParent(self):
        return self.parentNode
    def getSons(self):
        return self.sonNodes 
    def printInfo(self):
        print('Node Name:', self.value)
        print('Parent :', None if self.parentNode == None else self.parentNode.getValue())
        print('Son :', [son.getValue() for son in self.sonNodes])
# This class is used to build head node list.
class node_head():
    def __init__(self, value):
        self.value = value
        self.nodelist = []
    def addNode(self, node):
        self.nodelist.append(node)
    def getValue(self):
        return self.value
    def getList(self):
        return self.nodelist

def findNode(head, target):
    if head.getSons() == []:
        return None
    else:
        for son in head.getSons():
            if son.getValue() == target:
                return son
    return None
# print node from head to buttom
def printNode(h):
    print(h.getValue(),h.getCount())
    if h.getSons() == []:
        print('-End-')
    else:
        for son in h.getSons():
            printNode(son)
# print node for node to head
def printNodeUp(s, tracklist):
    p = s.getParent()
    if p.getValue() == None:
        print('-End-')
    else:
        print(p.getValue(), p.getCount())
        tracklist.append((p.getValue(), p.getCount()))
        tracklist = printNodeUp(p, tracklist)
    return tracklist 
# load file to df
def loadData(fileName):
    df = pd.DataFrame(columns=['CostumeID', 'tractID', 'Item'])
    with open('data', 'r') as f:
        index = 0
        for line in f:
            df.loc[index] = line.split()
            index = index + 1
    df = df.astype(int)
    sector = df.groupby('CostumeID')
    df2 = pd.DataFrame(columns=['CostumeID','ItemList'])
    for i in range(1, list(df['CostumeID'])[-1]):
           df2.loc[i] = [i, list(sector.get_group(i)['Item'])]
    return df2
# print Patteren 
def printPatteren(h, l, minSup, value, total):
    def check_add(l_old, item_new):
        if  item_new in l_old:
            l_old[l_old.index(item_new)][-1]+=item_new[-1]
        else:
            l_old.append(item_new)
    sons = h.getSons()
    if sons == []:
        print('-End-')
    else:
        for son in sons:
            l0 = l.copy()
            if son.getCount() < minSup:
                break
            else:
                l1 = [son.getValue(), value, son.getCount()]
                print(l1)
                check_add(total,l1)
                if l!=[]:
                    l2 = l + l1
                    print(l2)
                    check_add(total,l2)
                l0.append(son.getValue())
                total = printPatteren(son, l0, minSup, value, total)
    return total

# ---------------

# load data
df = loadData('data')
# count all item in frequency
# m use map item to order by frequency
totalList = []
for l in df['ItemList']:
    for item in l:
        totalList.append(item)
frequency = pd.Series(totalList).value_counts()
headList = [node_head(item) for item in frequency.index]

m = pd.Series(list(range(len(frequency))),index=frequency.index)

# build FP-tree
headNode = node()
for itemlist in df['ItemList']:
    head = headNode
    for item in itemlist:
        theNode = findNode(head, item)
        if theNode == None:
            x = node(value=item, parentNode=head)
            x.addCount()
            headList[list(m.index).index(item)].addNode(x)
            head.addSon(x)
            head = x
        else:
            theNode.addCount()
            head = theNode
# collect path for leaf to head
pathLists = []
for head in headList:
    trackLists = []
    for n in head.getList():
        tlist = [(n.getValue(), n.getCount())]
        print('\n', n.getValue(), n.getCount())
        print('|')
        trackLists.append(printNodeUp(n, tlist) )
    pathLists.append(trackLists)
# reverse path and set all node's count to leaf node's count
suffixLists = []
for pathlist in pathLists:
    suffixList = []
    for path in pathlist:
        path.reverse()
        n = path[-1][1]
        path = [(item[0],n) for item in path]
        suffixList.append(path)
    suffixLists.append(suffixList)
# build suffix tree
suffixTrees = []
for suffixList in suffixLists:
    head_null = node()
    for path in suffixList:
        head = head_null
        for item, value in path[:-1]:
            theNode = findNode(head, item)
            if theNode == None:
                newNode = node(item, head)
                newNode.setCount(value)
                head.addSon(newNode)
                head = newNode
            else:
                theNode.setCount(theNode.getCount() + value)
                head = theNode
    suffixTrees.append(head_null)
# get pattern from suffix tree
total_all = []
for i in range(len(suffixTrees)):
    print(m.index[i])
    total = printPatteren(suffixTrees[i],[],2,m.index[i],[])
    total_all += total
total_all.reverse()
for i in range(len(frequency)):
    total_all.append(list([frequency.index[i], frequency[i]]))
# output pattern to file
with open('patern_IBM.txt', 'w') as f:
    for p in total_all: 
        out_str = '('
        for item in p[:-2]:
            out_str = out_str +  '%s, '%item
        out_str += '%s) : %d\n'%(p[-2],p[-1])
        f.write(out_str)

