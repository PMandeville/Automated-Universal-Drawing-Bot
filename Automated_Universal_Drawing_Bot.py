import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from os import listdir
from PIL import Image as PImage
import numpy as np
import matplotlib.pyplot as plt

import cv2
import math

import six
import sys
sys.modules['sklearn.externals.six'] = six
import mlrose
import numpy as np

from tkinter import *
import re


query = str(input("What would you like to have drawn? "))
searchresult = '2'

ImageURL = "https://www.bing.com/images/search?q=" + query

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get(ImageURL)
time.sleep(1)
xpath = '//*[@id="mmComponent_images_2"]/ul[1]/li['+searchresult+']/div/div/a/div/img'
element = driver.find_element(By.XPATH, xpath)
src = element.get_attribute('src')
driver.get(src)
element = driver.find_element(By.XPATH, '/html/body/img')
newPath = "./"+query+".png"
element.screenshot(newPath)
driver.close()

imgName = query+".png"

img = cv2.imread(imgName)
cv2.imshow('Original Image', img)
cv2.waitKey()
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
cv2.imshow('Grayscale', img_gray)
cv2.waitKey()
img_blur = cv2.GaussianBlur(img_gray, (3,3), 0)
cv2.imshow('Gaussian Blur', img_blur)
cv2.waitKey()
edges = cv2.Canny(image=img_blur, threshold1=100, threshold2=300) # Canny Edge Detection
cv2.imshow('Edges', edges)
cv2.waitKey()

rows,cols,_ = img.shape

edgePixels = []

for i in range(cols):
    for j in range(rows):
        k = edges[j,i]
        if (k != 0):
            edgePixels.append(tuple([i,j]))
print("# of pixels to draw= "+str(len(edgePixels)))

vertexArr = [];
minVertexArr = [];
######

from collections import defaultdict
 
# Class to represent a graph

 
class Graph:
 
    def __init__(self, vertices):
        self.V = vertices  
        self.graph = []  

    def addEdge(self, u, v, w):
        self.graph.append([u, v, w])

    def find(self, parent, i):
        if parent[i] == i:
            return i
        return self.find(parent, parent[i])
    def union(self, parent, rank, x, y):
        xroot = self.find(parent, x)
        yroot = self.find(parent, y)

        if rank[xroot] < rank[yroot]:
            parent[xroot] = yroot
        elif rank[xroot] > rank[yroot]:
            parent[yroot] = xroot
        else:
            parent[yroot] = xroot
            rank[xroot] += 1

    def KruskalMST(self):
        result = [] 
        i = 0
        e = 0
        self.graph = sorted(self.graph,key=lambda item: item[2])
 
        parent = []
        rank = []
        for node in range(self.V):
            parent.append(node)
            rank.append(0)
        while e < self.V - 1:
            u, v, w = self.graph[i]
            if (len(self.graph)-1>i):
                i += 1
            else:
                break
            x = self.find(parent, u)
            y = self.find(parent, v)
            if x != y:
                e = e + 1
                result.append([u, v, w])
                self.union(parent, rank, x, y)
        minimumCost = 0
        for u, v, weight in result:
            minimumCost += weight
            minVertexArr.append(tuple([u,v]))
####
edges = []
                             
for i in range(len(edgePixels)):
    for j in range(len(edgePixels)-i-1):
        a = i
        b = i+j+1
        dist = math.sqrt((edgePixels[a][0]-edgePixels[b][0])**2+(edgePixels[a][1]-edgePixels[b][1])**2)
        edges.append([a,b,dist])

NumEdges = len(edges)

edges = sorted(edges, key=lambda x: x[2])
print("Num of edges to analyze & reduce = " + str(len(edges)))

g = Graph(NumEdges)
for edge in edges:
    g.addEdge(edge[0],edge[1],edge[2])
g.KruskalMST()

width = cols
height = rows
win=Tk()
dim = str(width)+"x"+str(height)
win.geometry(dim)

# Create a canvas widget
canvas=Canvas(win, width=width, height=height)
canvas.pack()

##rearrange edges to be in neighboring order
coords= edgePixels
edges = minVertexArr
newedges = []
print("edges length = "+str(len(edges)))
for i in range(len(edges)):
    if (len(newedges) == 0):
        newedges.append(edges[i])
        edges.pop(i)
    else:
        pairfound = False
        lastindex = len(newedges)-1
        lastcoord = [coords[newedges[lastindex][1]][0], coords[newedges[lastindex][1]][1]]
        for j in range(len(edges)):
            newfirstcoord = [coords[edges[j][0]][0], coords[edges[j][0]][1]]
            if (lastcoord == newfirstcoord):
                newedges.append(edges[j])
                edges.pop(j)
                pairfound = True
                break
        if (pairfound == False):
            newedges.append(edges[0])
            edges.pop(0)
print("newedges length = "+str(len(newedges)))
edges = newedges
## draw edges
maxLineLength = 5;
for edge in edges:
    if (math.sqrt((coords[edge[1]][0]-coords[edge[0]][0])**2+(coords[edge[1]][1]-coords[edge[0]][1])**2) < maxLineLength):
        canvas.create_line(coords[edge[0]][0], coords[edge[0]][1], coords[edge[1]][0], coords[edge[1]][1])
        win.update()
        time.sleep(0.01)
