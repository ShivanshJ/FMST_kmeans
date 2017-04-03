from point import Point
from kruskal_mst import Graph

import math as math
import numpy as np
import matplotlib.pyplot as plt

means =[]   #Stores the centroids as list
test=[]     #Stores the mst edges of centroid in the form u,v,weight

##Function to store final centroids of clusters as a global-list(means)
#used in clustering.py -> def compute_mean
def mean_mst(mean):
    print '....computing centroid means'
    global means
    means=[]
    for i in range(len(mean)):
        print "Cluster %d(%f,%f)" % (i+1,mean[i].latit, mean[i].longit)
        means.append(mean[i])

##Function to get MST of centroids of each cluster, and store in test[]
def print_centroid():
    print '\n\n............................Entering final_mst.py'
    cluster_nodes=0             #To print cluster numbers via no. of centroids
    for i in range(len(means)):
        cluster_nodes+=1

    global test
    test = []
    g = Graph(cluster_nodes)    #Initializing object Graph
    for i in range(len(means)):     #To create an array of unique points in the cluster
        g.unique(means[i])           #Even in make_graph while making MST
        
    path = []                    #............Path is for setting a flag
    for i in range(len(means)):
        path.append(0)
    
    for i in range(len(means)):
        for j in range(len(means)):
            if means[i]!=means[j] and path[j]==0:
                g.convert_point_index(means[i], means[j], math.sqrt(math.pow(means[i].latit - means[j].latit,2.0) + math.pow(means[i].longit - means[j].longit,2.0)))
        path[i]=1
        
    global test
    test = g.KruskalMST() #has [u,v,w]

    print 'STEP 3 \nPress 0: To draw MST of cluster CENTROIDS on canvas \nPress 1: To print MST edges of cluster CENTROIDS'
    data = input()
    plt.figure(figsize=(12,12)) #new window figure of size 12:12
    for u,v,weight in test:                          
            if data==1:
                print ("Distance from (%f,%f)  -- (%f,%f) is : %f" % (u.latit,u.longit,v.latit,v.longit, weight))
            #Now plotting it
            x=np.linspace(u.latit,v.latit)
            y=np.linspace(u.longit,v.longit)
            plt.plot(x, y)
    #plt.draw()  
    plt.show()


##...........This function joins - Subset MST's (of adjacent clusters(as in MST of centroids){ mst_all_clusters[cluster number][0] stores all point of every cluster ) AND Centroid MST(test stores u,v,w of all centroids)}

##final_one = [] In run_main.py, Stores the first final MST formed by joining subset MST's of all clusters
##final_two = [] In run_main.py, Stores the second final MST made from new_midpoint_centroid_mst()
def mst(mst_all_clusters):
    final=[] #RETURNS THE FINAL MST FORMED AFTER JOINING, as : final[[u.latit,u.longit],[v.latit,v.longit], weight] ,i.e, final[u,v]

    print '\nSTEP 4 \nJoining subset MSTs of cluster'
    print 'in mst()'
    plt.figure(figsize=(12,12))
    for u,v,weight in test:   
        a=means.index(u)
        b=means.index(v)
        #.....Plotting centroid of one cluster with closest point in other cluster
        shortest = 10000
        for point in mst_all_clusters[a][0]:
            s = math.sqrt(math.pow(v.latit - point.latit,2.0) + math.pow(v.longit - point.longit,2.0))
            if(s < shortest):
                shortest=s
                close_point1=point
        shortest = 10000
        for point in mst_all_clusters[b][0]:
            s = math.sqrt(math.pow(u.latit - point.latit,2.0) + math.pow(u.longit - point.longit,2.0))
            if(s < shortest):
                shortest=s
                close_point2=point
        
        x=np.linspace(close_point1.latit,close_point2.latit)
        y=np.linspace(close_point1.longit,close_point2.longit)
        plt.plot(x, y)
        final.append([close_point1,close_point2,  math.sqrt(math.pow(close_point1.latit - close_point2.latit,2.0) + math.pow(close_point1.longit - close_point2.longit,2.0))]) #Appends as u,v edge in final[]
    #.....Plotting the subset MST's again , were already stored in : mst_all_clusters[][1] (has MST edges of each cluster)
    for i in range(len(mst_all_clusters)):
        for m,n,weight in mst_all_clusters[i][1]:
            x=np.linspace(m.latit,n.latit)
            y=np.linspace(m.longit,n.longit)
            plt.plot(x, y)
            final.append([m,n,weight])   #Appends as u,v edge in final[]
    plt.show()
    print '....................................End of final_mst.py'
    return final    #returns to complete_graph() , make_graph.py --> cluster.print_clusters(), clustering.py --> final_one[] in run_main.py

##Function to return midpoint of adjacent centroids, in the list new[]
#accessed in clustering.py -> def k_means ; to return the midpoint centroids instead of def compute_mean
def new_midpoint_centroid_mst():
    new=[]
    for u,v,weight in test:
        x=Point( ((u.latit + v.latit)/2) , ((u.longit + v.longit)/2) )
        new.append(x)
    return new
