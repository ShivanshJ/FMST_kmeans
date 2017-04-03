#This makes subset mst's

from kruskal_mst import Graph
from point import Point
from final_mst import print_centroid #For printing centroid mst
from final_mst import mst       #To send clusters

import math as math
import numpy as np
import matplotlib.pyplot as plt

##This function makes the Subset-MST of each cluster
def complete_graph(clusters):  
    mst_all_clusters = []  
    for cluster in clusters.values():
        cluster_nodes=0           #To count total nodes/points in each cluster
        for point in cluster:
            cluster_nodes+=1 

        g = Graph(cluster_nodes)
        #To create an array of unique points in the cluster
        for point in cluster:
                g.unique(point)
                
        #............Path is for setting a flag
        path = []
        for i in range(len(cluster)):
            path.append(0)
        #...........
        i=0
        #Nested for making edge to each point
        for point1 in cluster:
            j=0
            for point2 in cluster: 
                    if point1!=point2 and path[j]==0:
                        g.convert_point_index(point1, point2, math.sqrt(math.pow(point1.latit - point2.latit,2.0) + math.pow(point1.longit - point2.longit,2.0)))
                    j+=1      
            path[i]=1
            i+=1
        mst_all_clusters.append([cluster, g.KruskalMST()])
        #g.KruskalMST() has the array results([u,v,w])
        #It has subset MST's
    #Printing
    print_mst(mst_all_clusters) #Under make_graph.py
    return mst(mst_all_clusters) #Under final_mst.py ##returns to --> cluster.print_clusters(),clustering.py --> final_one[] in run_main.py
    ##This function joins - Subset MST's ( mst_all_clusters[cluster number][0] stores u,v,w ) AND Centroid MST's(test stores u,v,w of all centroids)



def print_mst(mst_all_clusters):
        print 'STEP 2 \nPress 0: To draw MST on canvas \nPress 1: To show MST edges of each cluster'
        data = raw_input()

        cluster_cnt = 0
        #new window figure of size 12:12
        plt.figure(figsize=(12,12))
        for i in range(len(mst_all_clusters)):                          
            cluster_cnt += 1
            
            #Just for seeing if points were showing up( testing )
            #print "MST result in cluster #%d" % cluster_cnt
            #for point in mst_all_clusters[i][0]:
             #   print "Under MST(%f,%f)" % (point.latit, point.longit)
            if data==1:                                                    
                print "MST edges in nodes in cluster #%d" %cluster_cnt
            #print mst_all_clusters[i][1]
            for u,v,weight in mst_all_clusters[i][1]:
                if data==1:
                    print ("Distance from (%f,%f)  -- (%f,%f) is : %f" % (u.latit,u.longit,v.latit,v.longit, weight))
                #Now plotting it
                x=np.linspace(u.latit,v.latit)
                y=np.linspace(u.longit,v.longit)
                plt.plot(x, y)
        plt.draw()  
        plt.show()
        print '\nResults of MST edges stored in - mst_all_clusters[u,v,weight]'
        print '\n\n.................End of make_graph.py'
        print_centroid()
        


