import random as rand
import math
from k_means_clustering import clustering
from point import Point
import csv

from kruskal_mst import Graph

import numpy as np
import matplotlib.pyplot as plt

geo_locs = []
#loc_ = Point(0.0, 0.0)  #tuples for location
#geo_locs.append(loc_)
#read the fountains location from the csv input file and store each fountain location as a Point(latit,longit) object
f = open('F:\Shivansh Work\University work VIT\Final Year Project\Python\k_means_kruskal\drinking_fountains.csv', 'r')
reader = csv.DictReader(f, delimiter=",")

ct=0 #key for geo_locs
x=0     # to restrict the number of data points chosen
for line in reader:
    #if x<25:
        ct+=1
        x += 1
        loc_ = Point(float(line['LATITUDE']), float(line['LONGITUDE']))  #tuples for location
        geo_locs.append(loc_)
print ct
   
'''
print len(geo_locs)
for p in geo_locs:
    print "%f %f" % (p.latit, p.longit)
'''

final_one = [] #In run_main.py, Stores the first final MST formed by joining subset MST's of all clusters
final_two = [] #In run_main.py, Stores the second final MST made from new_midpoint_centroid_mst()

#let's run k_means clustering. the second parameter is the no of clusters: root(N)
##..........aMST_one
cluster_nodes=15  #gives the number of clusters
cluster = clustering(geo_locs, cluster_nodes )
flag = cluster.k_means(1)


if flag == -1:
    print "Error in arguments!"
else:
    #the clustering results is a list of lists where each list represents one cluster
    final_one = cluster.print_clusters(cluster.clusters)

##.............aMST_two
print '\n\n..........................................................\n\n'
print 'Press 1 to make MSTs of the midpoints of the adjacent centroids of clusters'
data=input()

cluster_nodes=cluster_nodes-1
cluster_two = clustering(geo_locs, cluster_nodes )
flag= cluster_two.k_means(2)
final_two = cluster_two.print_clusters(cluster_two.clusters)

print '\n\n\n********************************************\n'
print 'Press 1 to join MST of clusters, and MST of centroid mid-points***'
data=input()


'''...............................................Making the final mst of the joined graph'''
##Making final_graph through finalone and finaltwo
final_graph=[]
plt.figure(figsize=(12,12))
plt.xlabel('Latitude')
plt.ylabel('Longitude')
plt.title("Joint subset-MSTs")
for u,v,w in final_one:
    x=np.linspace(u.latit,v.latit)
    y=np.linspace(u.longit,v.longit)
    plt.plot(x, y)
    final_graph.append([u,v,w])
for u,v,w in final_two:
    x=np.linspace(u.latit,v.latit)
    y=np.linspace(u.longit,v.longit)
    plt.plot(x, y)
    final_graph.append([u,v,w])
plt.show()

##***********************Making MST of the graph formed
final_mst=[]
g = Graph(ct)                           #Initializing object Graph, with total no. of data points

dict= {}
for u,v,w in final_graph:               #To create an array of unique points in the cluster
                                       #even in make_graph while making MST  
    if not(dict.has_key(u)):
        dict[u]=1
        g.unique(u)
    if not(dict.has_key(v)):
        dict[v]=1
        g.unique(v)
    
for u,v,w in final_graph:
    g.convert_point_index(u,v,w)

        
final_mst = g.KruskalMST()       #has [u,v,w]
plt.figure(figsize=(12,12))     #new window figure of size 12:12
plt.xlabel('Latitude')
plt.ylabel('Longitude')
plt.title("FINAL MST")
for u,v,weight in final_mst:                          
    x=np.linspace(u.latit,v.latit)
    y=np.linspace(u.longit,v.longit)
    plt.plot(x, y)
    #plt.draw()  
plt.show()
