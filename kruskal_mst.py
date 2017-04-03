# Python program for Kruskal's algorithm to find Minimum Spanning Tree
# of a given connected, undirected and weighted graph
import numpy as np
import matplotlib.pyplot as plt

from collections import defaultdict
 
#Class to represent a graph
class Graph:
 
    def __init__(self,vertices):
        self.V= vertices #No. of vertices
        self.graph = [] # default dictionary to store graph.
        self.indexy=[]   #MINE.....for making an array of all
                        #unique points in the cluster sent.
         
    #......MINE.....to create array of unique points, i.e, u contains u.latit & longit
    def unique(self, u):
        self.indexy.append(u)

    #.........MINE
    def convert_point_index(self, u, v, w):     
        self.addEdge(self.indexy.index(u), self.indexy.index(v),w)
        
    # function to add an edge to graph
    def addEdge(self,u,v,w):
        self.graph.append([u,v,w])
 
    # A utility function to find set of an element i
    # (uses path compression technique)
    def find(self, parent, i):
        if parent[i] == i:
            return i
        return self.find(parent, parent[i])
    
 
    # A function that does union of two sets of x and y
    # (uses union by rank)
    def union(self, parent, rank, x, y):
        xroot = self.find(parent, x)
        yroot = self.find(parent, y)
 
        # Attach smaller rank tree under root of high rank tree
        # (Union by Rank)
        if rank[xroot] < rank[yroot]:
            parent[xroot] = yroot
        elif rank[xroot] > rank[yroot]:
            parent[yroot] = xroot
        #If ranks are same, then make one as root and increment
        # its rank by one
        else :
            parent[yroot] = xroot
            rank[xroot] += 1


#................................................................. 
    # The main function to construct MST using Kruskal's algorithm
    def KruskalMST(self):
 
        result =[] #This will store the resultant MST
 
        i = 0 # An index variable, used for sorted edges
        e = 0 # An index variable, used for result[]
 
        #Step 1:  Sort all the edges in non-decreasing order of their
        # weight.  If we are not allowed to change the given graph, we
        # can create a copy of graph
        
        self.graph =  sorted(self.graph,key=lambda item: item[2])
        
    
        parent = [] ; rank = []

        '''#self.V gives nodes count; self.graph gives total edges made:
        print self.V
        print len(self.graph)
        '''
        
        # Create V subsets with single elements
        for node in range(self.V):
            parent.append(node)
            rank.append(0)  
#.......................Mine
            '''
        for node in range(self.V):
            print parent[node][1].latit
            '''
#........................    
        i = 0
        # Number of edges to be taken is equal to V-1
        while e < self.V -1 :
 
            # Step 2: Pick the smallest edge and increment the index
            # for next iteration
            u,v,w =  self.graph[i]
            i = i + 1
            x = self.find(parent, u)
            y = self.find(parent, v)
            
 
            # If including this edge does't cause cycle, include it
            # in result and increment the index of result for next edge
            if x != y:
                e = e + 1  
                result.append([ self.indexy[u], self.indexy[v],w])
                #result.append([ u,v,w])
                self.union(parent, rank, x, y)          
            # Else discard the edge
        
        '''#print the contents of result[] to display the built MST 
        print "Following are the edges in the constructed MST"
        for u,v,weight  in result:
            #print str(u) + " -- " + str(v) + " == " + str(weight)
            #print ("Distance from %d  -- %d is : %d" % (u,v, weight))
        
            x=np.linspace(u,v)
            y=np.linspace(u-1,v-2)
            plt.plot(x, y)
        plt.show()'''
        
        
        return result
 
'''
g = Graph(4)
g.addEdge(0, 3,  1)
g.addEdge(0, 1, 8)
g.addEdge(1, 2, 2)
g.addEdge(1, 3, 5)
g.addEdge(2, 3, 6)
 
g.KruskalMST()
'''



























