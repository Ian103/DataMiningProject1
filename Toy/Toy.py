#!/usr/bin/env python
# coding: utf-8


import pandas as pd
import numpy as np


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
        print('Son :', [son.getValue() for son in self.sonNodes()])


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

def printNode(h):
    print(h.getValue(),h.getCount())
    if h.getSons() == []:
        print('-End-')
    else:
        for son in h.getSons():
            printNode(son)

def printNodeUp(s, tracklist):
    p = s.getParent()
    if p.getValue() == None:
        print('-End-')
    else:
        print(p.getValue(), p.getCount())
        tracklist.append((p.getValue(), p.getCount()))
        tracklist = printNodeUp(p, tracklist)
    return tracklist 

df = pd.read_csv('toydata.csv')
df = df.drop('TID', axis=1)
df['itemList'] = df['items'].str.split(',')


totalList = []
for l in df['itemList']:
    for item in l:
        totalList.append(item)
frequency = pd.Series(totalList).value_counts()
headList = [node_head(item) for item in frequency.index]

m = pd.Series((0,1,2,3,4),index=frequency.index)


for i in range(df.shape[0]):
    df['itemList'][i] = sorted(df['itemList'][i],key=lambda item : m[item] )

for itemlist in df['itemList']:
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

pathLists = []
for head in headList:
    trackLists = []
    for n in head.getList():
        tlist = [(n.getValue(), n.getCount())]
        print('\n', n.getValue(), n.getCount())
        print('|')
        trackLists.append(printNodeUp(n, tlist) )
    pathLists.append(trackLists)

suffixLists = []
for pathlist in pathLists:
    suffixList = []
    for path in pathlist:
        path.reverse()
        n = path[-1][1]
        path = [(item[0],n) for item in path]
        suffixList.append(path)
    suffixLists.append(suffixList)
    print(suffixList)
    print('----')

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

for h in suffixTrees:
    printNode(h)

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

total_all = []
for i in range(len(suffixTrees)):
    print(m.index[i])
    total = printPatteren(suffixTrees[i],[],2,m.index[i],[])
    total_all += total
total_all.reverse()
for i in range(len(frequency)):
    total_all.append(list([frequency.index[i], frequency[i]]))

with open('patern_Toy.txt', 'w') as f:
    for p in total_all: 
        out_str = '('
        for item in p[:-2]:
            out_str = out_str +  '%s, '%item
        out_str += '%s) : %d\n'%(p[-2],p[-1])
        f.write(out_str)

