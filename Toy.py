#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np


# ### Class

# In[2]:


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
        #l = [son.getValue() for son in self.sonNodes]
        #print(len(self.sonNodes))


# In[3]:


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


# ### Function

# #### Find the node which value is target

# In[4]:


def findNode(head, target):
    if head.getSons() == []:
        return None
    else:
        for son in head.getSons():
            if son.getValue() == target:
                return son
    return None


# #### print the subtree which root is h

# In[5]:


def printNode(h):
    print(h.getValue(),h.getCount())
    if h.getSons() == []:
        print('-End-')
    else:
        for son in h.getSons():
            printNode(son)


# In[6]:


def printNodeUp(s, tracklist):
    p = s.getParent()
    if p.getValue() == None:
        print('-End-')
    else:
        print(p.getValue(), p.getCount())
        tracklist.append((p.getValue(), p.getCount()))
        tracklist = printNodeUp(p, tracklist)
    return tracklist 


# ### Read Data
# Toy Data : from FP-growth

# In[7]:


df = pd.read_csv('toydata.csv')
df = df.drop('TID', axis=1)
df['itemList'] = df['items'].str.split(',')
df


# In[8]:


totalList = []
for l in df['itemList']:
    for item in l:
        totalList.append(item)
frequency = pd.Series(totalList).value_counts()
headList = [node_head(item) for item in frequency.index]
frequency


# In[9]:


m = pd.Series((0,1,2,3,4),index=frequency.index)


# In[10]:


m


# In[11]:


for i in range(df.shape[0]):
    df['itemList'][i] = sorted(df['itemList'][i],key=lambda item : m[item] )
df


# In[12]:


headNode = node()
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


# In[13]:


printNode(headNode)


# In[14]:


pathLists = []
for head in headList:
    trackLists = []
    for n in head.getList():
        tlist = [(n.getValue(), n.getCount())]
        print('\n', n.getValue(), n.getCount())
        print('|')
        trackLists.append(printNodeUp(n, tlist) )
    pathLists.append(trackLists)


# In[15]:


pathLists


# In[16]:


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


# In[23]:


suffixLists


# In[150]:


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


# In[151]:


for h in suffixTrees:
    printNode(h)


# In[186]:


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


# In[200]:


total_all = []
for i in range(len(suffixTrees)):
    print(m.index[i])
    total = printPatteren(suffixTrees[i],[],2,m.index[i],[])
    total_all += total
for i in range(len(frequency)):
    total_all.append(list([frequency.index[i], frequency[i]]))


# In[199]:


total_all

