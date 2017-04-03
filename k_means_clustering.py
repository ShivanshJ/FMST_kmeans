import random as rand
import math as math
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

from point import Point
from make_graph import complete_graph #To send cluster points for MST
from final_mst import *
#mean_mst - To send the centroids of each cluster
#new_midpoint_centroid_mst - for the new cluster formations

class clustering:
    def __init__(self, geo_locs_, k_):
        self.geo_locations = geo_locs_
        self.k = k_
        self.clusters = []  #clusters of nodes
        self.means = []     #means of clusters
        self.debug = False  #debug flag        
    
    #this method computes the initial means
    def initial_means(self, points):
        rng = rand.Random()
        length = len(self.geo_locations)
        clusters = dict()
        index_list = []
        i = 0
        while i < (self.k):
            index = rng.randrange(length)
            #print "index============",index
            if index not in index_list:
                point_ = self.geo_locations[index]
                #print "point_=======",point_
                clusters.setdefault(i, []).append(point_)
                #print "clusters=====",clusters
                i += 1
            index_list.append(index)
            print "index_list=======",index_list
        #compute mean of clusters
        self.means = self.compute_mean(clusters)
        if self.debug:
            print "initial means:"
            self.print_means(self.means)

    #the function which computes centroids       
    def compute_mean(self, clusters):
        means = []
        for cluster in clusters.values():
            mean_point = Point(0.0, 0.0)
            cnt = 0.0
            for point in cluster:
                #print "compute: point(%f,%f)" % (point.latit, point.longit)
                mean_point.latit += point.latit
                mean_point.longit += point.longit
                cnt += 1.0
            mean_point.latit = mean_point.latit/cnt
            mean_point.longit = mean_point.longit/cnt
            means.append(mean_point)

        mean_mst(means) ##Send centroid locations to final_mst
        return means    #this method assign nodes to the cluster with the smallest mean
    
    def assign_points(self, points):
        if self.debug:
            print "assign points"
        clusters = dict()
        for point in points:
            dist = []
            if self.debug:
                print "point(%f,%f)" % (point.latit, point.longit)
            #find the best cluster for this node
            for mean in self.means:
                dist.append(math.sqrt(math.pow(point.latit - mean.latit,2.0) + math.pow(point.longit - mean.longit,2.0)))
            #let's find the smallest mean
            if self.debug:
                print dist
            cnt_ = 0
            index = 0
            min_ = dist[0]
            for d in dist:
                if d < min_:
                    min_ = d
                    index = cnt_
                cnt_ += 1
            if self.debug:
                print "index: %d" % index
            clusters.setdefault(index, []).append(point)
        return clusters

    def update_means(self, means, threshold):
        #check the current mean with the previous one to see if we should stop
        for i in range(len(self.means)):
            mean_1 = self.means[i]
            mean_2 = means[i]
            if self.debug:
                print "mean_1(%f,%f)" % (mean_1.latit, mean_1.longit)
                print "mean_2(%f,%f)" % (mean_2.latit, mean_2.longit)            
            if math.sqrt(math.pow(mean_1.latit - mean_2.latit,2.0) + math.pow(mean_1.longit - mean_2.longit,2.0)) > threshold:
                return False
        return True
    
#..........................
#ALSO Accesses MST program    
    #debug function: print cluster points
    def print_clusters(self, clusters):
        print '\n\nSTEP 1 \nPress 0: To draw clusters on canvas \nPress 1: To print the cluster nodes'
        data = input()

        if data==1:
            cluster_cnt = 1
            for cluster in clusters.values():
                print "......Nodes in cluster #%d" % cluster_cnt
                cluster_cnt += 1            
                for point in cluster:
                    print "(%f,%f)" % (point.latit, point.longit)

            print 'Press 1 to draw clusters on canvas.'
            data=input()
        else:
            print '\nResults stored as list in - self.clusters=[]'
        plt.show()
        print '\n\n...............................Entering make_graph.py'
        return complete_graph(clusters)#returns final[u,v] (final MST edges) to--> final_one[] in run_main.py
#.........................
           
    #print means, in cases of self.debug
    def print_means(self, means):
        for point in means:
            print "%f %f" % (point.latit, point.longit)
            
    ##k_means algorithm, ......PLOTS the CLUSTERs
    def k_means(self, plot_flag):
        if len(self.geo_locations) < self.k:
            return -1   #error
        points_ = [point for point in self.geo_locations]

        ##.........Additional condition for new_midpoint_centroid_mst() : when recomputing
        #kmeans++ for final_two, where new centroid for clusters are : midpoints of the
        #edges of adjacent cluster centroid
        if plot_flag==1:
            self.initial_means(points_) #compute the initial means/centroids , and store in self.means
        elif plot_flag==2:
            self.means=new_midpoint_centroid_mst() #Instead of computing initial means/centroid , directly assign as we know the initial centroids
        stop = False
        while not stop:
            #assignment step: assign each node to the cluster with the closest mean
            points_ = [point for point in self.geo_locations]
            clusters = self.assign_points(points_)
            if self.debug:
                self.print_clusters(clusters)
                
            ##Recomputes the initial means/centroids
            means = self.compute_mean(clusters)

            #............
            if self.debug:
                print "means:"
                print self.print_means(means)
                print "update mean:"
            stop = self.update_means(means, 0.01)
            if not stop:
                self.means = []
                self.means = means
        self.clusters = clusters
        #plot cluster for evluation
        if plot_flag!=0:
            fig = plt.figure( figsize=(12,12))
            ax = fig.add_subplot(111)
            #plt.show()
            markers = ['x', 'd', 'o', 'h', 'H', 7, 4, 5, 6, '8', 'p', ',', '+', '.', 's', '*', 3, 0, 1, 2]
            colors = ['#5f9ea0', 'k', 'g', [0,0,0,0.5], '#191970', [0,1,0], [0,1,1], '#9400d3' , [1,0,1], '#c71585', '#8b8989', '#adff2f', '#ffa500','#ff0000','#32cd32' ]
            cnt = 0
            for cluster in clusters.values(): 
                latits = []
                longits = []
                for point in cluster:
                    latits.append(point.latit)
                    longits.append(point.longit)
                ax.scatter(latits, longits, s=55, c=colors[cnt%16], marker=markers[cnt%20], label=cnt+1)
                cnt += 1
            plt.legend()

            #draw re-draws figure
            plt.draw()
            #plt.show() --This is instead usedin print_clusters
            print '....................................End of clustering.py'
            return 0
